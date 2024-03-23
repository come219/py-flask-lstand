'''
lstand server - 219

    - flask
    - mysql
    

'''


from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
from firebase_handler import FirebaseHandler
#from mysql_handler import MySQLHandler  # Import the MySQLHandler class
#from flask_mysqldb import MySQL  
from user_service import UserService  
from server_service import ServerService  

from flask_cors import CORS

import logging
from logging.handlers import RotatingFileHandler
import bcrypt
import jwt
from datetime import datetime, timedelta

from functools import wraps
#from jwt.exceptions import InvalidTokenError
#from jwt.exceptions import DecodeError



# from flask_jwt_extended import jwt_required, get_jwt_identity

import uuid

import re

from datetime import datetime, timedelta
import threading
import time

# from flask_jwt import jwt_required
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager


from collections.abc import Mapping

# Open the file api_jwt.py located at C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\venv\lib\site-packages\jwt\api_jwt.py.



# flask
app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'  # Use simple caching that uses a hashmap
app.config['SECRET_KEY'] = 'lstand'
cache = Cache()
cache.init_app(app)


# logging
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = RotatingFileHandler('flask_log.log', maxBytes=1024*1024 * 10, backupCount=10)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


#mysql = MySQL(app)
#ysql_handler = MySQLHandler(app)  # Create an instance of MySQLHandler

# app.config['CACHE_TYPE'] = 'simple'
# app.config['MYSQL_HOST'] = 'spectre219'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1337'
# app.config['MYSQL_DB'] = 'lstand_db_2'

port = 8888
host = "0.0.0.0"


jwt_manager = JWTManager(app)


scores = {"bob": 4, "john": 1, "james": 3}  # Some initial data for testing


firebase_handler = FirebaseHandler()    # Initialize FirebaseHandler
user_service = UserService(app)         #item_service, #inventory_service
server_service = ServerService(app)         #server service
#role_service
#auth_service


#server_service
#game_service, #shops_service


#orders_service
#trades_service
#notification_service
#messaging_service

#payment_service
#logging_service


# secret_key = str(app.config['SECRET_KEY'])



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
    
    - user login function:
        - calls filter_by_username
        - not calls filter_by_email
        - calls valid_password
 
    
    login with email ..
    
    implement try-catch??
    
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inh6MjhyZWNpcGUiLCJleHAiOjE3MTA2MTA2NjB9.6PGAaZzHWVsl3wowtIcpkVUwMwD7syst7fnbndeEFx4"
    }
    
    - need to implement refresh / access tokens
    
    '''
    # You'll need to implement your own login logic here.
    # For demonstration purposes, let's assume you receive a username and password in JSON format.
    try:
        auth = request.get_json()

        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'message': 'Could not verify'}), 401

    
        # Check if the username and password are correct (you need to implement this logic)
        # Check if the username exists
        # filter by username..
        if user_service.filter_by_username(auth['username']):
            # You can add password validation logic here
            # For example: if valid_password(auth['username'], auth['password']):
            # if not user or not user.check_password(auth['password']):
            #     return jsonify({'message': 'Invalid credentials'}), 401
            
            # Retrieve the hashed password associated with the provided username from your database
            hashed_password = user_service.get_hashed_password(auth['username'])
            
            #secret_key = str(app.config['SECRET_KEY'])
            secret_key = str(app.config['SECRET_KEY'])
            #secret_key = 'lstand'
            
            

            
            #validate_password
            # Validate the password
            if user_service.validate_password(auth['password'], hashed_password):
                # Generate a JWT token
                # token = jwt.encode({'username': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, str(secret_key).encode('utf-8'))
                token = jwt.encode({'username': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, bytes(secret_key, 'utf-8'))
                #return jsonify({'token': token.decode('UTF-8')})
                return jsonify({'token': token})
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500  
        
        
        
#######################
##  refresh, access token
#
# Input Validation: Ensure that you validate the inputs received in the /login2 and /refresh routes. Validate the structure and content of the JSON payloads to prevent unexpected behavior or security vulnerabilities.
#
# Authentication Middleware: Implement middleware to authenticate requests that require access tokens. This middleware can verify the access token before allowing access to protected routes, providing a centralized mechanism for authentication.
# 
# Token Expiration Strategy: Consider implementing a more flexible token expiration strategy. Instead of hardcoding token expiration times in the token generation functions, you can make these values configurable, allowing for easier adjustment or customization based on your application's needs.
# 
# Database Connection Pooling: Utilize database connection pooling to manage database connections more efficiently. This can improve the performance and scalability of your application by reducing the overhead of creating and closing database connections for each request.
# 
# Security Enhancements: Review your application's security measures regularly and stay updated on best practices for securing authentication systems. This includes measures such as securely storing sensitive data (e.g., secret keys, passwords), using HTTPS for communication, and implementing measures to prevent common security vulnerabilities like SQL injection and cross-site scripting (XSS).
# 
# Unit Testing: Implement unit tests to verify the correctness of your authentication-related functions and routes. Unit testing helps ensure that your code behaves as expected under various scenarios and reduces the risk of introducing regressions when making changes.
# 
# Documentation: Provide comprehensive documentation for your authentication system, including usage examples, endpoint descriptions, and error handling guidelines. Clear documentation helps developers understand how to use your API and troubleshoot issues effectively.
# 
# Rate Limiting: Consider implementing rate limiting to protect against brute-force attacks and prevent abuse of your authentication endpoints. Rate limiting can help mitigate the impact of malicious or excessive requests on your server's resources.
#
#
#######################




@app.route('/login2', methods=['POST'])
def login2():
    '''
    login for refresh, access token 
    '''
    try:
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'message': 'Could not verify'}), 401
        
        # Check if the username exists
        if user_service.filter_by_username(auth['username']):
            # Retrieve the hashed password associated with the provided username
            hashed_password = user_service.get_hashed_password(auth['username'])
            
            # Validate the password
            if user_service.validate_password(auth['password'], hashed_password):
                # Retrieve the user ID by username
                user_id = user_service.get_player_id_by_username(auth['username'])
                
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
                    access_token = user_service.generate_access_token(user_id, secret_key)
                    refresh_token = user_service.generate_refresh_token(user_id)
                    
                    # Store the refresh token securely
                    user_service.store_refresh_token(user_id, refresh_token)
                    
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



@app.route('/login2_OLD', methods=['POST'])
def login2_OLD():
    '''
    login for refresh, access token 
    
    
    '''
    try:
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            return jsonify({'message': 'Could not verify'}), 401
        
        
        # Your login logic here... 
        # Check if the username and password are correct
        # Check if the username exists
        # filter_by_username()
        if user_service.filter_by_username(auth['username']):
            # password validation logic
            
            # Retrieve the hashed password associated with the provided username from your database
            hashed_password = user_service.get_hashed_password(auth['username'])
            
            secret_key = str(app.config['SECRET_KEY'])
            
            # Validate the password
            # validate_password()
            if user_service.validate_password(auth['password'], hashed_password):
                # Generate a JWT token
                
                
                # but need user_id -get user_id by username?
                # Call the relevant service method to get player ID ('user_id') by username
                # user_id = user_service.get_player_id_by_username(username)
                
                user_id = user_service.get_player_id_by_username(auth['username'])  # Assuming this method exists
                
                # expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

                # token = jwt.encode({'username': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, bytes(secret_key, 'utf-8'))
                
                expiration_time = datetime.utcnow() + timedelta(minutes=30)
                # token = jwt.encode({'username': auth['username'], 'exp': expiration_time}, bytes(secret_key, 'utf-8'))

                # token = jwt.encode({'sub': user_id, 'exp': expiration_time}, bytes(secret_key, 'utf-8'))
                token = jwt.encode({'sub': user_id, 'username': auth['username'], 'exp': expiration_time}, bytes(secret_key, 'utf-8'))

               
                # return jsonify({'token': token})
                
                # Part - 2, get access tokens, refresh_tokens..
        
            
                # Assuming successful login
                access_token = user_service.generate_access_token(user_id, secret_key)
                refresh_token = user_service.generate_refresh_token(user_id)
                
                # Store the refresh token securely (e.g., in a database)
                user_service.store_refresh_token(user_id, refresh_token)
                
                # return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
                #return jsonify({'access_token': access_token.decode('UTF-8'), 'refresh_token': refresh_token.decode('UTF-8')})
                return jsonify({'access_token': access_token, 'refresh_token': refresh_token})
               
                
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
            # if not isinstance(decoded_token, dict):
            #     raise jwt.DecodeError("Invalid token payload")
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
        # except jwt.DecodeError:
        #     # Handle invalid token
        #     return jsonify({'valid': False, 'message': 'Invalid token'}), 401

        # except InvalidTokenError:
            # Handle invalid token
            # return jsonify({'valid': False, 'message': 'Invalid token'}), 401
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
    
    user_id = user_service.verify_refresh_token(refresh_token)
    secret_key = str(app.config['SECRET_KEY'])
    try:
        if user_id:
            access_token = user_service.generate_access_token(user_id, secret_key)
            return jsonify({'access_token': access_token})
        else:
            return jsonify({'message': 'Invalid refresh token'}), 401
    # except InvalidTokenError:
    #    return jsonify({'message': 'Invalid refresh token'}), 401
    # except jwt.DecodeError:
    #     # Handle invalid token
    #     return jsonify({'valid': False, 'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'valid': False, 'message': f'An error occurred: {e}'}), 500







####
#
# player_service
#
#####

# curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer your_jwt_token_here" -d '{"player_id": "25"}' http://localhost:8888/api2/players/avatar


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
            return False, "Missing user_id or sub claim in token"
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return False, "Expired JWT token"
    except jwt.DecodeError:
        # Handle invalid token
        return False, "Invalid JWT token"
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return False, str(e)

def verify_token2(token):
    try:
        # Extract the token from the "Bearer" prefix
        token = token.split(" ")[1]
        
        # Decode the JWT token payload
        decoded_token = jwt.decode(token, options={"verify_signature": False})  # Don't verify signature for decoding payload only
        
        # Check if the "user_id" or "sub" claim is present in the decoded token
        if 'user_id' in decoded_token:
            # print('verify_token', decoded_token['user_id'])
            return decoded_token['user_id']
        elif 'sub' in decoded_token:
            return decoded_token['sub']
        else:
            raise ValueError("Missing user_id or sub claim in token")
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise ValueError("Expired JWT token")
    except jwt.DecodeError:
        # Handle invalid token
        raise ValueError("Invalid JWT token")
    except Exception as e:
        # Handle other exceptions
        raise ValueError(f"An error occurred: {e}")



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
        player_id = user_service.get_player_id_by_username(username)

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


@app.route('/api2/players/avatar/change', methods=['POST'])
@jwt_required()
def post_player_avatar_change2():
    """
    # post_player_avatar_change by id with jwt
    {
       example json body using player_id and avatar_id
    }
    """
    try:
        token = request.headers.get('Authorization')

        #  # Ensure that the token exists
        if not token:
            return jsonify({"success": False, "error": "Missing JWT token"}), 401

        
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        avatar_id = data.get('avatar_id')

        # Verify token
        verify_id_or_error  = verify_token2(token)

        if str(verify_id_or_error) != str(player_id):
            return jsonify({"success": False, "error": "Player ID mismatch"}), 322



        results = user_service.post_player_change_avatar(player_id, avatar_id )

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player avatar object retrieved successfully", "player_id": player_id, "avatar_obj": results}), 200
        else:
            return jsonify({"success": False, "message": "No player avatar object found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/avatar/change', methods=['POST'])
def post_player_avatar_change():
    """
    # post_player_avatar_change by id
    {
       example json body using player_id and avatar_id
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        avatar_id = data.get('avatar_id')

        results = user_service.post_player_change_avatar(player_id, avatar_id )

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player avatar object retrieved successfully", "player_id": player_id, "avatar_obj": results}), 200
        else:
            return jsonify({"success": False, "message": "No player avatar object found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api2/players/avatar', methods=['POST'])
@jwt_required()
def post_player_avatar2():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    # post_player_avatar by id
    {
       example json body using player_id
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
        # valid, verify_id_or_error  = _verify_token(token)
        

        # token
        # print("\n TOKEN :", token)
    
        
        verify_id_or_error  = verify_token2(token)


        # if not valid:
        #  return jsonify({"success": False, "error": "error JWT token {}".format(verify_id_or_error )}), 401


        #  # Decode the JWT token to get the payload
        # try:
        #     payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        # except jwt.ExpiredSignatureError:
        #     return jsonify({"success": False, "error": "Expired JWT token"}), 401
        # except jwt.InvalidTokenError:
        #     return jsonify({"success": False, "error": "Invalid JWT token"}), 401



        # # Get the current user's identity from the JWT token
        # current_user = get_jwt_identity()
        # 
        # # Check if the "sub" claim is present in the JWT token
        # if current_user.get('sub') is None:
        #     return jsonify({"success": False, "error": "Missing 'sub' claim in JWT token"}), 400


        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')

        # if verify_id_or_error is not None:
           # If verify_id_or_error is not None, it means there was an error during token verification
        #   return jsonify({"success": False, "error": verify_id_or_error}), 401        


        

        # print("verify_id_or_error:", verify_id_or_error)
        # print('player_id:'+player_id)

        # if verify_id_or_error.strip() != player_id.strip():
        #    return jsonify({"success": False, "error": "Player ID mismatch"}), 322

        if str(verify_id_or_error) != str(player_id):
            return jsonify({"success": False, "error": "Player ID mismatch"}), 322


        # if verify_id_or_error != player_id:
        #    return jsonify({"success": False, "error": "Player ID mismatch"}), 322

        results = user_service.post_player_avatar_by_id(player_id)

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
       example json body using player_id
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')

        results = user_service.post_player_avatar_by_id(player_id)

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player avatar object retrieved successfully", "player_id": player_id, "avatar_obj": results}), 200
        else:
            return jsonify({"success": False, "message": "No player avatar object found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500




'''
Player Recipes Service

    4 player recipe tables.
    
    
    functions:
        - get_player_recipe1():
        - get_player_recipe2():
        - get_player_recipe3():
        - get_player_recipe4():
        * post_player_recipe_rename():
        * post_player_recipe_activate():
        - post_player_recipe_update():
        - post_player_recipe_default():
        - post_player_recipe_default_init():
        - post_player_recipe_use():



Table: mysql> desc player_recipe1;
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int          | NO   | PRI | NULL    | auto_increment |
| recipe_name     | varchar(255) | YES  |     | NULL    |                |
| player_id       | bigint       | YES  | MUL | NULL    |                |
| recipe_active   | tinyint(1)   | YES  |     | NULL    |                |
| quality         | varchar(255) | YES  |     | NULL    |                |
| flavour_string  | varchar(255) | YES  |     | NULL    |                |
| flavour_effects | json         | YES  |     | NULL    |                |
| pricing         | double       | YES  |     | NULL    |                |
| cups            | varchar(255) | YES  |     | NULL    |                |
| ingredients     | json         | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
10 rows in set (0.00 sec)


'''




# recipes

# use recipe default - post_player_recipe_use

# 

# post player recipe use
# get all active and use

# get player recipe active



@app.route('/api/players/recipes/1', methods=['POST'])
def get_player_recipe1():
    """
    # get_player_recipe1
    @jwt_required()  # Requires a valid JWT token to access this route
    
    {
       example json body using player_id
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')

        # Call the function to get the player's recipe
        results = user_service.get_player_recipe1(player_id)

        if results is not None:
            # Return the results as a JSON response
            return jsonify({"success": True, "message": "Player recipe1 retrieved successfully", "player_id": player_id, "recipes": results}), 200
        else:
            return jsonify({"success": False, "message": "No player recipes found for player ID", "player_id": player_id}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500

# get_player_recipe2
@app.route('/api/players/recipes/2', methods=['POST'])
def get_player_recipe2():
    """
    # get_player_recipe2
    @jwt_required()  # Requires a valid JWT token to access this route
    
    """
    try:
        data = request.json
        player_id = data.get('player_id')
        results = user_service.get_player_recipe2(player_id)
        if results is not None:
            return jsonify({"success": True, "message": "Player recipe2 retrieved successfully", "player_id": player_id, "recipes": results}), 200
        else:
            return jsonify({"success": False, "message": "No player recipes found for player ID", "player_id": player_id}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# get_player_recipe3
@app.route('/api/players/recipes/3', methods=['POST'])
def get_player_recipe3():
    """
    # get_player_recipe3
    @jwt_required()  # Requires a valid JWT token to access this route
    
    """
    try:
        data = request.json
        player_id = data.get('player_id')
        results = user_service.get_player_recipe3(player_id)
        if results is not None:
            return jsonify({"success": True, "message": "Player recipe3 retrieved successfully", "player_id": player_id, "recipes": results}), 200
        else:
            return jsonify({"success": False, "message": "No player recipes found for player ID", "player_id": player_id}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# get_player_recipe4
@app.route('/api/players/recipes/4', methods=['POST'])
def get_player_recipe4():
    """
    # get_player_recipe4
    @jwt_required()  # Requires a valid JWT token to access this route
    
    """
    try:
        data = request.json
        player_id = data.get('player_id')
        results = user_service.get_player_recipe4(player_id)
        if results is not None:
            return jsonify({"success": True, "message": "Player recipe4s retrieved successfully", "player_id": player_id, "recipes": results}), 200
        else:
            return jsonify({"success": False, "message": "No player recipes found for player ID", "player_id": player_id}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/api/players/recipes/rename', methods=['POST'])
def post_player_recipes_rename():
    '''
    # post recipe rename
    Allows player to rename recipe without altering else
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    Potentially removing rename in recipe_update function
    
    {
    "recipe_table": "player_recipe1",
    "recipe_name": "Default Recipe",
    "player_id": 25
    }
    '''
    try:
        # Extract data from the JSON request
        data = request.json
        recipe_table = data.get('recipe_table')
        new_recipe_name = data.get('recipe_name')
        player_id = data.get('player_id')

        # Call the service method to rename the recipe
        user_service.post_player_recipe_rename(recipe_table, new_recipe_name, player_id)

        # Return success response
        return jsonify({"success": True, "message": "Player recipe renamed successfully", "player_id": player_id}), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route('/api/players/recipes/activate', methods=['POST'])
def post_player_recipe_activate():
    '''
    Allows player to active recipe without altering else in recipe
    Also triggers unactive for other recipes ..
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    Potentially removing active in recipe_update function??
    
    {
    "recipe_table": "player_recipe1",
    "recipe_active": true,
    "player_id": 25
    }
    '''

@app.route('/api/players/recipes/update', methods=['POST'])
def post_player_recipe_update():
    """
    # post_player_recipe_update
    
    Updates  a singular targetted table recipe.
   
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    
    body example:
    {
        "recipe_table": "player_recipe1",
        "recipe_name": "Default Recipe",
        "recipe_active": true,
        "player_id": 25,
        "quality": "Medium",
        "flavour_string": "",
        "flavour_effects": ["Cool", "Dry", "Balanced", "Mild"],
        "pricing": 5.99,
        "cups": "Cups",
        "ingredients": {

            "Liquids": {
                "water": {"amount": 169.0}
            },

            "Cooling": {
                "ice": {"amount": 0.0}
            },


            "Sugars": {
                "sugar": {"amount": 0.0}
            },
            "Salts": {
                "salts": {"amount": 0.0}
            },

            "Base": {
                "lemons": {"amount": 3}
            },

            "Others": {
                "tea": {"amount": 0.0}
            }
        }
    }

    """
    
    # dumps ??
    
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        recipe_table = data.get('recipe_table')
        recipe_name = data.get('recipe_name')
        recipe_active = data.get('recipe_active')
        quality = data.get('quality')
        flavour_string = data.get('flavour_string')
        flavour_effects = data.get('flavour_effects')
        pricing = data.get('pricing')
        cups = data.get('cups')
        ingredients = data.get('ingredients')

        user_service.post_player_recipe_update(recipe_table, recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients)
        
        return jsonify({"success": True, "message": "Player {recipe_table} recipe updated successfully", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        


@app.route('/api/players/recipes/use', methods=['POST'])
def post_player_recipes_use():
    """
    # post_player_recipe_use
    
    API function to use chosen player recipe.
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
    "player_id": 25,
    "recipe_table": "player_recipe1",
    }
    """
    try:
        data = request.json
        player_id = data.get('player_id')
        recipe_table = data.get('recipe_table')
        
        user_service.post_player_recipes_use(recipe_table, player_id)
        
        return jsonify({"success": True, "message": "Player recipe used successfully", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        

@app.route('/api/players/recipes/pitchers/use', methods=['POST'])
def post_player_recipes_pitchers_use():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    # post_player_recipe_picthers_use
    online edition - simple
    - requires current weather - simple string
    - requires current location  - number
    - interprets weather for random vals
    - provides the cups sold
    - provides the tips sold
    
    API function to use chosen player recipe.
    {
    "player_id": 25,
    "recipe_table": "player_recipe1",
    }
    """
    
    
    def interpretValuesWeather(_weather):
         switch = {
            "clear skies": 10,
            "sunny": 9,
            "windy": 8,
            "rainy": 2,
            "snowy": 1,
            # Add more cases for other weather conditions as needed
        }

    return switch.get(_weather.lower(), "Sunny")

    def interpretValuesLocation(_location):
         switch = {
            0: 5,
            1: 7,
            2: 9,
            3: 2,
            4: 1,
            # Add more cases for other weather conditions as needed
        }

    return switch.get(_location, 0)
        
    weather_condition = "Clear Skies"
    location = 0

    
    try:
        data = request.json
        player_id = data.get('player_id')
        recipe_table = data.get('recipe_table')
        weather_json = data.get('weather_json')
        location_val = data.get('location_val')
        
        weather_condition = weather_json
        location = location_val
        weather_value = interpretValuesWeather(weather_condition)
        location_value = interpretValuesLocation(location)
        
        npc_population = weather_value * location_value
        
        # random generate number against npc_population to generate npc demand
        
        
        # not use recipe use function
        # new function that does a for loop for the 
        # amount of pitchers and cups in pitchers (7)
        # random generate cups sold - to return
        # random generate tips given - to return
        # npc multiplier (npc_population) - to return
        # npc demand (npc_demand) random val generated - to return
        #
        user_service.post_player_recipes_use(recipe_table, player_id)
        
        return jsonify({"success": True, "message": "Player recipe used successfully", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
   




@app.route('/api/players/recipes/default', methods=['POST'])
def post_player_recipe_default():
    """
    # post_player_recipe_default
    API function to default chosen player recipe.
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
    "player_id": 25,
    "recipe_table": "player_recipe1"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        recipe_table = data.get('recipe_table')
        

        user_service.post_player_recipe_default(recipe_table, player_id)
        
        return jsonify({"success": True, "message": "Player recipe updated successfully - defaulted", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
        
@app.route('/api/players/recipes/default/init', methods=['POST'])
def post_player_recipe_default_init():
    """
    # post_player_recipe_default
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    ?? why is this an api call.
    {
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        recipe_table = data.get('recipe_table')
        

        user_service.post_player_recipe_default_init(recipe_table, player_id)
        
        return jsonify({"success": True, "message": "Player recipe init successfully - defaulted", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
        
        


'''
Player Levels Service


    functions:
    - post_level_xp_increase()
    ? post_level_currentlevel_increase()
    - get_player_levels()
    - get_player_balance()
    - get_player_mtx_coins()
   
    

Table: mysql> desc player_levels;
+----------------+--------+------+-----+---------+-------+
| Field          | Type   | Null | Key | Default | Extra |
+----------------+--------+------+-----+---------+-------+
| player_id      | bigint | NO   | PRI | NULL    |       |
| level_id       | bigint | NO   | PRI | NULL    |       |
| current_level  | int    | YES  |     | NULL    |       |
| achieved_level | int    | YES  |     | NULL    |       |
| xp_level       | int    | YES  |     | NULL    |       |
+----------------+--------+------+-----+---------+-------+

Levels: mysql> select * from levels;
+----+-----------+
| id | name      |
+----+-----------+
|  1 | campaign  |
|  2 | openworld |
|  3 | endday    |
|  4 | trading   |
|  5 | farming   |
|  6 | fishing   |
|  7 | mining    |
|  8 | crafting  |
|  9 | casino    |
| 10 | fire      |
| 11 | pool      |
| 12 | magic     |
| 13 | slayer    |
| 14 | dungeon   |
| 15 | rpg       |
| 16 | combat    |
| 17 | agility   |
| 18 | summoning |
| 19 | charisma  |
+----+-----------+
19 rows in set (0.00 sec)






'''
        


@app.route('/api/players/levels/xp/increase', methods=['POST'])
def post_level_xp_increase():
    """
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    {
        "player_id": "25",
        "level_id": "1",
        "num_xp": "1"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        level_id = data.get('level_id')
        num_xp = data.get('num_xp')

        user_service.post_level_xp_increase(player_id, level_id, num_xp)
        
       
        # possibly checks for level increase?
        

        return jsonify({"success": True, "message": "Player xp lvl increased successfully", "player_id": player_id, "level": level_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/levels', methods=['POST'])
def get_player_levels():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        levels = user_service.post_player_levels_by_id(id)

        return jsonify({"success": True, "message": "Player levels retrieved successfully", "player_id": id, "levels": levels}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500



# get player main level
# post, to calc the main level

@app.route('/api/players/items/balance', methods=['POST'])
def get_player_balance():
    """
    
    OLD -> POTENTIALLY TO BE CHANGED IF BALANCE, <currencies> reimplemented into player table
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        balance = user_service.get_player_items_balance(id)

        return jsonify({"success": True, "message": "Player balance retrieved successfully", "player_id": id, "balance": balance}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
        
@app.route('/api/players/items/mtxcoins', methods=['POST'])
def get_player_mtx_coins():
    """
    
    OLD -> POTENTIALLY TO BE CHANGED IF <currencies> reimplemented into player table
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        mtx_coins = user_service.get_player_items_mtx_coins(id)

        return jsonify({"success": True, "message": "Player mtxcoins retrieved successfully", "player_id": id, "mtxcoins": mtx_coins}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500




'''
Player Membership Service




'''


@app.route('/api/players/membership/bool', methods=['POST'])
def get_player_membership_bool():
    """
    
    # get_player_membership function
    #   -> to return all membership values using id
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    get_player_membership post function
    
    intends to retrieve membership boolean value
    
    body:
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')         # id -> player_id ??

        membership = user_service.get_player_membership_bool(id)

        return jsonify({"success": True, "message": "Player membership retrieved successfully", "player_id": id, "membership": membership}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


# get_player_membership_status
# -> string related membership data


@app.route('/api/players/membership/timer', methods=['POST'])
def get_player_membership_timer():
    """
    get_player_membership_timer
    
    intends to retrieve membership timer value
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    body:
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')         # id -> player_id ??

        membership = user_service.get_player_membership_timer(id)

        return jsonify({"success": True, "message": "Player membership timer retrieved successfully", "player_id": id, "membership": membership}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500



'''
Player Streak Service


    functions: 
    - get_player_streak()
    * check_player_streak()
    * get_player_streak_freeze_use()
    * post_player_streak_freeze_use()
    ? post_player_streak_life_use()
    * post_player_streak_update()
    * post_player_streak_save()
    - post_player_streak_default()
    - get_player_streak_highscores()
    - post_player_streak_highscore()

'''

@app.route('/api/players/streak', methods=['POST'])
def get_player_streak():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        streak = user_service.get_streak_counter(id)

        return jsonify({"success": True, "message": "Player streak retrieved successfully", "player_id": id, "streak": streak}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/streak/check', methods=['POST'])
def get_player_streak_check():
    """
    gets the player_streak time and check if less or equal else default
    
    @jwt_required() ?? called by server
    
    body:
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        streak = user_service.get_streak_counter(id)

        return jsonify({"success": True, "message": "Player streak checked successfully", "player_id": id, "streak": streak}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/api/players/streak/update', methods=['POST'])
def post_player_streak_update():
    """
    updates the player_streak time and if less or equal else default
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    body:
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        streak = user_service.get_streak_counter(id)

        return jsonify({"success": True, "message": "Player streak update successfully", "player_id": id, "streak": streak}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"error, player streak update failed.": False, "error": str(e)}), 500

'''
Player Days Service

    functions:
    - increase_player_days()
    * increase_player_days_value()
    - get_player_days()

'''


@app.route('/api/players/days/increase', methods=['POST'])
def increase_player_days():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        user_service.increase_day_counter(id)

        return jsonify({"success": True, "message": "Player days increased successfully", "player_id": id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/days', methods=['POST'])
def get_player_days():
    """
    TEST CHECK IF DOUBLE VALUE RETURN WORKS
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        days = user_service.get_day_counter(id)

        return jsonify({"success": True, "message": "Player days retrieved successfully", "player_id": id, "days": days}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
       


'''
Player Lives Service

    functions:
    - post_player_lives()
    * increase_player_lives_value()
    * decrease_player_lives_value()
    * check_player_lives_value()
    * check_player_lives_effects()

'''

# post_player_lives():
@app.route('/api/players/lives', methods=['POST'])
def post_player_lives():
    """
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')
        #lives = data.get('lives')

        # Call the relevant service method to update player lives
        lives = user_service.get_player_lives(id)

        return jsonify({"success": True, "message": "Player lives retrieved successfully", "player_id": id, "lives": lives}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


'''
Player Info Services

    functions:
    - post_player_email_by_id()
    - post_player_username()
    - post_player_id_by_username()
    
    


'''




@app.route('/api/players/email', methods=['POST'])
def post_player_email_by_id():
    """
    Get player Email
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        # Call the relevant service method to get player email by ID
        player_email = user_service.get_player_email_by_id(id)

        if player_email is not None:
            return jsonify({"success": True, "message": "Player email retrieved successfully", "player_id": id, "email": player_email}), 201
        else:
            return jsonify({"success": False, "error": f"No email found for Player ID {id}"}), 404

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500




@app.route('/api/players/username', methods=['POST'])
def post_player_username():
    """
    post_player_username
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        # Call the relevant service method to update player username
        username =user_service.get_player_username(id)
        
        # Ensure all result sets are fetched before executing a new query
        # while user_service.connection.more_results():
        #     user_service.connection.next_result()

        return jsonify({"success": True, "message": "Player username retrieved successfully", "player_id": id, "username": username}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players/id_by_username', methods=['POST'])
def post_player_id_by_username():
    """
    Post player_id by username
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "username": "new_username"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        username = data.get('username')

        # Call the relevant service method to get player ID by username
        player_id = user_service.get_player_id_by_username(username)

        return jsonify({"success": True, "message": "Player ID retrieved successfully", "username": username, "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500

       
'''
Player Items Services

    functions:
    - get_player_items()
    - post_player_items_buy_item()
    
    
    

'''
        
@app.route('/api/players/items', methods=['POST'])
def get_player_items():
    """
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
        "id": "25"
    }
    
    {
    items
    message
    player_id
    success
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        id = data.get('id')

        items = user_service.post_player_items_by_id(id)

        return jsonify({"success": True, "message": "Player items retrieved successfully", "player_id": id, "items": items}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500



@app.route('/api/players/items/buy', methods=['POST'])
def post_player_items_buy_item():
    """
    
    OLD -> THIS WILL BE CHANGED IF <currencies> reimplemented into player table.
    
    @jwt_required()  # Requires a valid JWT token to access this route
    
    
    {
    "player_id": "25",
    "item_id": "5",
    "balance_minus": "2",
    "item_quantity": "1"
    }

    """
    try:
        # Extract data from the JSON request
        data = request.json
        player_id = data.get('player_id')
        item_id = data.get('item_id')
        balance_minus = data.get('balance_minus')
        item_quantity = data.get('item_quantity')

        # Call the function to buy the item
        user_service.post_player_items_buy_item(player_id, item_id, balance_minus, item_quantity)

        return jsonify({"success": True, "message": f"Player ID {player_id} successfully bought {item_quantity} of item ID {item_id}."}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500





'''
Player Services

    functions:
    - create_player()
    - get_users()
    - get_player()
    
    
    
    

'''


@app.route('/api/players/create', methods=['POST'])
def create_player():
    """
    Register & create player .. 
    
    {
    "email": "z25@example.com",
    "username": "z25",
    "password": "securepassword",
    "first_name": "2",
    "last_name": "2",
    "dob": "1990-01-01"
    }

    
    
    
    
    {
        "email": "player@example.com",
        "username": "player123",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe",
        "dob": "1990-01-01"
    }
    """
    try:
        # Extract data from the JSON request
        data = request.json
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        
        # Check if the email is in a valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"success": False, "error": "Invalid email format"}), 400
            
            
            
        # password checker
        # Check if the password is of valid length
        # if len(password) < 8 or len(password) > 20:
        #    return jsonify({"success": False, "error": "Password must be between 8 and 20 characters"}), 400

        # Check if the password is strong
        # if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        #    return jsonify({"success": False, "error": "Password must contain at least one letter and one number"}), 400
        

        # Create the player
        player_id = user_service.create_player(email, username, password, first_name, last_name, dob)

        # Initialize the player
        user_service.init_player(player_id)

        return jsonify({"success": True, "message": "Player created successfully", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/players', methods=['GET'])
def get_users():
    return jsonify(user_service.get_players())
    
    
@app.route('/api/players/<username>', methods=['GET'])
def get_player(username):
    player = user_service.get_player(username)
    return jsonify(player)








# Schema used to validate scores POST payload so only specified fields are accepted
# to be removed ..
class ScoreSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    score = fields.Integer(required=True, allow_none=False,
                           validate=[Range(min=1, error="Value must be greater than 0")])




#######
#
# server_service
#
######


@app.route('/api/server/info/id', methods=['POST'])
def post_server_info_by_id():
    """
    POST method to get the current server info by id.
    
    """
    try:
        server_time = server_service.post_server_info_by_id()
        return jsonify({"success": True, "server_time": str(server_time)}), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
 

@app.route('/api/server/info', methods=['GET'])
def get_server_info():
    """
    Get the current server time.
    """
    try:
        server_info = server_service.get_server_info()
        return jsonify({"success": True, "server_info": str(server_info)}), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        

@app.route('/api/server/time', methods=['GET'])
def get_server_time():
    """
    Get the current server time.
    """
    try:
        server_time = server_service.get_server_time()
        return jsonify({"success": True, "server_time": str(server_time)}), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
        
@app.route('/api/server/timezone', methods=['GET'])
def get_server_timezone():
    """
    Get the current server timezone.
    """
    try:
        server_timezone = server_service.get_server_timezone()
        return jsonify({"success": True, "server_timezone": server_timezone}), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500

        
        
@app.route('/api/server/location', methods=['GET'])
def get_server_location():
    """
    Get the current server location.
    """
    try:
        server_location = server_service.get_server_location()
        return jsonify(server_location), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500




@app.route('/api/server/connection', methods=['GET'])
def get_server_connection():
    """
    Get the current server connection.
    
    Possibly related to hop worlds,
    
    Should increase player count?
    """
    try:
        connection = server_service.get_server_connection()
        print("server connection request")
        return jsonify(connection), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500





'''
Server Services


'''

@app.route('/ping', methods=['GET'])
def ping():
    '''
    Ping function to the server.
    GET Method
    
    If there is no response it returns an error or 404
    else it will return pong, status 200.
    '''
    return jsonify(status='pong'), 200
    
@app.route('/pong', methods=['POST'])
def pong():
    '''
    Pong function to the server.
    POST Method
    
    If there is no response it returns an error or 404
    else it will return ping, status 200.
    
    Old implementation:
    '''
    # if body == "ping":
        # return "Received 'ping'."
    # elif body == "pong":
        # return "Received 'pong'."
    # elif body == "":
        # return jsonify(status='empty'), 200
    # else:
        # return "The body contains an unexpected value."
    return jsonify(status='ping'), 200


@app.route('/')
def index():
    '''
    index.html to show the main webpage, can be used to verify connection.
    
    '''
    #if not is_server_online:
    #    return redirect(url_for('offline'))
    #return render_template('index.html')
    
    if not is_server_online:
        abort(404)
    return render_template('index.html')
    
    
is_server_online = True  # Change to False to simulate offline state
                   
            
@app.route('/offline')
def offline():
    '''
    offline.html to show a page when the server is offline.
    '''
    return render_template('offline.html')

@app.errorhandler(404)
def not_found(error):
    '''
    not_found.html to show a page when the server is offline.
    '''
    return render_template('not_found.html'), 404

@app.route('/flask_log.log')
def serve_log_file():
    '''
    server function to send logs to a file.
    
    sends on start.
    '''
    log_file_path = '/flask_log.log'  # Adjust the path accordingly
    return send_from_directory('.', 'flask_log.log', as_attachment=True)

app.add_url_rule('/home','home', index)



def print_server_time():
    '''
    server function to print the time
    
    called at start & every 15 minutes
    
    '''
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("\nServer time:", current_time)
            # Wait for 15 minutes
            next_time = datetime.now() + timedelta(minutes=15)
            while datetime.now() < next_time:
                # Check every second if 15 minutes have passed
                time.sleep(1)
    except Exception as e:
            print(f"An error occurred: {e}")


'''
main python

    runs the server.
    
    notes:
    - multi-threading
    - restarting
    - backup/restore services
    - sync servers
    - auth impl.
    - refactor services to class files

'''
if __name__ == '__main__':
    try:
        app.logger.info("Lstand Server Start.")
        print("\n\nVersion 0.004, 19/3/24")
        #print("\n\n")
        print("\n\nServer starting ...")
        #print("\n\n")
        print("\n\nEnsure tables ...")
        #print("\n\n")
        print("\n\nRestoring backups ...")
        print("\n\nSyncing servers ...")
        #print("\n\n")
        
        print("\n\nInit tools ...")
        print(" timer tool:")
        # Start a separate thread to print server time every 15 minutes
        thread = threading.Thread(target=print_server_time)
        thread.daemon = True  # Set the thread as daemon
        thread.start()
        #thread.join() ? # Wait for it to finish
        
        print(" player count tool:")
        print(" restart tool:")
        print(" error tool:")
        print("\n\n")
        
        
        
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        # Log error when server encounters an exception
        app.logger.error(f"An error occurred: {e}")
    finally:
        
        # Log when server closes
        app.logger.info("The Server has closed.")



# main with mysql server check -> function
# if __name__ == '__main__':
    # with app.app_context():
        # try:
            # # Now you can access the database connection
            # cursor = mysql.connection.cursor()
            # # Perform database operations here
        # except Exception as e:
            # print(f"An error occurred: {e}")
        # finally:
            # # Ensure the cursor is closed even if an error occurs
            # cursor.close()
    # app.run(host=host, port=port)


# print version, log etc

# check backups, restore,

# sync other servers

# tools defs