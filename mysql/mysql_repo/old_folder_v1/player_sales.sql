-- player sales table



CREATE TABLE player_sales ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	weather_id BIGINT, -- Assuming player_id is a reference to another table
	player_id BIGINT, -- Assuming player_id is a reference to another table  
	player_day DOUBLE, -- Assuming player_day is a reference to another table 
	irl_day TIMESTAMP, -- time when played
	location VARCHAR(255),  -- campaign selected game location
	profit DOUBLE,
	loss DOUBLE,
	tips DOUBLE,
	total DOUBLE,
	start_time VARCHAR(255), 
	finish_time VARCHAR(255),  -- skiptime VARCHAR(255), 
	duration VARCHAR(255), 
	events JSON, 
	FOREIGN KEY (player_id) REFERENCES player(id)
	);
	
	
	-- status active bool?
	-- recipe id data?
	-- damage?