-- mysql player inventory

-- m2m list

-- stall meaning player's counter or shop

CREATE TABLE player_inventory ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	player_id BIGINT, -- Assuming player_id is a reference to another table  
	  -- border_id ??
	stall_name VARCHAR(255), 
	stall JSON, 
	stall_levels JSON,
	perks JSON,  
	equipment JSON, 
	-- equipment_helmet JSON,
	-- equipment_body JSON,
	-- equipment_gaunlets JSON,
	-- equipment_cape JSON,
	-- equipment_legs JSON,
	-- equipment_boots JSON,
	-- equipment_ring JSON,
	-- equipment_mainhand JSON,
	-- equipment_offhand JSON,
	summoning JSON, 
	-- summoning_armor JSON, 
	FOREIGN KEY (player_id) REFERENCES player(id)
	);