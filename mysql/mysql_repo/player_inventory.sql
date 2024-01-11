-- mysql player inventory

-- m2m list

-- stall meaning player's counter or shop

CREATE TABLE player_inventory ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	player_id BIGINT, -- Assuming player_id is a reference to another table  
	  
	stall_name VARCHAR(255), 
	stall JSON, 
	perks JSON, 
	equipment JSON, 
	summoning JSON, 
	FOREIGN KEY (player_id) REFERENCES player(id)
	);