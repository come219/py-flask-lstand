-- mysql player_token table


CREATE TABLE player_token ( 
	token_id INT AUTO_INCREMENT PRIMARY KEY,
	player_id BIGINT, -- Assuming player_id is a reference to another table  
	access_token VARCHAR(255) NOT NULL,
	refresh_token VARCHAR(255) NOT NULL,
	expiration_date DATETIME NOT NULL,
	creation_date DATETIME NOT NULL,
	last_updated DATETIME NOT NULL,
	-- ip address VARCHAR(255),
	-- user_agent VARCHAR(255),
	-- is_active VARCHAR(255),
	-- UNIQUE access_token,
	FOREIGN KEY (player_id) REFERENCES player(id)
	);