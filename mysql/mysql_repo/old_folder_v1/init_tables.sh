#!/bin/bash

# print statement to show run


# MySQL Connection Details
DB_HOST="localhost"   # change to file or hashed
DB_USER="mysql"       # change to file or hashed
DB_PASSWORD="1337"    # change to file or hashed
DB_NAME="lstand_db"   # change to file or hashed
DB_PROD_NAME="lstand_main_db"   # change to file or hashed

# Function to execute SQL file
execute_sql_file() {
    local file="$1"
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$file"

    #print "."
}

# Create or initialize core server table
execute_sql_file "server_roles.sql"


execute_sql_file "game_items.sql"	# server items - item
execute_sql_file "game_levels.sql"	# server levels - levels

# server shops

# Create or initialize core player table
execute_sql_file "player.sql"

# requires
execute_sql_file "player_items.sql"
execute_sql_file "player_levels.sql"
execute_sql_file "player_role.sql"

# player's
execute_sql_file "player_security.sql"
execute_sql_file "player_update.sql"


# Create or initialize GAME table
execute_sql_file "player_inventory.sql"
execute_sql_file "player_shops.sql"

# player_weather
# player_recipes
# player_sales
# 
# player_farm
# 


# print statement to say conclusions and time

# Create your combined table or any additional tables
# Execute additional SQL files as needed
# execute_sql_file "additional_table.sql"

# update / insert into tables backup/saved data


# print statement to say conclusions and time



# print statement to total conclusions and time






### Notes::

# mysql -u username -p database_name < path\to\file.sql

# mysql> source path\to\file.sql;

# mysql> \. path\to\file.sql;

# \. C:\Users\qqstj\IdeaProjects\base_lstand_backend\!embedded_projects\dbms_repo\mysql_repo\server_roles.sql

# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\game_items.sql
# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\game_levels.sql

# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player.sql

# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_items.sql 
# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_levels.sql 
# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_role.sql 


#\. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_avatar.sql 

# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_security.sql 
# \. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_update.sql 

#\. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\server_info.sql 
#\. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\server_info_insert.sql 

#\. C:\Users\qqstj\OneDrive\Documents\GitHub\py-flask-lstand\mysql\mysql_repo\player_recipes.sql 


# game_items_insert.sql

# game_levels_insert.sql


# weather

# sales








###################################
#
# understanding player creation -
#
#	1. create_player()  creates player:-->  player_security
#
#	2. init_player() player_update, , player_items, player_recipes
#		
#		init_player_items_start(player_id)
#       init_player_levels_start(player_id)
#       init_player_inventory_start(player_id)
#		init_player_recipes_start(player_id)
#		weather init
#		init_avatar
#		
#
###################################
