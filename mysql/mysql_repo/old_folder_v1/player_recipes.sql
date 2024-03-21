-- player recipes table



CREATE TABLE player_recipe1 ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	recipe_name VARCHAR(255), 
	player_id BIGINT, -- Assuming player_id is a reference to another table 
	recipe_active BOOLEAN,
	quality VARCHAR(255), 
	flavour_string VARCHAR(255), 
	flavour_effects JSON, 
	pricing DOUBLE, 
	cups VARCHAR(255), 
	ingredients JSON,
	FOREIGN KEY (player_id) REFERENCES player(id)
	);
	
	CREATE TABLE player_recipe2 ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	recipe_name VARCHAR(255), 
	player_id BIGINT, -- Assuming player_id is a reference to another table 
	recipe_active BOOLEAN,
	quality VARCHAR(255), 
	flavour_string VARCHAR(255), 
	flavour_effects JSON, 
	pricing DOUBLE, 
	cups VARCHAR(255), 
	ingredients JSON,
	FOREIGN KEY (player_id) REFERENCES player(id)
	);
	
	CREATE TABLE player_recipe3 ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	recipe_name VARCHAR(255), 
	player_id BIGINT, -- Assuming player_id is a reference to another table 
	recipe_active BOOLEAN,
	quality VARCHAR(255), 
	flavour_string VARCHAR(255), 
	flavour_effects JSON, 
	pricing DOUBLE, 
	cups VARCHAR(255), 
	ingredients JSON,
	FOREIGN KEY (player_id) REFERENCES player(id)
	);
	
	CREATE TABLE player_recipe4 ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	recipe_name VARCHAR(255), 
	player_id BIGINT, -- Assuming player_id is a reference to another table 
	recipe_active BOOLEAN,
	quality VARCHAR(255), 
	flavour_string VARCHAR(255), 
	flavour_effects JSON, 
	pricing DOUBLE, 
	cups VARCHAR(255), 
	ingredients JSON,
	FOREIGN KEY (player_id) REFERENCES player(id)
	);
	
	
	-- ingredients JSON 
	-- ingredients0_liquids JSON 
	-- ingredients1_cooling JSON 
	-- ingredients2_sugars JSON 
	-- ingredients3_salts JSON 
	-- ingredients3_bases JSON (lemons, fruits)
	-- ingredients3_others JSON (tea, coffee)


-- CREATE TABLE player_items (
--   player_id BIGINT,
--   item_id BIGINT,
--   quantity BIGINT,
--   total_use INT,
--   current_use INT,
-- 
--   FOREIGN KEY (player_id) REFERENCES player(id),
--   FOREIGN KEY (item_id) REFERENCES item(id),
--   PRIMARY KEY (player_id, item_id)
-- );



