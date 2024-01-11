-- mysql player
CREATE TABLE player (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  player_days DOUBLE,
  player_lives INT,
  player_lives_status VARCHAR(255),
  player_streak INT,
  player_streak_timer TIMESTAMP,
  player_networth BIGINT,
  player_location VARCHAR(255),
  player_offers_notifications INT,
  player_trade_requests INT,
  player_inbox_messages INT,
  player_private BOOLEAN DEFAULT FALSE,
  player_hide BOOLEAN DEFAULT FALSE,
  main_level INT,
  total_level INT,
  total_xp INT,
  quest_points INT,
  quest_level INT,
  player_membership BOOLEAN DEFAULT FALSE,
  player_membership_expiry TIMESTAMP,
  player_membership_status VARCHAR(255)
  
);
-- FIELD FOR PLAYER_AVATAR_ID --> located in player_avatar
-- b/c also stall id, json..




-- delimiter for networth ??

-- delimiter for total level
-- delimiter for total xp

-- delimiter for main level ??
-- delimiter for quest points
-- delimiter for quest level
