-- mysql game_levels
-- levels list levels to insert, level_id, level_name
--

CREATE TABLE levels (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- prestige levels, counts ??
  -- prestige_level INT,
  -- prestige_count INT,
  -- prestige_days_count INT,
  -- prestige_level_campaign_count INT,
  -- prestige_level_..._count INT,
  -- unprestiged BOOLEAN,           -- removes all prestige levels, returns all values back in total

