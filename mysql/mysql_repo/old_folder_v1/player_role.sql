-- mysql player role
-- m2m list

CREATE TABLE player_role (
  player_id BIGINT,
  role_id INT,
  FOREIGN KEY (player_id) REFERENCES player(id),
  FOREIGN KEY (role_id) REFERENCES server_roles(id)
);
