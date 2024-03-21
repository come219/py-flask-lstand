-- mysql player_levels


-- player_levels m2m table, level_id, current_level, achieved_level, xp_level,
-- levels list levels to insert, level_id, level_name
-- prestige levels... later..

CREATE TABLE player_levels (
  player_id BIGINT,
  level_id BIGINT,
  current_level INT,
  achieved_level INT,
  xp_level INT,
  FOREIGN KEY (player_id) REFERENCES player(id),
  FOREIGN KEY (level_id) REFERENCES levels(id),
  PRIMARY KEY (player_id, level_id)

);

