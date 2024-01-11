from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
from firebase_handler import FirebaseHandler
from mysql_handler import MySQLHandler  # Import the MySQLHandler class
from flask_mysqldb import MySQL  


app = Flask(__name__)
mysql = MySQL(app)



# app = Flask(__name__)
# app.config['CACHE_TYPE'] = 'simple'  # Use simple caching that uses a hashmap
# cache = Cache()
# cache.init_app(app)

# mysql = MySQL(app)
# mysql_handler = MySQLHandler(app)  # Create an instance of MySQLHandler


# app.config['CACHE_TYPE'] = 'simple'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'mysql'
# app.config['MYSQL_PASSWORD'] = '1337'
# app.config['MYSQL_DB'] = 'lstand_db'

# port = 8888
# host = "0.0.0.0"


class UserService:

    
    def __init__(self, app):
        self.app = app

    def get_connection(self):
        with self.app.app_context():
            return self.app.mysql.connection

    def __del__(self):
        #self.cursor.close()
        #self.connection.close()
        pass


    # Player


    # register player?
    
    
    
    # create player -     # need to call  security, roles, update,
    #
    # role not implemented
    # update not implemented
    def create_player(self, email, username, password, first_name, last_name, dob):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = '''
            INSERT INTO player (
                player_days, player_lives, player_streak, player_streak_timer,
                player_networth, player_location, player_offers_notifications,
                player_trade_requests, player_inbox_messages, player_private, player_hide,
                current_campaign, level_campaign, xp_campaign,
                current_openworld, level_openworld, xp_openworld,
                current_endday, level_endday, xp_endday,
                current_trading, level_trading, xp_trading,
                current_farming, level_farming, xp_farming,
                current_fishing, level_fishing, xp_fishing,
                current_mining, level_mining, xp_mining,
                current_crafting, level_crafting, xp_crafting,
                current_casino, level_casino, xp_casino,
                current_fire, level_fire, xp_fire,
                current_pool, level_pool, xp_pool,
                current_magic, level_magic, xp_magic,
                current_slayer, level_slayer, xp_slayer,
                current_dungeon, level_dungeon, xp_dungeon,
                current_rpg, level_rpg, xp_rpg,
                current_combat, level_combat, xp_combat,
                current_agility, level_agility, xp_agility,
                current_summoning, level_summoning, xp_summoning,
                current_charisma, level_charisma, xp_charisma,
                main_level, total_level, total_xp, quest_points, quest_level
            )
            VALUES (
                0, 0, 0, NULL, 0, '', 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0
            );
        '''

        try:
            # Assuming you have a database connection and cursor, execute the query like this:
            cursor.execute(query)

            # Commit the changes to the database
            connection.commit()

            print("Player created successfully")

        except Exception as e:
            # Handle the exception
            print(f"Error creating player: {e}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

    # Example usage:
    # create_player()

    
    # init player start?
    # need to call update, items, inventory, 
    def init_player(self, username):
        try:
            # Insert a new record into the 'player_update' table with default or NULL values
            cursor.execute("""
                INSERT INTO player_update (
                    player_id, action_id, user_location, user_last_update,
                    user_uptime, user_playtime, user_last_logout, connected,
                    player_ip, player_irl_location, player_os, player_current_region,
                    player_home_region, player_pref_region
                )
                SELECT id, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL
                FROM player
                WHERE username = %s
            """, (username,))

            # Commit the changes to the database
            db_connection.commit()

            # Obtain the player_id for the specified username
            player_id = cursor.lastrowid

            # Call functions to initialize player items and inventory
            self.init_player_items_start(player_id)
            self.init_player_inventory_start(player_id)

            print(f"Player {username} initialized successfully with player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error initializing player {username}: {e}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

    # Example usage:
    # init_player('example_username')


    
    
    # init player save
    
    # get user role
    


    # get players
    def get_players(self):
        
        query = 'SELECT * FROM player;'
        
        
         # Execute the query
        # Assuming 'cursor' is a database cursor object connected to your database
        cursor.execute(query)
        
        # Fetch all records and return them
        results = cursor.fetchall()
        
        print("Fetching all users")
        
        # Check if any results were found
        if results:
            return results
        else:
            print("No users found")
            return []
            

    # get player AUTH
    def get_player(self, username):
        
        
        query = 'SELECT * FROM player WHERE id = %s;'
        
        print("Attempting fetch user {}", username)
        
        cursor.execute(query, (username,))
        
        # Fetch one record and return it
        result = cursor.fetchone()
    
        # Check if a result was found
        if result:
            print(f"Fetching user {username}")
            return result
        else:
            print(f"No user found with username {username}")
            return None
 
 
    # update player_sec post AUTH
    
    # update player_upd put AUTH
    
    # init start inventory post AUTH
    def init_player_inventory_start():
    
        return
    
    # init save inventory put AUTH
    
    # get player inventorys post AUTH
    def get_player_inventory(self, username):
    
        return
    
    # update inventory  post AUTH
    def update_player_inventory(self, username):
        
        
        query = 'UPDATE player_inventory WHERE id = %s;'
        
        print("Attempting fetch user {}", username)
        
        cursor.execute(query, (username,))
        
        # Fetch one record and return it
        result = cursor.fetchone()
    
        # Check if a result was found
        if result:
            print(f"Fetching user {username}")
            return result
        else:
            print(f"No user found with username {username}")
            return None
    
    
    # init start items
    def init_player_items_start(self, player_id):
        query = '''
            INSERT INTO player_items (player_id, balance, mtx_coins, casino_chips, token_spins, lemons, limes, shiny_lemons, shiny_limes, sugar, salts, honey, water, sodas, milk, alcohol, ice, heating, cups, tea, coffee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        default_values = (player_id, 20, 0, 0, 0, 18, 0, 0, 9, 0, 0, 20, 0, 0, 0, 0, 0, 10, 0, 0, 0)

        try:
            # Assuming you have a database connection and cursor, execute the query like this:
            cursor.execute(query, default_values)

            # Commit the changes to the database
            db_connection.commit()

            print(f"Player items initialized successfully for player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error initializing player items for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

    # Example usage:
    # init_player_items_start(1)

        
    # init save items
    def init_player_items_save():
    # open save file..
    # check save file for player
    
        return
        
    # get items
    def get_player_items(self, player_id):
        query = '''
            SELECT * FROM player_items
            WHERE player_id = %s;
        '''

        try:
            # Assuming you have a database connection and cursor, execute the query like this:
            cursor.execute(query, (player_id,))

            # Fetch all records
            results = cursor.fetchall()

            if results:
                # You can return the first result if you expect only one record, or return all results as a list
                return results[0]
            else:
                print(f"No player items found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching player items for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

    # Example usage:
    # player_items = get_player_items(1)
    # print(player_items)

    
    # update items put AUTH
    # 
    #  notes::
    #   - specific update_player_items: update_customer_buy, update_player_buy, ...
    def update_player_items(self, player_id, balance, mtx_coins, casino_chips, token_spins, lemons, limes, shiny_lemons, shiny_limes, sugar, salts, honey, water, sodas, milk, alcohol, ice, heating, cups, tea, coffee):
        query = '''
            UPDATE player_items
            SET
                balance = %s,
                mtx_coins = %s,
                casino_chips = %s,
                token_spins = %s,
                lemons = %s,
                limes = %s,
                shiny_lemons = %s,
                shiny_limes = %s,
                sugar = %s,
                salts = %s,
                honey = %s,
                water = %s,
                sodas = %s,
                milk = %s,
                alcohol = %s,
                ice = %s,
                heating = %s,
                cups = %s,
                tea = %s,
                coffee = %s
            WHERE player_id = %s;
        '''

        print(f"Updating player inventory for player ID {player_id}")
        
        try:
            # Assuming you have a database connection and cursor, execute the query like this:
            cursor.execute(query, (balance, mtx_coins, casino_chips, token_spins, lemons, limes, shiny_lemons, shiny_limes, sugar, salts, honey, water, sodas, milk, alcohol, ice, heating, cups, tea, coffee, player_id))

            # Commit the changes to the database
            db_connection.commit()

            print(f"Player inventory updated successfully for player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error updating player inventory for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db_connection.close()

    # Example usage:
    # update_player_items(1, 1000, 500, 200, 50, 10, 20, 5, 10, 50, 30, 15, 200, 100, 50, 10, 5, 2, 1, 100, 50, 30)
        
    
    
    # init start m2m items
    # init save m2m items
    # get items 
    # update items post AUTH
    
    # more items m2m
    # recipes
        # player_id recipe 1, pricing 1, cost?, active, chosen, name, 
        # player_id recipe 2 
        # player_id recipe 3
        # player_id recipe 4
    
    # weather
    # sales
    
    
    
       
       
       
       
       
       
       
       
       
       