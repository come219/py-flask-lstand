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


# flask
app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'  # Use simple caching that uses a hashmap
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


# player avatar
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



@app.route('/api/players/recipes/rename', methods=['POST'])
def post_player_recipe_rename():
    '''
    # post recipe rename
    Allows player to rename recipe without altering else
    
    Potentially removing rename in recipe_update function
    
    {
    "recipe_table": "player_recipe1",
    "recipe_name": "Default Recipe",
    "player_id": 25
    }
    '''

@app.route('/api/players/recipes/activate', methods=['POST'])
def post_player_recipe_activate():
    '''
    Allows player to active recipe without altering else in recipe
    Also triggers unactive for other recipes ..
    
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


##########################
#
# membership service
#
##########################


# get_player_membership function
#   -> to return all membership values using id

@app.route('/api/players/membership/bool', methods=['POST'])
def get_player_membership_bool():
    """
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



##########################
# streak service
##########################

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
    log_file_path = '/flask_log.log'  # Adjust the path accordingly
    return send_from_directory('.', 'flask_log.log', as_attachment=True)




app.add_url_rule('/home','home', index)



if __name__ == '__main__':
    app.logger.info("Server start")
    print("\n\nserver starting ...")
    print("\n\n")
    app.run(host=host, port=port, debug=True)

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
