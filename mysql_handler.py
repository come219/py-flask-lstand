from flask_mysqldb import MySQL





    # location?
    # ping data
    # packet lost data

# CREATE TABLE server_info (
    # id INT AUTO_INCREMENT PRIMARY KEY,
    # name_server VARCHAR(255) NOT NULL,
    # num_users INT NOT NULL,
    # num_total INT NOT NULL,
    # uptime FLOAT NOT NULL,
    # last_update DATETIME NOT NULL,
    # last_use DATETIME NOT NULL,
    # members boolean?
# );


## table player security:: firebase, auth stuff, email, pass, id

## table player info:: user_id, name, sprite, game_location, server_location
## table player data:: user_id, days, money, mtx, lives, weather_fk
## table player weather:: user_id, temp, weather_state, precip, weather_id, day_fk?

## table player items:: all items?? (categorized?)
## table player recipes:: user_id, recipe1, pricing1, recipe2, pricing2, recipe3, pricing3, recipe4, pricing4
## table player sales:: user_id, day, sold, profit, weather_fk, recipe_num

## table player farm
## table player perks


## table player logs




#class MySQLHandler:
#    def __init__(self, app):
#        self.mysql = MySQL(app)

    # get total players
    # get current players

    # player sign in
    
    # player sign out
    

    # get player sprite
    
    
    
    
    
    
    
    
    
    ###########
    
    # def get_scores(self):
        # cur = self.mysql.connection.cursor()
        # cur.execute("SELECT name, score FROM scores ORDER BY score DESC")
        # scores = cur.fetchall()
        # cur.close()
        # return scores

    # def update_score(self, name, score):
        # cur = self.mysql.connection.cursor()
        # cur.execute("INSERT INTO scores (name, score) VALUES (%s, %s) ON DUPLICATE KEY UPDATE score = GREATEST(score, VALUES(score))", (name, score))
        # self.mysql.connection.commit()
        # cur.close()
