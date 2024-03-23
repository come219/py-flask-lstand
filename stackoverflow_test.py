# stackoverflow question

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import jwt
from datetime import datetime, timedelta
from functools import wraps
import uuid
import re
from datetime import datetime, timedelta
import threading
import time
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from collections.abc import Mapping


app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple' 
app.config['SECRET_KEY'] = 'secret_key'
cache = Cache()
cache.init_app(app)


# logging
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler('flask_log.log', maxBytes=1024*1024 * 10, backupCount=10)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

port = 8888
host = "0.0.0.0"
import MySQLdb

jwt_manager = JWTManager(app)

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="db_password",  # your password
                     db="database_table")        # name of the data base


# Define a decorator for authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_resource():
    """
    A protected resource that requires a valid token for access.
    """
    return jsonify({'message': 'This is a protected resource!'})

@app.route('/login', methods=['POST'])
def login():
    '''
    login for refresh, access token 
    '''
    try:
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'message': 'Could not verify'}), 401
        
        # Check if the username exists
        if filter_by_username(auth['username']):
            # Retrieve the hashed password associated with the provided username
            hashed_password = get_hashed_password(auth['username'])
            
            # Validate the password
            if validate_password(auth['password'], hashed_password):
                # Retrieve the user ID by username
                user_id = get_player_id_by_username(auth['username'])
                
                # Check if the user ID is retrieved successfully
                if user_id is not None:
                    # Define the expiration time for the token
                    expiration_time = datetime.utcnow() + timedelta(minutes=30)
                    
                    # Generate the JWT token with the "sub" claim set to the user ID
                    secret_key = str(app.config['SECRET_KEY'])
                    token_payload = {'sub': user_id, 'username': auth['username'], 'exp': expiration_time}
                    # token = jwt.encode(token_payload, bytes(secret_key, 'utf-8'))

                    token = jwt.encode({'username': auth['username'], 'exp': expiration_time}, bytes(secret_key, 'utf-8'))

                    
                    # Generate access and refresh tokens
                    access_token = generate_access_token(user_id, secret_key)
                    refresh_token = generate_refresh_token(user_id)
                    
                    # Store the refresh token securely
                    store_refresh_token(user_id, refresh_token)
                    
                    # Return the access and refresh tokens
                    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
                else:
                    return jsonify({'message': 'User ID not found'}), 404
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'Invalid credentials'}), 401 
    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500 

  

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    '''
    Endpoint to verify the validity of a JWT token (access).
    
    Expected JSON body:
    {
        "token": "JWT_access_token_here"
    }
    
    Returns JSON response indicating token validity.
    '''
    try:
        # Get the JWT token from the request
        token = request.json.get('token')

        # Validate input
        if not token:
            return jsonify({'message': 'Token is missing'}), 400

        try:
            # Decode the JWT token payload
            decoded_token = jwt.decode(token, options={"verify_signature": False})  # Don't verify signature for decoding payload only

            if 'user_id' in decoded_token:
                return jsonify({'valid': True, 'user_id': decoded_token['user_id']}), 200
            else:
                return jsonify({'valid': False, 'message': 'Token is missing "user_id" claim'}), 400



            # Ensure the decoded token is a dictionary
            if 'sub' in decoded_token:
                return jsonify({'valid': True, 'user_id': decoded_token['sub']}), 200
            else:
                return jsonify({'valid': False, 'message': 'Token is missing "sub" claim'}), 400


            # Check if the "sub" claim is present in the payload
            if 'sub' in decoded_token:
                return jsonify({'valid': True, 'user_id': decoded_token['sub']}), 200
            else:
                return jsonify({'valid': False, 'message': 'Token is missing "sub" claim'}), 400
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return jsonify({'valid': False, 'message': 'Token is expired'}), 401
    except Exception as e:
        return jsonify({'valid': False, 'message': f'An error occurred: {e}'}), 500

@app.route('/refresh', methods=['POST'])
def refresh():
    '''
    user auth refresh token
    
    
    '''
    refresh_token = request.json.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 400
    
    user_id = verify_refresh_token(refresh_token)
    secret_key = str(app.config['SECRET_KEY'])
    try:
        if user_id:
            access_token = generate_access_token(user_id, secret_key)
            return jsonify({'access_token': access_token})
        else:
            return jsonify({'message': 'Invalid refresh token'}), 401
    except Exception as e:
        return jsonify({'valid': False, 'message': f'An error occurred: {e}'}), 500



def _verify_token(token):
    try:
        # Decode the JWT token payload
        decoded_token = jwt.decode(token, options={"verify_signature": False})  # Don't verify signature for decoding payload only
        
        # Check if the "user_id" or "sub" claim is present in the decoded token
        if 'user_id' in decoded_token:
            return True, decoded_token['user_id']
            print("verified token")
        elif 'sub' in decoded_token:
            return True, decoded_token['sub']
            print("verified token")
        else:
            return False, None
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return False, None
    except jwt.DecodeError:
        # Handle invalid token
        return False, None
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return False, None


@app.route('/api/player-id', methods=['POST'])
def get_player_id_by_username():
    '''
    Endpoint to retrieve a player's ID by their username.
    
    Expected JSON body:
    {
        "username": "player_username_here"
    }
    
    Returns JSON response with the player's ID if found.
    '''
    try:
        # Get the username from the request
        username = request.json.get('username')

        if not username:
            return jsonify({'message': 'Username is missing'}), 400

        # Call the service method to get the player's ID
        player_id = get_player_id_by_username(username)

        if player_id is not None:
            return jsonify({'success': True, 'player_id': player_id}), 200
        else:
            return jsonify({'success': False, 'message': f'No player found with username: {username}'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'An error occurred: {e}'}), 500



'''
Player Avatar Service

table: player_avatar
+-------------------+--------+------+-----+---------+-------+
| Field             | Type   | Null | Key | Default | Extra |
+-------------------+--------+------+-----+---------+-------+
| player_id         | bigint | YES  | MUL | NULL    |       |
| avatar_id         | int    | YES  |     | NULL    |       |
| profile_border_id | int    | YES  |     | NULL    |       |
+-------------------+--------+------+-----+---------+-------+

'''

@app.route('/api2/players/avatar', methods=['POST'])
@jwt_required()
def post_player_avatar2():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    # post_player_avatar by id
    {   
    "player_id": "28"
    }
    """

    secret_key = str(app.config['SECRET_KEY'])

    try:

        # # Extract the JWT token from the request headers
        token = request.headers.get('Authorization')

        #  # Ensure that the token exists
        if not token:
            return jsonify({"success": False, "error": "Missing JWT token"}), 401


        # verify token call?
        
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')

        results = post_player_avatar_by_id(player_id)

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player avatar object retrieved successfully", "player_id": player_id, "avatar_obj": results}), 200
        else:
            return jsonify({"success": False, "message": "No player avatar object found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/avatar', methods=['POST'])
def post_player_avatar():
    """
    # post_player_avatar by id
    {   
    "player_id": "28"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')

        results = post_player_avatar_by_id(player_id)

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player avatar object retrieved successfully", "player_id": player_id, "avatar_obj": results}), 200
        else:
            return jsonify({"success": False, "message": "No player avatar object found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500



# 
def post_player_avatar_by_id(player_id):
    """
    Retrieve player avatars by player_id.
    change from fetch all () ??
    """
    cur = db.cursor()
    select_sql = """
        SELECT *
        FROM player_avatar
        WHERE player_id = %s
    """
    try:
        cur.execute(select_sql, (player_id,))
        avatars = cur.fetchall()
        if avatars:
            return avatars, 200
        else:
            return {"message": f"No avatars found for player ID {player_id}"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
    


def post_player_avatar_by_id(player_id):
    """
    Retrieve player avatars by player_id.
    change from fetch all () ??
    """
    cur = db.cursor()
    select_sql = """
        SELECT *
        FROM player_avatar
        WHERE player_id = %s
    """
    try:
        cur.execute(select_sql, (player_id,))
        avatars = cur.fetchall()
        if avatars:
            return avatars, 200
        else:
            return {"message": f"No avatars found for player ID {player_id}"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
    
    

def get_player_id_by_username(username):
    '''
    Retrieves player ID by username from the player table
    
    Parameters:
    - username: Username of the player
    
    Returns:
    - Player's ID if found, None otherwise
    '''
    query = 'SELECT player_id FROM player_security WHERE username = %s;'
        
        
    try:
        cur = db.cursor()
        cur.execute(query, (username,))
        db.commit()
        result = cur.fetchone()  # Fetch the first record
        if result is not None:
            print(f"Fetching ID for username: {username}")
            return result[0]  # Return the player ID
        else:
            # possible error
            logging.info(f"No ID found for username: {username}")
            return None
    
    except Exception as e:
        print(f"No ID found for username: {username}")
        # print(f"An error occurred while fetching username for Player {player_id}: {e}")
        return None
    finally:
        cur.close()
        


    
def generate_access_token( user_id, secret_key):
    '''
    user auth func
    '''
    # Generate an access token with a short expiration time (e.g., 15 minutes)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, app.config['SECRET_KEY'])
    
    # access_token = jwt.encode({'user_id': user_id}, secret_key, algorithm='HS256')
    token = jwt.encode({'user_id': user_id, 'sub': user_id, 'exp': expiration}, secret_key, algorithm='HS256')
    # return token.decode('UTF-8')
    return token

def generate_refresh_token( user_id):
        '''
        user auth func
        '''
        # Generate a refresh token with a longer expiration time (e.g., 7 days)
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        token = jwt.encode({'user_id': user_id, 'exp': expiration}, app.config['SECRET_KEY'])
        # return token.decode('UTF-8')
        return token




def verify_refresh_token(self, refresh_token):
    '''
    user auth func
    Verifies the refresh token and returns the associated user ID if valid.
    '''
    try:
        payload = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Check if the token is expired
        expiration_timestamp = payload.get('exp')
        if expiration_timestamp is not None and datetime.datetime.utcfromtimestamp(expiration_timestamp) < datetime.datetime.utcnow():
            expiration_datetime = datetime.datetime.utcfromtimestamp(expiration_timestamp)
            if expiration_datetime < datetime.datetime.utcnow():
                raise jwt.ExpiredSignatureError('Token has expired')
        # Check if the refresh token is valid (e.g., check if it exists in the database)
        if self.is_valid_refresh_token(user_id, refresh_token):
            return user_id
        else:
            raise jwt.exceptions.DecodeError('Invalid refresh token')
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token has expired')  # Token has expired
    except jwt.exceptions.DecodeError as e:
        # Log or handle invalid token error
        print(f"Invalid token: {e}")
        # raise jwt.DecodeError('Invalid refresh token')
        return jsonify({'valid': False, 'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'valid': False, 'message': f'An error occurred: {e}'}), 500
    

def store_refresh_token( user_id, refresh_token):
        '''
        Stores the refresh token in the player_token table.
        
        NOTES: check if token_id needs to be unique, &  increment??

        :param user_id: The ID of the player.
        :param refresh_token: The refresh token to be stored.
        :return: True if the refresh token was successfully stored, False otherwise.
        '''
        try:
            # Generate access token
            access_token = str(uuid.uuid4())

        
            # Get a database cursor
            cur = db.cursor()

            # Define the INSERT query
            
            insert_query = """
            INSERT INTO player_token (player_id, access_token, refresh_token, expiration_date, creation_date, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            # Calculate expiration date (e.g., set expiration 7 days from creation)
            expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)

            # Get current date and time for creation and last_updated fields
            current_datetime = datetime.datetime.utcnow()

            # Execute the INSERT query with parameters
            cur.execute(insert_query, (user_id, access_token, refresh_token, expiration_date, current_datetime, current_datetime))
            
            # Commit the transaction
            db.commit()

            # Close the cursor
            cur.close()

            return True
        except Exception as e:
            # If an error occurs, rollback the transaction
            db.rollback()
            print(f"An error occurred while storing refresh token: {e}")
            return False
    

def validate_password( user_input, hashed_password):
        """
        Validates the user's input password against the hashed password.
        Returns True if the input password matches the hashed password, False otherwise.
        """
        try:
            # Verify the input password against the hashed password
            return bcrypt.checkpw(user_input.encode('utf-8'), hashed_password)
        except Exception as e:
            print(f"An error occurred during password validation: {e}")
            return False
    

def get_hashed_password( username):
        """
      
        """
        cur = db.cursor()

        query_sql = """
            SELECT password
            FROM player_security
            WHERE username = %s;
        """

        try:
            cur.execute(query_sql, (username,))
            result = cur.fetchone()
            
            # if result:
            #    return result[0]  # Return the hashed password if the username exists
                
            if result:
                return result[0].encode('utf-8')

            else:
                return None  # Return None if the username doesn't exist
        except Exception as e:
            # Handle any exceptions (e.g., database connection issues)
            print(f"An error occurred while filtering by username {username}: {e}")
            return None
        finally:
            cur.close()


def filter_by_username( username):
        """
        Filter by username for login.
        Returns True if the username exists, False otherwise.
        """
        cur = db.cursor()

        query_sql = """
            SELECT *
            FROM player_security
            WHERE username = %s;
        """
        query_sql_v2 = """
            SELECT COUNT(*) AS user_count
            FROM player_security
            WHERE username = %s;
        """

        try:
            cur.execute(query_sql, (username,))
            result = cur.fetchone()
            # user_count = result['user_count']
            user_count = result[0]
            return user_count > 0
        except Exception as e:
            # Handle any exceptions (e.g., database connection issues)
            print(f"An error occurred while filtering by username {username}: {e}")
            return False
        finally:
            cur.close()



if __name__ == '__main__':
    try:
        app.logger.info("Server Start.")
        
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        # Log error when server encounters an exception
        app.logger.error(f"An error occurred: {e}")
    finally:
        
        # Log when server closes
        app.logger.info("The Server has closed.")

