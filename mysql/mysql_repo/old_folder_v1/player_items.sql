-- player items sql - many to many
-- Player_Items junction table

CREATE TABLE player_items (
  player_id BIGINT,
  item_id BIGINT,
  quantity DOUBLE, 

  FOREIGN KEY (player_id) REFERENCES player(id),
  FOREIGN KEY (item_id) REFERENCES item(id),
  PRIMARY KEY (player_id, item_id)
);

