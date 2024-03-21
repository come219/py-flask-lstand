-- player weather table



CREATE TABLE player_weather ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	player_id BIGINT, -- Assuming player_id is a reference to another table 
	player_day DOUBLE, -- Assuming player_day is a reference to another table 
	weather_type VARCHAR(255), -- geo locator, server, value rand, 
	weather_component JSON, 
	FOREIGN KEY (player_id) REFERENCES player(id)
	);