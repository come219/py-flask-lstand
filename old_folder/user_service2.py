'''
user_service.py

    used to provide user service api
    uses mysql db and flask.

'''

'''

    standard imports:
        - flask
        - marshmallow
'''
from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
import MySQLdb
import datetime
import json

import logging

'''

    core imports
    

'''
from firebase_handler import FirebaseHandler
#from mysql_handler import MySQLHandler  # Import the MySQLHandler class
#from flask_mysqldb import MySQL  


app = Flask(__name__)



db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="1337",  # your password
                     db="lstand_db_2")        # name of the data base


# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set the desired logging level
logger = logging.getLogger(__name__)  

class UserService:
    '''
    UserService class
    
    should provide user, player, actor uses action to create, sign-in,
    
    potentially move unrelated direct user services to separate file?
        - recipe, inventory, items, day, streak
        - keep security, update, init, etc 
    
    features:
        - sign-in
        - log-in
        - init user functions (inventory, recipe, ...)
        
    
    '''
    
    def __init__(self, app):
        """
        Initialize a new instance of the class.

        :param app: The Flask application instance.
        :type app: Flask
        """
        self.app = app

    def get_connection(self):
        return mysql.connection

    def __del__(self):
        #self.cursor.close()
        #self.connection.close()
        #db.close()
        pass


    ##################
    #
    #   player_avatar - player_avatar table ?? player_id, avatar_id
    #
    #   player_avatar_unlocked table
    #
    #   id, avatar_id, border_id
    #
    ###########
    
    # def init_player_avatar
    
    def init_player_avatar_start(self, player_id):
        """
        Initialize the starting avatar for the player
        using player_id.
        
        To be called in player create.
        """
    
        cur = db.cursor()
        
        
        insert_sql = """
            INSERT INTO player_avatar (player_id, avatar_id, profile_border_id)
            VALUES (%s, 0, 0);
        """
        
        
        try:
            cur.execute(insert_sql, (player_id,))
            #player_id = cur.lastrowid   # Obtain the player_id for the specified username
            db.commit()
            print(f"Starting items initialized for player ID {player_id}")
        except Exception as e:
            # Rollback in case there is any error
            raise Exception(f"An error occurred while initializing starting avatar for player ID {player_id}: {e}")
        finally:
            cur.close()
            
        
    # def player_avatar_change_avatar
    # def player_avatar_change_border
    
    # def player_avatar_check_border # check member expiry to change border
    
    # def get_player_avatar_player_id
  
    # def get_player_avatar_player_username
  
    def post_player_avatar_by_id(self, player_id):
        """
        Retrieve player avatars by player_id.
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
    
    
    ####
    #
    # item - service
    #
    ##
    @staticmethod
    def get_item_id(item_name):
        """
        Given an item name, retrieve the corresponding item_id from the database.
        This function needs to be implemented based on your specific database schema.
        """
        try:
            # Create a cursor
            # cursor = db.cursor(dictionary=True)
            cursor = db.cursor()

            # Execute the SQL query to fetch the item_id based on the item_name
            query = 'SELECT id FROM item WHERE name = %s'
            cursor.execute(query, (item_name,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor and database connection
            #cursor.close()
            #db.close()
            # prevent from affecting closing other method

            # Return the item_id if found, otherwise return None
            return result[0] if result else None # Access id using its index in the tuple

        except Exception as e:
            printf(f"Error fetching item_id for item name {item_name}: {e}")
            return None

    
    
    
    #####################
    # Player table - fields
    ##################
    
    
    
    ##################
    #
    #   player_membership
    #   - bool memberships(state)
    #   - string membership_status
    #   - timestamp membership_expiry
    #
    #   notes:
    #   - string state_members, 
    #   - timestamp time_members, membership/length
    #
    #
    ###########
    
    def get_player_membership_bool(self, _id):
        '''
        Retrieves player's membership boolean variable
        - false: normal user
        - true: member user
        
        
        Implement try-catch
        '''
        query = 'SELECT player.player_membership FROM player WHERE id = %s;'
        
        cur = db.cursor()
        cur.execute(query, (_id,))
        db.commit()
        
        results = cur.fetchone()  # Fetch the first record

        if results is not None:
            print(f"Fetching player_membership from Player {_id}")
            return results[0]  # Return the player_membership
        else:
            print("No user result found")
            return None
    
    
    def get_player_membership_status():
        '''
        get the membership_status string
        0 - never member ( normal user )
        1 - member user
        3 - ex-member user
        4 - bond user
        5 - tier member ?
        9 - super user ?
        ???
        '''
    
    #def change_player_membership_status()
    
    #def update_player_membership_timer
    
    #
    
    def get_player_membership_timer(self, _id):
        '''
        get_player_membership_timer function -> timer ->> expiry?
        
        Retrieves player's membership_expiry variable field.
        
        This data, player_membership_expiry, contains the player's 
        last and/or next time (timestamp) of the player's membership.
        
        
        notes:
        
        - returns null, if never member -> normal_user
        - returns new timer -> member
        - returns old timer -> ex-member
        
        
        
        '''
        query = 'SELECT player.player_membership_expiry FROM player WHERE id = %s;'
        
        cur = db.cursor()
        cur.execute(query, (_id,))
        db.commit()
        
        results = cur.fetchone()  # Fetch the first record

        if results is not None:
            print(f"Fetching player_membership_expiry from Player {_id}")
            return results[0]  # Return the player_membership
        else:
            print("No user result found")
            return None
    
    
    
    ##################
    #
    #   player_streak
    #
    #   user calls get_streak_counter
    #   streak_check should be called as well
    #       - call increaseStreakTimer
    #       - call resetStreakTimer -> check streakFreeze, save streakTimer
    #       - return StreakTimer
    #
    ###########
        
    
    def get_streak_counter(self, _id):
        '''
        function that is called by api
        
        notes:
        
        -   removed: db.commit()
        
        -   added try-catch
        
        
        
        cur.execute(query, (_id,))
        db.commit()
        
        results = cur.fetchone()  # Fetch the first record

        if results is not None:
            print(f"Fetching player_streak from Player {_id}")
            return results[0]  # Return the player_streak
        else:
            print("No user result found")
            return None
        cur.close()
        
        '''
        cur = db.cursor()
        
        query = 'SELECT player_streak FROM player WHERE id = %s;'
        
        
        try:
            # Execute the query
            cur.execute(query, (_id,))

            # Fetch all records
            results = cur.fetchone() 
            
            if results:
                # Return all results as a list
                print(f"Fetching player_streak from Player {_id}")
                return results[0]
            else:
                print(f"No streak found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching streak item for player ID {player_id}: {e}")

        finally:
            # cur.fetchall()
            cur.close()
            
        
    
    def check_streak_timer():
        '''
        this is either called during sign-in or called after required action
        # check current time
        # check streak time
        # check if current time - streak time > 24 hours
        # if true -> increase_streak_value
        # else -> nothing
        
        '''
        # Get the current time
        current_time = datetime.datetime.now()

        # Fetch the player's streak timer from the database
        cur = db.cursor()
        cur.execute('SELECT player_streak_timer FROM player WHERE id = %s;', (_id,))
        db.commit()
        result = cur.fetchone()

        if result is None:
            print(f"No player found with id {_id}")
            return None

        streak_time = result[0]

        # Check if current time - streak time > 24 hours
        time_difference = current_time - streak_time
        if time_difference.total_seconds() > 24 * 60 * 60:  # 24 hours in seconds
            # If true, increase the streak value
            cur.execute('UPDATE player SET player_streak = player_streak + 1 WHERE id = %s;', (_id,))
            db.commit()
            print(f"Increased player_streak for Player {_id}")
        else:
            print("Streak timer has not passed 24 hours yet")

        return None
      
    
    def increase_streak_value():
        '''
        called to request increase in streak value.
        '''
        pass
        
    def save_streak_timer():
        pass
        
        
    ##################
    #
    #   player_days
    #
    ###########
    
    #def increase_day_counter_quarter(self, _id):
    
    #def increase_day_counter_half(self, _id):
        
    def increase_day_counter(self, _id):
        '''
        called during specific events in game to increase player's days.
        
        notes:
        
        - needs try-catch statement
        '''
        # First, fetch the current player_days
        cur = db.cursor()
        cur.execute('SELECT player_days FROM player WHERE id = %s;', (_id,))
        result = cur.fetchone()
        
        if result is None:
            print(f"No player found with id {_id}")
            return None
        
        current_days = result[0]
        
        # Then, increment player_days by 1
        new_days = current_days + 1
        
        # Finally, update the player_days in the database
        cur.execute('UPDATE player SET player_days = %s WHERE id = %s;', (new_days, _id))
        db.commit()
        
        print(f"Increased player_days for Player {_id} to {new_days}")
        return new_days

    
    def get_day_counter_OLD(self, _id):
        '''
        retrieves player_days by id
        
        notes:
        
        - needs try-catch statement
        - cur.close
        
        '''
    
        query = 'SELECT player_days FROM player WHERE id = %s;'
        
        cur = db.cursor()
        cur.execute(query, (_id,))
        db.commit()
        
        results = cur.fetchone()  # Fetch the first record

        if results is not None:
            print(f"Fetching player_days from Player {_id}")
            return results[0]  # Return the player_days
        else:
            print("No user result found")
            return None
            
    def get_day_counter(self, _id):
        '''
        retrieves player_days by id
        
        notes:
        
        - needs try-catch statement
        - cur.close
        
        '''
    
        query = 'SELECT player_days FROM player WHERE id = %s;'
    
        try:
            with db.cursor() as cur:
                cur.execute(query, (_id,))
                db.commit()
                
                results = cur.fetchone()  # Fetch the first record

                if results is not None:
                    print(f"Fetching player_days from Player {_id}")
                    return results[0]  # Return the player_days
                else:
                    print("No user result found")
                    return None
        
        except pymysql.Error as e:
            # Handle MySQL database-related exceptions
            print(f"Error fetching player_days for Player {_id}: {e}")
            return None
        
        finally:
            # Close the cursor
            cur.close()
        
        
    def get_player_lives(self, _id):
        '''
        retrieves player_lives by id
        
        '''
    
        query = 'SELECT player_lives FROM player WHERE id = %s;'
        
        cur = db.cursor()
        cur.execute(query, (_id,))
        db.commit()
        
        results = cur.fetchone()  # Fetch the first record

        if results is not None:
            print(f"Fetching player_lives from Player {_id}")
            return results[0]  # Return the player_lives
        else:
            print("No user result found")
            return None
            
            
    # increase player lifes
    
    # decrease player lives
    
    # effect player lives status
    # get player lives status
        
    
    
    def calc_main_level():
    #selects quest lvl, certain levels    adds them
        pass
    
    def calc_total_level():
    #selects levels adds them
        pass
        
    def calc_total_xp():
    #calc levels xp adds them
        pass
        
    def calc_quest_points():
    # selects completed quests and their value      adds them
        pass
        
    def calc_quest_level():
    # selects quest completed by num
        pass
    
    
   
    def register_firebase_player():
        pass
        
    # register player?
        
    
    
    ####
    # OLD NOTES
    #
    # player_members:: player_id, members_status, membership_expiry, membership_timer, 
    #
    ####
    
    # post_player_membership_status
    # post_player_membership_expiry
    # post_player_membership_timer
    
  
    ########################
    #
    # player::  ... lives_status_effect,    
    #
    ########################
  
  
    def create_player(self, email, username, password, first_name, last_name, dob):
        '''
        notes:
            - need to init membership time so that its not null 
            - need to implement standard init time so that can see if not null 1,1,1999
            - need to implement init profile avatar + profile border
            - implement player_mana
        
        old notes:
            - need to implement player_membership, among other
        '''
        cur = db.cursor()
        
       
        query_OLD = '''
            INSERT INTO player (
                player_days, player_lives, player_streak, player_streak_timer,
                player_networth, player_location, player_offers_notifications,
                player_trade_requests, player_inbox_messages, player_private, player_hide,
                main_level, total_level, total_xp, quest_points, quest_level
            )
            VALUES (
                0, -- player_days
                10, -- player_lives
                0, -- player_streak
                CURRENT_TIMESTAMP, -- player_streak_timer
                0, -- player_networth
                '', -- player_location
                0, -- player_offers_notifications
                0, -- player_trade_requests
                0, -- player_inbox_messages
                0, -- player_private
                0, -- player_hide
                0, -- main_level
                0, -- total_level
                0, -- total_xp
                0, -- quest_points
                0 -- quest_level
                -- NULL -- new_column, assuming it allows NULL values
            );
        '''

        query_OLD = '''
        INSERT INTO player (
                player_days, player_lives, player_lives_status, player_streak, player_streak_timer,
                player_networth, player_location, player_offers_notifications,
                player_trade_requests, player_inbox_messages, player_private, player_hide,
                main_level, total_level, total_xp, quest_points, quest_level,
                player_membership, player_membership_expiry, player_membership_status
            )
            VALUES (
                0, -- player_days
                10, -- player_lives
                '', -- player_lives_status
                0, -- player_streak
                CURRENT_TIMESTAMP, -- player_streak_timer
                0, -- player_networth
                '', -- player_location
                0, -- player_offers_notifications
                0, -- player_trade_requests
                0, -- player_inbox_messages
                0, -- player_private
                0, -- player_hide
                0, -- main_level
                0, -- total_level
                0, -- total_xp
                0, -- quest_points
                0, -- quest_level
                0, -- player_membership
                NULL, -- player_membership_expiry
                '' -- player_membership_status
            );
        '''
        
        
        
        query = '''
        INSERT INTO player (
                player_days, player_lives, player_lives_status, player_streak, player_streak_timer,
                player_networth, player_location, player_offers_notifications,
                player_trade_requests, player_inbox_messages, player_private, player_hide,
                main_level, total_level, total_xp, quest_points, quest_level,
                player_membership, player_membership_expiry, player_membership_status
            )
            VALUES (
                0, -- player_days
                10, -- player_lives
                '', -- player_lives_status
                0, -- player_streak
                CURRENT_TIMESTAMP, -- player_streak_timer
                0, -- player_networth
                '', -- player_location
                0, -- player_offers_notifications
                0, -- player_trade_requests
                0, -- player_inbox_messages
                0, -- player_private
                0, -- player_hide
                0, -- main_level
                0, -- total_level
                0, -- total_xp
                0, -- quest_points
                0, -- quest_level
                0, -- player_membership
                STR_TO_DATE('1,1,1999', '%m,%d,%Y'), -- Default membership expiry (1st January 1999)
                '' -- player_membership_status
            );
        '''


        try:
            # player -> player_security
            cur.execute(query)
            player_id = cur.lastrowid
            db.commit()

            print("Player created success... security check")
            security_query = '''
                INSERT INTO player_security (
                    player_id, email, verified_email, username, password,
                    password_reset_token, password_reset_expire, player_hide_code,
                    first_name, last_name, dob, user_creation_date, user_last_login,
                    user_login_attempts, account_locked, account_locked_reason
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s
                );
            '''
            cur.execute(security_query, (player_id, email, 0, username, password, None, None, None, first_name, last_name, dob, None, 0, 0, None))
            db.commit()
           
            print(f"Player {player_id} fully created successfully")
            return player_id
           

        except Exception as e:
            # Handle the exception
            print(f"Error creating player: {e}")

        finally:
            #cur.fetchall()
            # Close the cursor and database connection
            cur.close()
            print("finally reached")
            return player_id

    # Example usage:
    # user_service.create_player(email, username, password, first_name, last_name, dob)

    
    def get_player_by_id():
        pass
    
    def get_player_by_user():
        pass
        
        
    def get_player_email_by_id(self, player_id):
        '''
        Retrieves player email by player_id from the player_security table
        
        Parameters:
        - player_id: ID of the player
        
        Returns:
        - Player's email if found, None otherwise
        
        
        implement try-catch statement
        '''
        query = 'SELECT email FROM player_security WHERE player_id = %s;'

        cur = db.cursor()
        cur.execute(query, (player_id,))
        db.commit()

        result = cur.fetchone()  # Fetch the first record

        if result is not None:
            print(f"Fetching email from Player ID {player_id}")
            return result[0]  # Return the player's email
        else:
            print(f"No email found for Player ID {player_id}")
            return None

    
    
    def get_player_id_by_username(self, username):
        '''
        Retrieves player ID by username from the player table
        
        Parameters:
        - username: Username of the player
        
        Returns:
        - Player's ID if found, None otherwise
        
        implement try-catch statment
        '''
        query = 'SELECT id FROM player WHERE username = %s;'

        cur = db.cursor()
        cur.execute(query, (username,))
        db.commit()

        result = cur.fetchone()  # Fetch the first record

        if result is not None:
            print(f"Fetching ID for username: {username}")
            return result[0]  # Return the player ID
        else:
            print(f"No ID found for username: {username}")
            return None

    
    def get_player_username(self, player_id):
        '''
        Retrieves player username by player_id from player_security table
        
        Parameters:
        - player_id: ID of the player
        
        Returns:
        - Player's username if found, None otherwise
        '''
        query = 'SELECT username FROM player_security WHERE player_id = %s;'

        try:
            cur = db.cursor()
            cur.execute(query, (player_id,))
            db.commit()

            result = cur.fetchone()  # Fetch the first record

            if result is not None:
                print(f"Fetching username from Player {player_id}")
                return result[0]  # Return the username
            else:
                print("No username found")
                return None
        except Exception as e:
            print(f"An error occurred while fetching username for Player {player_id}: {e}")
            return None
        finally:
            cur.close()


    

    
    

    def init_player(self, _id):
        """
        init player start (?)
        
        calls: player_update, player_items, player_inventory
        
        player_mana
        
        
        """
        
        print("init player attempt")
        
        cur = db.cursor()
        
        update_query = """
                INSERT INTO player_update (
                    player_id, action_id, user_location, user_last_update,
                    user_uptime, user_playtime, user_last_logout, connected,
                    player_ip, player_irl_location, player_os, player_current_region,
                    player_home_region, player_pref_region
                )
                SELECT id, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL
                FROM player
                WHERE id = %s
            """
         
        
        try:
            # Insert a new record into the 'player_update' table with default or NULL values
            print(f"Executing update query for player ID: {_id}")
            cur.execute(update_query, (_id,))
            
            db.commit()
            
            # player_id = cur.lastrowid   # Obtain the player_id for the specified username
            player_id = _id

            # Call functions to initialize player items, levels, inventory 
            self.init_player_items_start(player_id)
            self.init_player_levels_start(player_id)
            self.init_player_inventory_start(player_id)
            self.init_player_recipes_start(player_id)
            #init weather
            self.init_player_avatar_start(player_id)
      

            print(f"Player {player_id} initialized successfully with player ID")

        except Exception as e:
            if e.args[0] == 2006:  # MySQL server has gone away
                # Attempt to reconnect to the database
                print("Attempting to reconnect to the database...")
                db.reconnect(attempts=3, delay=5)  # Adjust the number of attempts and delay as needed
                # Retry the transaction
                self.init_player(player_id)
            else:
                # Handle other exceptions
                print(f"Error creating player: {e}")
                # Handle the exception
                print(f"Error initializing player {username} || id: {player_id}: {e}")
            
            

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()

    # Example usage:
    # init_player('example_username')


    
    
    # init player from save
    def init_player_from_save():
        '''
        when new table
        '''
        pass
    
    
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
 
 
    ##################
    #
    #  security 
    #
    #################
    
    # post_player_verify ?
    
    # post_user_request_change_password
    
    # post_user_change_password
    
    # post_user_change_dob
    
    # post_user_change_name
    
    
 
    # update player_sec post AUTH
    
    # post_auth_player
    
    
    
    ####################
    #
    #  update
    #
    ####################
    
    # def hop world
    
    def post_user_signin():
    # get user, pass
    # check
    # should return id
        pass
    
    def post_player_signin():
    
    # insert into player_update where id = %s connected = true
    
    # val = select player_count from server_info 
    # insert into server_info (player_count) +1 + val
    
        print("player {id} sign in")
        pass
    
    def post_player_signout():
    # insert into player_update where id = %s connected = false
    
    # val = select player_count from server_info 
    # insert into server_info (player_count) -1 + val
    
        print("player {id} sign out")
        pass
    
    
    # post_player_add_playtime
    
    # post_player_add_uptime
    
    
    
    # post_player_update()
    
    # post_player_region_change()
    
    
    # update player_upd put AUTH
    
    
    #################
    #
    #    inventory (shifter_id, chosen_shifter, stall, perks, equipment, summoning?)
    #
    #################
    
    # init start inventory post AUTH
    def init_player_inventory_start(self, player_id):
        print("player inventory init not yet implemented")
        #print("player inventory table not fully designed")
        pass
    
    # init save inventory put AUTH
    
    # get player inventorys post AUTH
    def get_player_inventory(self, username):
        print("player inventory get not yet implemented")
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
    
    
    
    ######################
    #
    #       LEVELS:
    #
    #####################
    def get_player_levels_by_id():
    
        pass
        
        
    def post_player_levels_by_id(self, player_id):
        cur = db.cursor()
        query = '''
            SELECT player_id, level_id, current_level, achieved_level, xp_level
            FROM player_levels
            WHERE player_id = %s;
        '''
        
        query = '''
            SELECT player_levels.player_id, player_levels.level_id, levels.name, player_levels.current_level, player_levels.achieved_level, player_levels.xp_level
            FROM player_levels
            JOIN levels ON player_levels.level_id = levels.id
            WHERE player_levels.player_id = %s;
        '''
    
        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchall()

            if results:
                # Return all results as a list
                return results
            else:
                print(f"No player levels found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching player levels for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()

        
    # def get specific current_level player_level by id
    
    def init_player_levels_start(self, player_id):
        '''
        Instantiate the player levels starting levels upon
        user creation. Gives the player each level at 1.
        '''
        
        
        
        insert_sql = '''
        INSERT INTO player_levels (player_id, level_id, current_level, achieved_level, xp_level)
        SELECT %s, i.id, 
            CASE 
                WHEN i.name = 'campaign' THEN 1
                WHEN i.name = 'openworld' THEN 1
                WHEN i.name = 'endday' THEN 1
                WHEN i.name = 'trading' THEN 1
                WHEN i.name = 'farming' THEN 1
                WHEN i.name = 'fishing' THEN 1
                WHEN i.name = 'mining' THEN 1
                WHEN i.name = 'crafting' THEN 1
                WHEN i.name = 'casino' THEN 1
                WHEN i.name = 'fire' THEN 1
                WHEN i.name = 'pool' THEN 1
                WHEN i.name = 'magic' THEN 1
                WHEN i.name = 'slayer' THEN 1
                WHEN i.name = 'dungeon' THEN 1
                WHEN i.name = 'rpg' THEN 1
                WHEN i.name = 'combat' THEN 1
                WHEN i.name = 'agility' THEN 1
                WHEN i.name = 'summoning' THEN 1
                WHEN i.name = 'charisma' THEN 1
                ELSE 1
            END,
            1,
            0
        FROM levels i;
        '''
        
        
        # try catch
        print(f"init player levels Player {player_id}")
        try:
            cur = db.cursor()
            cur.execute(insert_sql, (player_id,))
            db.commit()
            print(f"Player levels initialized successfully for Player ID: {player_id}")
        except Exception as e:
            print(f"Error initializing player levels for Player ID: {player_id}: {e}")
        finally:
            cur.fetchall()
            print("finally player levels")
            cur.close()
        
        pass
        
    def init_player_levels_save(self, player_id):
        pass
    
    def post_level_increase(self, player_id, level_id):
        '''
        call current lvl increase, total lvl increase
        '''
 
        cur = db.cursor()
        query = '''
            UPDATE player_levels
            SET current_level = current_level + 1, 
                achieved_level = CASE WHEN current_level + 1 > achieved_level THEN current_level + 1 ELSE achieved_level END
            WHERE player_id = %s AND level_id = %s;
        '''

        try:
            # Execute the query
            cur.execute(query, (player_id, level_id))

            # Commit the transaction
            db.commit()

            print(f"Level increased successfully for Player ID: {player_id}, Level ID: {level_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error increasing level for Player ID: {player_id}, Level ID: {level_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()

    
    def post_level_xp_increase(self, player_id, level_id, num_xp):
        cur = db.cursor()
        query = '''
            UPDATE player_levels
            SET xp_level = xp_level + %s
            WHERE player_id = %s AND level_id = %s;
        '''

        try:
            # Execute the query
            cur.execute(query, (num_xp, player_id, level_id))

            # Commit the transaction
            db.commit()

            print(f"XP increased successfully for Player ID: {player_id}, Level ID: {level_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error increasing XP for Player ID: {player_id}, Level ID: {level_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()

    
    def post_current_level_increase(self, player_id, level_id):
    #increase current level
        pass
        
    def post_current_level_decrease(self, player_id, level_id):
    # decrease current level
        pass
        
    def post_current_level_reset():
    # checks total level difference with current level
    # check difference + 1 or - 1
        pass
    
    ######################
    #
    #       ITEMS:
    #
    #####################
    
    def post_player_items_update():
        pass
    
    def post_player_items_increase():
        pass
        
    def post_player_items_decrease():
        pass
        
    def post_player_balance_sell():
        pass
        
    def post_player_balance_buy():
        pass
        
    def post_player_item_obtain():
        pass
        
    def post_player_item_ingredients():
        pass
    
    def post_player_item_use():
        pass
    
    def post_player_item_purchase():
        pass
        
    def post_player_item_sell():
        pass  
    
    def post_player_items_buy_item(self, player_id, item_id, balance_minus, item_quantity):
        '''
        post_player_items_buy_item
        player purchase item from shop/else by function
        '''
        balance_minus = int(balance_minus)
        #double??

        # Get the player's current balance
        balance = self.get_player_items_balance(player_id)
        if balance is None:
            print(f"Player ID {player_id} does not have a Balance item.")
            return

        # Check if the player has enough balance to buy the item
        if balance[0][3] < balance_minus:
            print(f"Player ID {player_id} does not have enough balance to buy the item.")
            return

        # Deduct the cost of the item from the player's balance
        # IF <currencies> moved, 'UPDATE player ...'
        new_balance = balance[0][3] - balance_minus
        query = '''
            UPDATE player_items
            SET quantity = %s
            WHERE player_id = %s AND item_id = %s;
        '''
        cur = db.cursor()
        try:
            cur.execute(query, (new_balance, player_id, balance[0][1]))
            db.commit()
        except Exception as e:
            print(f"Error updating Balance item for player ID {player_id}: {e}")
            return

        # Add the purchased item to the player's items
        query = '''
            INSERT INTO player_items (player_id, item_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + %s;
        '''
        try:
            cur.execute(query, (player_id, item_id, item_quantity, item_quantity))
            db.commit()
        except Exception as e:
            print(f"Error buying item for player ID {player_id}: {e}")
            return

        print(f"Player ID {player_id} successfully bought {item_quantity} of item ID {item_id}.")

    
    #  MAJOR CHANGES TO BALANCE IF <currencies> moved
    def get_player_items_balance(self, player_id):
        '''
        Error fetching Balance item for player ID 25: (2014, "Commands out of sync; you can't run this command now")
        '''
        cur = db.cursor()
        query = '''
            SELECT player_items.player_id, player_items.item_id, item.name, player_items.quantity
            FROM player_items
            JOIN item ON player_items.item_id = item.id
            WHERE player_items.player_id = %s AND item.name = 'Balance';
        '''

        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchall()
            #results = cur.fetchone()

            if results:
                # Return all results as a list
                return results
            else:
                print(f"No Balance item found for player ID {player_id}")
                logger.info(f"No Balance item found for player ID {player_id}")
                return None

        except pymysql.Error as e:
            if isinstance(e, pymysql.MySQLError):
                # Handle MySQL database-related exceptions
                logger.error(f"MySQL Error fetching Balance item for player ID {player_id}: {e}")
            elif isinstance(e, pymysql.IntegrityError):
                # Handle integrity constraint violations
                logger.error(f"Integrity Error fetching Balance item for player ID {player_id}: {e}")
            else:
                # Handle other pymysql errors
                logger.error(f"Error fetching Balance item for player ID {player_id}: {e}")

        except Exception as e:
            # Handle the exception
            print(f"Error fetching Balance item for player ID {player_id}: {e}")

        finally:
            # consume
            try:
                cur.fetchall()
            except pymysql.Error as e:
                pass  # Ignore any errors during result consumption

            # Close the cursor and database connection
            cur.close()
            #db.close()

        
        
    def get_player_items_mtx_coins(self, player_id):
        cur = db.cursor()
        query = '''
            SELECT player_items.player_id, player_items.item_id, item.name, player_items.quantity
            FROM player_items
            JOIN item ON player_items.item_id = item.id
            WHERE player_items.player_id = %s AND item.name = 'MTX Coins';
        '''

        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchall()

            if results:
                # Return all results as a list
                return results
            else:
                print(f"No mtx coin item found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching mtx coin item for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()
    
    def get_player_items_by_id():
    
    # get player_items using player_id
        pass
        
        
    # def get 1 specific item 
        
        
    def post_player_items_by_id(self, player_id):
        '''
        Retrieves all player items using item id
        
        problems: 
            -   192.168.1.36 - - [26/Dec/2023 23:04:49] "POST /api/players/username HTTP/1.1" 500 -
                Error fetching player items for player ID 25: (2014, "Commands out of sync; you can't run this command now")
                
                fetchall?
        '''
        cur = db.cursor()
        query = '''
            SELECT * FROM player_items
            WHERE player_id = %s;
        '''
        query = '''
            SELECT player_items.*, item.name 
            FROM player_items
            JOIN item ON player_items.item_id = item.id
            WHERE player_id = %s;
        '''

        try:
            # Assuming you have a database connection and cursor, execute the query like this:
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchall()

            if results:
                # You can return the first result if you expect only one record, or return all results as a list
                return results
            else:
                print(f"No player items found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching player items for player ID {player_id}: {e}")

        finally:
            # Consume the result set to avoid "Commands out of sync" error
            cur.fetchall()
            # Close the cursor and database connection
            cur.close()
            #db.close()
    
    
        pass
        
    
    old_init_player_items_start_query = '''
            INSERT INTO player_items (player_id, balance, mtx_coins, casino_chips, token_spins, lemons, limes, shiny_lemons, shiny_limes, sugar, salts, honey, water, sodas, milk, alcohol, ice, heating, cups, tea, coffee)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
    

    def init_player_items_start(self, player_id):
        """
        Initialize the starting items for a new player in the game.

        This method populates the 'player_items' table with default item quantities for a given player.
        It sets the quantity of each item to 0, indicating that the player starts without any items.

        :param player_id: The unique identifier of the player.
        :type player_id: int
        :raises Exception: If there is an issue with the database operation.
        :returns: None

        The method executes an SQL INSERT statement to create records for each item in the 'item' table,
        associating them with the specified player ID and setting the initial quantity to 0.
        If an error occurs during the database operation, it raises an exception with the error details.
        
        
        notes:
        - should init with 1 mg of salt?
        - no given honey, no salt
        
        - this would be changed if <currencies> are moved into player table.
        """
    
        cur = db.cursor()
       
        
        insert_sql_old = """
        INSERT INTO player_items (player_id, item_id, quantity, total_use, current_use)
        SELECT %s, i.id, 
            CASE 
                WHEN i.name = 'Balance' THEN 20
                WHEN i.name = 'MTX Coins' THEN 0
                WHEN i.name = 'Casino Chips' THEN 0
                WHEN i.name = 'Token Spins' THEN 0
                WHEN i.name = 'Lemons' THEN 9
                WHEN i.name = 'Sugar' THEN 6
                WHEN i.name = 'Water' THEN 20
                WHEN i.name = 'Cups' THEN 12
                ELSE 0
            END,
            0,
            0
        FROM item i;
        """
        
        
        insert_sql = """
        INSERT INTO player_items (player_id, item_id, quantity)
        SELECT %s, i.id, 
            CASE 
                WHEN i.name = 'Balance' THEN 20
                WHEN i.name = 'MTX Coins' THEN 0
                WHEN i.name = 'Casino Chips' THEN 0
                WHEN i.name = 'Token Spins' THEN 0
                WHEN i.name = 'Lemons' THEN 9
                WHEN i.name = 'Sugar' THEN 6
                WHEN i.name = 'Water' THEN 20
                WHEN i.name = 'Cups' THEN 12
                ELSE 0
            END
        FROM item i;
        """
        
        
        try:
            cur.execute(insert_sql, (player_id,))
            #player_id = cur.lastrowid   # Obtain the player_id for the specified username
            db.commit()
            print(f"Starting items initialized for player ID {player_id}")
        except Exception as e:
            # Rollback in case there is any error
            # db_connection.roll
            raise Exception(f"An error occurred while initializing starting items for player ID {player_id}: {e}")
        finally:
            # Close the cursor
            #db.close()
            #cur.fetchall()
            cur.close()
            print("finally items")
        

       

        
    # init save items
    def init_player_items_save():
    # open save file..
    # check save file for player
    
        return
        
   
    def get_player_items(self, player_id):
        '''
        get player_items function
        get items
        
        checked for errors [ o ]
        
        '''
        
        
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
    #   - old impl.
    #   - VERY OLD IMPL!!!
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
            print(f"Error updating player items for player ID {player_id}: {e}")

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
    
    
    
    ##############
    #
    #   recipes
    #
    #
    #
    # AI nonsense:
    # This function will update the player’s recipe in the player_recipe1 table. It uses a similar structure to your post_player_items_by_id function, but the query is adjusted to insert into the player_recipe1 table instead of the player_items table. The try/except/finally block is used to handle potential exceptions and ensure the database connection is properly closed. Please replace db with your actual database connection object. Also, make sure to uncomment db.close() if you want to close the database connection after each operation. If you’re using a connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of the query, the transaction will be rolled back and no changes will be made to the database. This is why it’s important to handle exceptions and commit the transaction only when no errors have occurred. If you don’t commit the transaction, the changes won’t be saved to the database. If you’re using a database connection pool, you might not want to close the connection here. Instead, you would return it to the pool. Please adjust the code according to your specific requirements. Remember to call db.commit() after the execute statement to make sure the changes are saved to the database. If an error occurs during the execution of
    # 
    # recipes:
    #    #  recipe 1, player_id, pricing 1, cost?, active, chosen, name, 
    #    #  recipe 2  player_id
    #    #  recipe 3  player_id
    #    #  recipe 4  player_id
    #
    #
    ##############
    
    # def post_copy_recipe - copy to another/duplicate
    
    # def post_share_recipe - share json?
    
    # def post recipe rename
    # def post recipe deactivate
    # def post recipe activate
    
    # def get_player_recipe_check
    # check active recipes - call recipe active
    # check items quantity with recipe
    # return true if items quantity > 1 recipes
    # return false if less items than 1 recipe
    
    
    
    def get_player_recipe_active(self, player_id):
        '''
        
        # def get_player_recipe_active
        
        '''
        
        # for loop 1-4
        # using get_player_recipe
        
        #check which is / are active
        # and return recipe
    
    
    
    def post_player_recipes_use_pitcher(self, recipe_table, player_id):
        '''
        separate use recipe function for pitchers
        '''
    
    def post_player_recipes_use_active(self, player_id):
        '''
        use but check which active using function calls
        
        '''
        # call get active
        # call get recipe
        
        # then, use recipe
    
    # TODO : working on
    def post_player_recipes_use(self, recipe_table, player_id):
        '''
        using table param, use recipe
        
        '''
        cur = db.cursor()

        
        # Dynamic query to fetch the recipe
        query = f'''
            SELECT * FROM {recipe_table} 
            WHERE player_id = %s;
        '''
        
        # Query to check player items quantity
        query_quantity = '''
            SELECT * FROM player_items
            WHERE player_id = %s AND item_id = %s;
        '''
        
        # Query to update player items quantity after using the recipe
   
        query_use = '''
            UPDATE player_items
            SET quantity = %s
            WHERE player_id = %s AND item_id = %s;
        '''
        
        recipe_result = None
        recipe_check = False
        
        # Fetch the recipe - State 1
        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchone()

            if results:
                # using results in next state
                recipe_result = results
            else:
                print(f"No player recipe {recipe_table} found for player ID {player_id}")
                return None

        except Exception as e:
            print(f"Error fetching player recipe {recipe_table}  for player ID {player_id}: {e}")

        finally:
            # Consume the result set to avoid "Commands out of sync" error
            # using fetchone
            # cur.fetchall()
            # Close the cursor and database connection
            # cur.close() - > dont lol
            print('finally')
        
        # Use the recipe - State 2
        if recipe_result:
            print(f"Using recipe {recipe_table} :: {recipe_result}")

            # Parse recipe_result
            #ingredients_json = json.loads(recipe_result['ingredients'])
            ingredients_json = json.loads(recipe_result[-1])

            # Check if player has sufficient items for the recipe
            for category, items in ingredients_json.items():
                for item, details in items.items():
                    item_id = self.get_item_id(item)  # Define a function to get the item_id based on item name

                    # Fetch player items quantity
                    try:
                        cur.execute(query_quantity, (player_id, item_id))
                        player_item = cur.fetchone()

                        if player_item:
                            player_quantity = player_item[2]  # Access quantity using its index in the tuple
                            recipe_quantity = details['amount']

                            # Check if player has enough quantity of the item
                            if player_quantity < recipe_quantity:
                                recipe_check = True
                                break

                        else:
                            print(f"Item {item} not found for player ID {player_id}")

                    except Exception as e:
                        print(f"Error fetching player item quantity for {item} and player ID {player_id}: {e}")

            # Reduce items if all >= recipe amount
            if not recipe_check:
                try:
                    for category, items in ingredients_json.items():
                        for item, details in items.items():
                            item_id = self.get_item_id(item)
                            recipe_quantity = details['amount']

                            # Update player items quantity after using the recipe
                            if recipe_quantity != 0:
                                cur.execute(query_use, (player_quantity - recipe_quantity, player_id, item_id))

                    # Commit the transaction
                    db.commit()
                    print(f"Recipe {recipe_table} used successfully for player ID {player_id}")

                except Exception as e:
                    print(f"Error updating player items quantity after using the recipe for player ID {player_id}: {e}")
                    db.rollback()

        elif recipe_check:
            print(f"No sufficient items for {recipe_table} for player ID {player_id}")

        else:
            print(f"No result {recipe_table} for player ID {player_id}")
        
        
        # need to check if valid recipe use
        
        # also give the user the recipe profit.
        # pricing_json = json.loads(recipe_result[7])
        # cur.execute(query_use, (pricing_json, player_id, item_id))
        balance_plus = str(recipe_result[7])

        # Get the player's current balance
        balance = self.get_player_items_balance(player_id)
        if balance is None:
            print(f"Player ID {player_id} does not have a Balance item.")
            return

        # Increase the cost of the item from the player's balance
        balance_plus = float(balance_plus)
        new_balance = balance[0][3] + balance_plus
        query_new = '''
            UPDATE player_items
            SET quantity = %s
            WHERE player_id = %s AND item_id = %s;
        '''
        cur = db.cursor()
        new_balance_str = str(new_balance)
        try:
            cur.execute(query_new, (new_balance_str, player_id, balance[0][1]))
            db.commit()
            print(f"Recipe used successfully for player ID {player_id}")

        except Exception as e:
            print(f"Error updating Balance item for player ID {player_id}: {e}")
        
        finally:
            cur.close()


        # finally 
        # cur.close
        
    
    # def post_player_recipes_all_use
    # def post_player_recipes_perk_use
    
    # def post_player_recipe_default_use():
    
    
    def use_player_recipe(self, player_id):
        '''
        Unfinished, Old, Unbinded
        
        use recipe , uses active recipe
        
        post player recipe active use
        
        for loop to check for active recipes after retrieval
        
        then use the recipe against player items
        
              
        check active recipes - select
        using active, update items - update
        
        '''
        cur = db.cursor()
        
        # for loop:  for(int i = 0; i < 4; i++)
        
        index_recipe = 0
        recipe_json = ''
        
        
        query1 = '''
            SELECT * FROM player_recipe1
            WHERE player_id = %s;
        '''
        query2 = '''
            SELECT * FROM player_recipe2
            WHERE player_id = %s;
        '''
        query3 = '''
            SELECT * FROM player_recipe3
            WHERE player_id = %s;
        '''
        query4 = '''
            SELECT * FROM player_recipe4
            WHERE player_id = %s;
        '''
        
        # try catch - check for active true
        try:
            # Execute the query
            cur.execute(query1, (player_id,))

            # Fetch all records
            results = cur.fetchall()

            if results:
                # Return if active recipe
                if(results['recipes'][0] == true):
                    index_recipe = 1
                    recipe_json = results[0]
            else:
                print(f"No player recipes 1 found for player ID {player_id}")
        except Exception as e:
            print(f"Error fetching player recipes 1 for player ID {player_id}: {e}")
        finally:
            cur.fetchall()
            cur.close()
        
        
        if(index_recipe == 0):
            try:
                # Execute the query
                cur.execute(query2, (player_id,))

                # Fetch all records
                results = cur.fetchall()

                if results:
                    # Return if active recipe
                    if(results[recipes][0] == true):
                        index_recipe = 2
                else:
                    print(f"No player recipes 2 found for player ID {player_id}")
            except Exception as e:
                print(f"Error fetching player recipes 2 for player ID {player_id}: {e}")
            finally:
                cur.fetchall()
                cur.close()
                
        if(index_recipe == 0):
            try:
                # Execute the query
                cur.execute(query2, (player_id,))

                # Fetch all records
                results = cur.fetchall()

                if results:
                    # Return if active recipe
                    if(results[recipes][0] == true):
                        index_recipe = 3
                else:
                    print(f"No player recipes 3 found for player ID {player_id}")
            except Exception as e:
                print(f"Error fetching player recipes 3 for player ID {player_id}: {e}")
            finally:
                cur.fetchall()
                cur.close()
                
                
        if(index_recipe == 0):
            try:
                # Execute the query
                cur.execute(query2, (player_id,))

                # Fetch all records
                results = cur.fetchall()

                if results:
                    # Return if active recipe
                    if(results[recipes][0] == true):
                        index_recipe = 4
                else:
                    print(f"No player recipes 4 found for player ID {player_id}")
            except Exception as e:
                print(f"Error fetching player recipes 4 for player ID {player_id}: {e}")
            finally:
                cur.fetchall()
                cur.close()
                
        # using index_recipe and use recipe to use items
        #recipe_json 
        
        
        
        
            
        


 
        
    
    def init_player_recipes_start(self, player_id):
        '''
        creates recipes (default) for player in all tables.
        player_recipe1, player_recipe2, ...
        
        
        not working!!
        '''
         
        cur = db.cursor()
        
        query = '''
            INSERT INTO player_recipe1 ( 
            recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients) 
            VALUES ( 'Default Recipe', FALSE, PLAYER_ID_HERE, 'Medium', '',
            '["Cool", "Dry", "Balanced", "Mild" ]', 5.99, 'Cups',
            '{
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
                    "salt": {"amount": 0.0}
                },

                "Base": {
                    "lemons": {"amount": 3}
                },

                "Others": {
                    "tea": {"amount": 0.0}
                }
            }' );
        '''
        
        query2 = '''
            INSERT INTO player_recipe2 ( 
            recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients) 
            VALUES ( 'Default Recipe', FALSE, PLAYER_ID_HERE, 'Medium', '',
            '["Cool", "Dry", "Balanced", "Mild" ]', 5.99, 'Cups',
            '{
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
                    "salt": {"amount": 0.0}
                },

                "Base": {
                    "lemons": {"amount": 3}
                },

                "Others": {
                    "tea": {"amount": 0.0}
                }
            }' );
        '''
        
        try:
            cur.execute(query, (player_id,))
        
        except Exception as e:
            print(f"Error init player recipes for player ID {player_id}: {e}")
        finally:
            #cur.fetchall()
            cur.close()
        
        
        
        
    def get_player_recipes_all(self, player_id):
        '''
        Return all player recipes.
        
        no current uses?
        
        for loop ?
        '''
        recipe_table = ''
        
        query = f'''
            SELECT * FROM {recipe_table} 
            WHERE player_id = %s;
        '''
    
    def get_player_recipe(self, recipe_table, player_id):
        '''
        Return player recipe using recipe table
        
        '''
        query = f'''
            SELECT * FROM {recipe_table} 
            WHERE player_id = %s;
        '''
        
        cur = db.cursor()
        
        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchone()

            if results:
                return results
            else:
                printf(f"No player recipe {recipe_table} found for player ID {player_id}")
                return None

        except Exception as e:
            printf(f"Error fetching player recipe {recipe_table}  for player ID {player_id}: {e}")

        finally:
            cur.close()
        
        
    def get_player_recipe1(self, player_id):
        '''
        Retrieves player recipe1 using player id
        '''
        cur = db.cursor()
        query = '''
            SELECT * FROM player_recipe1
            WHERE player_id = %s;
        '''

        try:
            # Execute the query
            cur.execute(query, (player_id,))

            # Fetch all records
            results = cur.fetchall()

            if results:
                # Return all results as a list
                return results
            else:
                print(f"No player recipes found for player ID {player_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching player recipes for player ID {player_id}: {e}")

        finally:
            # Consume the result set to avoid "Commands out of sync" error
            cur.fetchall()
            # Close the cursor and database connection
            cur.close()
            #db.close()
            
    def get_player_recipe2(self, player_id):
        '''
        Retrieves player recipe2 using player id
        '''
        cur = db.cursor()
        query = '''
            SELECT * FROM player_recipe2
            WHERE player_id = %s;
        '''

        try:
            cur.execute(query, (player_id,))
            results = cur.fetchall()
            if results:
                return results
            else:
                print(f"No player recipes found for player ID {player_id}")
                return None
        except Exception as e:
            print(f"Error fetching player recipes for player ID {player_id}: {e}")
        finally:
            cur.fetchall()
            cur.close()
            
    def get_player_recipe3(self, player_id):
        '''
        Retrieves player recipe3 using player id
        '''
        cur = db.cursor()
        query = '''
            SELECT * FROM player_recipe3
            WHERE player_id = %s;
        '''

        try:
            cur.execute(query, (player_id,))
            results = cur.fetchall()
            if results:
                return results
            else:
                print(f"No player recipes found for player ID {player_id}")
                return None
        except Exception as e:
            print(f"Error fetching player recipes for player ID {player_id}: {e}")
        finally:
            cur.fetchall()
            cur.close()
            
    def get_player_recipe4(self, player_id):
        '''
        Retrieves player recipe4 using player id
        '''
        cur = db.cursor()
        query = '''
            SELECT * FROM player_recipe4
            WHERE player_id = %s;
        '''

        try:
            cur.execute(query, (player_id,))
            results = cur.fetchall()
            if results:
                return results
            else:
                print(f"No player recipes found for player ID {player_id}")
                return None
        except Exception as e:
            print(f"Error fetching player recipes for player ID {player_id}: {e}")
        finally:
            cur.fetchall()
            cur.close()


    def post_player_recipe_update(self, recipe_table, recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients):
        '''
        Updates player recipe using player id and other parameters
        
        
        works ??
        
        '''
        cur = db.cursor()
        
        flavour_effects_str = json.dumps(flavour_effects)
        ingredients_str = json.dumps(ingredients)
        
        query_old = f'''
            INSERT INTO {recipe_table} (recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        query_original = '''
            INSERT INTO player_recipe1 (recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        
        query = f'''
            UPDATE {recipe_table} 
            SET recipe_name = %s, recipe_active = %s, quality = %s, flavour_string = %s, flavour_effects = %s, pricing = %s, cups = %s, ingredients = %s
            WHERE player_id = %s;
        '''
        
        

        try:
            # Execute the query, player_id at the end -- WHY??, yess
            cur.execute(query, (recipe_name, recipe_active, quality, flavour_string, flavour_effects_str, pricing, cups, ingredients_str, player_id))

            # Commit the transaction
            db.commit()

            print(f"Player recipe updated for player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error updating player recipe for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()
            
            
    def post_player_recipe_default_init(self, recipe_table, player_id):
        '''
        inserts into player recipe using player id and other parameters
        
        
        
        recipe_name = 'Default Recipe'
        recipe_active = False
        quality= 'Medium'
        flavour_string =''
        flavour_effects = ["Cool", "Dry", "Balanced", "Mild"]
        pricing = 5.99 
        cups = "Cups" 
        ingredients= {
        "water": {"amount": 169.0},
        "ice": {"amount": 0.0},
        "sugar": {"amount": 0.0},
        "salts": {"amount": 0.0},
        "base": {
            "lemons": {"amount": 3}
        },
        "others": {
            "tea": {"amount": 0.0}
        }
        }
        
        
        
        [
            1,
            "Default Recipe",
            25,
            1,
            "Medium",
            "",
            "[\"Cool\", \"Dry\", \"Balanced\", \"Mild\"]",
            5.99,
            "Cups",
            "{\"Base\": {\"Lemons\": {\"amount\": 3}}, \"Salts\": {\"Salt\": {\"amount\": 0.0}}, \"Others\": {\"Tea\": {\"amount\": 0.0}}, \"Sugars\": {\"Sugar\": {\"amount\": 0.0}}, \"Cooling\": {\"Ice\": {\"amount\": 0.0}}, \"Liquids\": {\"Water\": {\"amount\": 169.0}}}"
        ]
        ''' 
        recipe_name = 'Default Recipe'
        recipe_active = False
        quality= 'Medium'
        flavour_string =''
        flavour_effects = ["Cool", "Dry", "Balanced", "Mild"]
        pricing = 5.99 
        cups = "Cups" 
        ingredients= {
        "Liquids": {
            "Water": {"amount": 169.0}
        },
        "Cooling": {
            "Ice": {"amount": 0.0}
        },
        "Sugars": {
            "Sugar": {"amount": 0.0}
        },
        "Salts": {
             "Salt": {"amount": 0.0}
        },
        "Bases": {
             "Lemons": {"amount": 3}
        },
        "Others": {
            "Tea": {"amount": 0.0}
        }
        }
        
        ingredients_json = json.dumps(ingredients)
        flavour_effects_json = json.dumps(flavour_effects)
        
        cur = db.cursor()
        query = f'''
            INSERT INTO {recipe_table} (recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        

        try:
            # Execute the query
            cur.execute(query, (recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects_json, pricing, cups, ingredients_json))

            # Commit the transaction
            db.commit()

            print(f"Player recipe updated for player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error updating player recipe for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()
    
    def post_player_recipe_default(self, recipe_table, player_id):
        '''
        Updates player recipe using player id and other parameters
        
        generally works
        
        '''
        
        
        s_ingredients_json = '''
        "ingredients": {

            "Liquids": {
                "Water": {"amount": 169.0}
            },

            "Cooling": {
                "Ice": {"amount": 0.0}
            },


            "Sugars": {
                "Sugar": {"amount": 0.0}
            },
            "Salts": {
                "Salt": {"amount": 0.0}
            },

            "Bases": {
                "Lemons": {"amount": 3}
            },

            "Others": {
                "Tea": {"amount": 0.0}
            }
        }
        '''
        
        
        recipe_name = 'Default Recipe'
        recipe_active = False
        quality= 'Medium'
        flavour_string =''
        flavour_effects = ["Cool", "Dry", "Balanced", "Mild"]
        pricing = 4.99 
        cups = "Cups" 
        ingredients= {
        "Liquids": {
            "Water": {"amount": 169.0}
        },
        "Cooling": {
            "Ice": {"amount": 0.0}
        },
        "Sugars": {
            "Sugar": {"amount": 0.0}
        },
        "Salts": {
            "Salt": {"amount": 0.0}
        },
        "Bases": {
            "Lemons": {"amount": 3}
        },
        "Others": {
           "Tea": {"amount": 0.0}
        }
        }
        
        ingredients_json = json.dumps(ingredients)
        flavour_effects_json = json.dumps(flavour_effects)
        
       
        
        
        cur = db.cursor()
        
        
        query = f'''
            UPDATE {recipe_table}
            SET recipe_name = %s, recipe_active = %s, quality = %s, flavour_string = %s, flavour_effects = %s, pricing = %s, cups = %s, ingredients = %s
            WHERE player_id = %s
        '''

        
        try:
            # Execute the query
            cur.execute(query, (recipe_name, recipe_active, quality, flavour_string, flavour_effects_json, pricing, cups, ingredients_json, player_id))

            # Commit the transaction
            db.commit()

            print(f"Player recipe updated for player ID {player_id}")

        except Exception as e:
            # Handle the exception
            print(f"Error updating player recipe for player ID {player_id}: {e}")

        finally:
            # Close the cursor and database connection
            cur.close()
            #db.close()

    
    ##################
    #
    #   weather::   weather_id, player_id, player_day, weathercomponents[]
    #
    ################
    
    # weather
    
    # def get weather all
    # def get weather day
    # def post weather
    
    
    ##################
    #
    # sales:: sales_id, weather_id, profit, loss, total, events
    #
    ####################
    
    # sales
    # post_player_sales
    
    # add to sale day
    # finish sale day
    
    ################
    #
    # farm
    #
    #################
    
    # farm
    # tree plot 1 - duration, stage, status, water, bonus, harvest, weeds, ... water_timer, 
    
    
    # def plant_seedling_plot1()
    
    # def plant_seedling_globalplot()
    
    # def check_plant_globalplot()


    # def grow_plant_plot1()
    
    # def bear_fruit_plot1()
    
    # def water_plot1()
    
    # def potion-plot1()

    # def check_plant_plot1()
    
    # def harvest_plant_plot1()
    
    # def axe_plant_plot1()
    
    # def weeds_grow_plots()
    
       
    
    ################
    #
    # crafting
    #
    #################
    
    # def player_offer_exchange
    
    # def player_craft_current_recipe
    
    # def player_craft_default_recipe
       
    
    # def player_refine_item
    
    # def player_enchant_item
    
    # def player_alchemy_item
    
    # def player_bless_item
    
    # def player_bones_to_bananas
    # def player_bones_to_peaches
    
    # def player_freshen_item
    
    # def player_freeze_item
    # def player_heat_item
    
    # def player_combine_item
    
    
    
    
    #########
    #
    # trading ..
    #
    #########
    
    
    # def player_create_trade_offer
    # def player_close_trade_offer
    
    # def player_get_trade_offers
    # def player_get_sent_offers
    # def player_close_sent_offers
    
    # def player_get_trade_offer
    # def player_accept_trade_offer
    # def player_decline_trade_offer
    
       
    ####
    #
    # player chat 
    #
    #####
    
    
    
    ####
    #
    # player social 
    #
    #####
       
       
    ####
    #
    #   player leaderboards
    #
    ##
    # get top 10 player most balance
    # get top 10 player most money_units
    # get top 10 players most networth
    
    # get top 10 players most xp total
    # get top 10 players most total lvl
    # get top 10 players most xp per lvl
    
    
    
    
    
    
    
    
       