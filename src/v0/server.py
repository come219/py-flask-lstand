from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
from firebase_handler import FirebaseHandler
#from mysql_handler import MySQLHandler  # Import the MySQLHandler class
#from flask_mysqldb import MySQL  
from user_service import UserService  
from server_service import ServerService  

from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'  # Use simple caching that uses a hashmap
cache = Cache()
cache.init_app(app)



#mysql = MySQL(app)
#ysql_handler = MySQLHandler(app)  # Create an instance of MySQLHandler

# app.config['CACHE_TYPE'] = 'simple'
# app.config['MYSQL_HOST'] = 'spectre219'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1337'
# app.config['MYSQL_DB'] = 'lstand_db'

port = 8888
host = "0.0.0.0"



scores = {"pete": 4, "john": 1, "timmy": 3}  # Some initial data for testing


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




#######
#
# server_service
#
######

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
    """
    try:
        connection = server_service.get_server_connection()
        return jsonify(connection), 200

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500






####
#
# player_service
#
#####



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


@app.route('/api/players/recipes/update', methods=['POST'])
def post_player_recipe_update():
    """
    # post_player_recipe_update
    
    
    
    
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
    
    ###
    
    {
    "recipe_table": "player_recipe1",
    "recipe_name": "Default Recipe",
    "recipe_active": false,
    "player_id": 25,
    "quality": "Medium",
    "flavour_string": "",
    "flavour_effects": ["Cool", "Dry", "Balanced", "Mild"],
    "pricing": 5.99,
    "cups": "Small",
    "ingredients": {
        "water": {"amount": 169.0},
        "ice": {"amount": 0.0},
        "sugar": {"amount": 0.0},
        "salts": {"amount": 0.0},
        "base": {
            "lemon": {"amount": 3},
            "lime": {"amount": 1}
        },
        "others": {
            "tea": {"amount": 0.0}
        }
    }
    }

    """
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
        
        return jsonify({"success": True, "message": "Player recipe updated successfully", "player_id": player_id}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500
        
        

@app.route('/api/players/recipes/default', methods=['POST'])
def post_player_recipe_default():
    """
    # post_player_recipe_default
    {
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
        
        
        
        
####
#
# player levels
#
###
        


@app.route('/api/players/levels/xp/increase', methods=['POST'])
def post_level_xp_increase():
    """
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
    
    POTENTIALLY TO BE CHANGED IF BALANCE, <currencies> reimplemented into player table
    
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
    
    POTENTIALLY TO BE CHANGED IF <currencies> reimplemented into player table
    
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


@app.route('/api/players/streak', methods=['POST'])
def get_player_streak():
    """
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




@app.route('/api/players/days/increase', methods=['POST'])
def increase_player_days():
    """
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
        
       


# post_player_lives():
@app.route('/api/players/lives', methods=['POST'])
def post_player_lives():
    """
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

        return jsonify({"success": True, "message": "Player lives updated successfully", "player_id": id, "lives": lives}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


# get player email
@app.route('/api/players/email', methods=['POST'])
def post_player_email_by_id():
    """
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




# post_player_username
@app.route('/api/players/username', methods=['POST'])
def post_player_username():
    """
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

        return jsonify({"success": True, "message": "Player username retrieved successfully", "player_id": id, "username": username}), 201

    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"success": False, "error": str(e)}), 500


# post player_id by username
@app.route('/api/players/id_by_username', methods=['POST'])
def post_player_id_by_username():
    """
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

       
        
@app.route('/api/players/items', methods=['POST'])
def get_player_items():
    """
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
    
    THIS WILL BE CHANGED IF <currencies> reimplemented into player table.
    
    
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





@app.route('/api/players/create', methods=['POST'])
def create_player():
    """
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
class ScoreSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    score = fields.Integer(required=True, allow_none=False,
                           validate=[Range(min=1, error="Value must be greater than 0")])

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(status='pong'), 200
    
@app.route('/pong', methods=['POST'])
def pong():
    # if body == "ping":
        # return "Received 'ping'."
    # elif body == "pong":
        # return "Received 'pong'."
    # elif body == "":
        # return jsonify(status='empty'), 200
    # else:
        # return "The body contains an unexpected value."
    return jsonify(status='ping'), 200


if __name__ == '__main__':
    app.run(host=host, port=port)

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
