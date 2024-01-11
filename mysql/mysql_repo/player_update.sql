-- mysql player update
CREATE TABLE player_update (
  player_id BIGINT NOT NULL,
  action_id BIGINT,
  user_location BIGINT,
  user_last_update TIMESTAMP,
  user_uptime TIMESTAMP,
  user_playtime TIMESTAMP,
  user_last_logout TIMESTAMP,
  connected BOOLEAN DEFAULT FALSE,
  player_ip VARCHAR(255),
  player_irl_location VARCHAR(255),
  player_os VARCHAR(255),
  player_current_region VARCHAR(255),
  player_home_region VARCHAR(255),
  player_pref_region VARCHAR(255),

  FOREIGN KEY (player_id) REFERENCES player(id)
  
);


-- PRIMARY KEY (player_id)	Including the PRIMARY KEY constraint ensures that the player_id column will have unique values for each row, which is necessary for maintaining data integrity and for efficient querying
-- player_id PK?
-- ip list?