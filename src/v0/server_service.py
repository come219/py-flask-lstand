from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
import datetime
import pytz
import requests
import socket
import MySQLdb


# server service

# (server service)


app = Flask(__name__)



db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="1337",  # your password
                     db="lstand_db")        # name of the data base




# server has to maintain player data across servers
# 
class ServerService:
    def __init__(self, app):
            """
            Initialize a new instance of the class.

            :param app: The Flask application instance.
            :type app: Flask
            """
            self.app = app


    ###############
    #
    #   player count
    #
    ################
    
    
    
    def get_player_count():
        pass
        
    def post_player_count_increase():
        pass
    
    def post_player_count_decrease():
        pass
        
    def reset_player_count():
        pass
        
    def init_player_count():
        pass

    ######
    #
    #   server info
    #
    ######
 
 
    def get_server_info(self):
        '''
        Intends to return the server_info table row
        --
        --
        server id
        server members
        server name
        server version
        server api
        server location
        server_timezone
        server_time
        game_time
        num_players
        max_players
        total_players
        network_ping - call an api to get ping, packet
        network_packet
        ?ip?
        ?load_balancer_ip?
        '''
        
        server_id = 1
        cur = db.cursor() #cur = self.db.cursor(dictionary=True)  # Use dictionary cursor for easier result access
        query = '''
            SELECT * FROM server_info WHERE id = %s;
        '''

        try:
            # Execute the query
            cur.execute(query, (server_id,))

            # Fetch the first result
            result = cur.fetchone()

            if result:
                # Return the result as a dictionary
                return result
            else:
                print(f"No server info found for server ID {server_id}")
                return None

        except Exception as e:
            # Handle the exception
            print(f"Error fetching server info for server ID {server_id}: {e}")

        finally:
            # Close the cursor
            cur.close()
        pass
        
    # def get_server_location_by_db    
        
    def get_server_location(self):
        """
        Get the current server location.

        :return: The current server location.
        :rtype: dict
        """
        try:
            response = requests.get('http://ip-api.com/json/')
            if response.status_code == 200:
                json_response = response.json()
                return {
                    "success": True,
                    "country": json_response.get('country'),
                    "region": json_response.get('regionName'),
                    "city": json_response.get('city'),
                    "zip": json_response.get('zip'),
                    "lat": json_response.get('lat'),
                    "lon": json_response.get('lon'),
                    "timezone": json_response.get('timezone'),
                    "isp": json_response.get('isp'),
                    "org": json_response.get('org'),
                    "as": json_response.get('as')
                }
            else:
                return {"success": False, "message": "Unable to get location"}

        except Exception as e:
            return {"success": False, "message": str(e)}
        
        
    # bing chat says could be implemented through client:: https://drive.google.com/file/d/1yDSvTA-yAIrMs2QigIWFpkQnpBtDYOFd/view?usp=sharing
    def get_server_response_time():
        pass
        
    
    def get_server_version():
        pass
        
    def get_server_api():
        pass
    
        
    def get_server_connection(self):
        """
        Check if there is a successful connection to the server at 8.8.8.8.

        :return: True if the connection is successful, False otherwise.
        :rtype: bool
        """
        target_ip = "8.8.8.8"
        target_port = 53  # DNS port

        try:
            # Create a socket to check connectivity
            socket.create_connection((target_ip, target_port), timeout=2)
            return True
        except OSError:
            return False
        
    # server time
    def get_server_time(self):
        """
        Get the current server time.

        :return: The current server time.
        :rtype: datetime
        """
        return datetime.datetime.now();
    
    # server timezone
    def get_server_timezone(self):
        """
        Get the current server timezone.

        :return: The current server timezone.
        :rtype: str
        """
        return datetime.datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%Z%z')