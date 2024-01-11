from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range
from firebase_handler import FirebaseHandler
from mysql_handler import MySQLHandler  # Import the MySQLHandler class
from flask_mysqldb import MySQL  


class Role:



connection = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)

# Create a cursor object
cursor = connection.cursor(dictionary=True)


# Role 
    # save role
    def save_role(self):
        
        query = 'INSERT INTO server_roles ...'
       
        cursor.execute(query)
        
        
        print("saving role to server.")
        
        
        # Check if any results were found
        if results:
            return results
        else:
            print("role cannot be saved.")
            return []
        
    # add role to user
    def save_role(self, username, role):
        
        query = 'INSERT INTO server_roles ...'
       
        cursor.execute(query, (username, role))
           
       
       
       
        print("saving user-role to server.")
        
        # Check if any results were found
        if results:
            return results
        else:
            print("user-role cannot be saved.")
            return []
        
        
       
       
       
       
       
       
       
       
       
       
       
       