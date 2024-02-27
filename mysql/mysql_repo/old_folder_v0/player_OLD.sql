-- mysql player

CREATE TABLE player (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  player_days INT,
  player_lives INT,
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
  quest_level INT


);



-- player_levels m2m table, level_id, current_level, achieved_level, xp_level,
-- levels list levels to insert, level_id, level_name


-- CHANGE DAYS TO DOUBLE

-- CHANGE BALANCE HERE??, + mtx coins, credit coins, other currencies, etc
-- Implement members_status BOOLEAN
-- Implement members_expiry datetime



CREATE TABLE player_v2 (
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
  quest_level INT
  player_membership BOOLEAN DEFAULT FALSE,
  player_membership_expiry TIMESTAMP,
  player_membership_status VARCHAR(255),
  
  
  

);



-- player_bal DOUBLE,
-- player_mtx DOUBLE,
-- player_credit DOUBLE,

-- normalised if in items

-- networth double?? --> round?
-- lives to DOUBLE??

-- ITEMS to DOUBLEs
-- if <currencies> moved into player table, then MUST move items row containing balance/<currencies>












-- dice_level INT,                  -- -> main level impl.
-- dice_experience INT,


--  main_level INT,
--  main_experience INT,            -- no need if a delimiter

-- quest_points ??
-- quest_level ??




-- delimiter for networth

-- delimiter for total level
-- delimiter for total xp

-- delimiter for main level?
-- delimiter for quest points
-- delimiter for quest level
