-- mysql player security
CREATE TABLE player_security (
  player_id BIGINT NOT NULL,
  email VARCHAR(255) NOT NULL,
  verified_email BOOLEAN DEFAULT FALSE,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  password_reset_token VARCHAR(255),
  password_reset_expire TIMESTAMP,
  player_hide_code VARCHAR(255),
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  dob DATE,
  user_creation_date TIMESTAMP NOT NULL,
  user_last_login TIMESTAMP,
  user_login_attempts INT DEFAULT 0,
  account_locked BOOLEAN DEFAULT FALSE,
  account_locked_reason VARCHAR(255),
  FOREIGN KEY (player_id) REFERENCES player(id)

);
