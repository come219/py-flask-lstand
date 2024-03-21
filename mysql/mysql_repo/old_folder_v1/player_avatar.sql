-- mysql player_avatar table

-- m2m junction table

-- needs init

CREATE TABLE player_avatar ( 
	player_id BIGINT, -- Assuming player_id is a reference to another table  
	avatar_id INT, -- chosen avatar, default 0
	profile_border_id INT,
	FOREIGN KEY (player_id) REFERENCES player(id)
--	FOREIGN KEY (avatar_id) REFERENCES avatar(id)
	);