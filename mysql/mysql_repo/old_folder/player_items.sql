-- mysql player items

CREATE TABLE player_items (
  player_id BIGINT PRIMARY KEY,
  balance BIGINT,
  mtx_coins BIGINT,
  casino_chips BIGINT,
  token_spins BIGINT,
  lemons BIGINT,
  limes BIGINT,
  shiny_lemons BIGINT,
  shiny_limes BIGINT,
  sugar BIGINT,
  salts BIGINT,
  honey BIGINT,
  water BIGINT,
  sodas BIGINT,
  milk BIGINT,
  alcohol BIGINT,
  ice BIGINT,
  heating BIGINT,
  cups BIGINT,
  tea BIGINT,
  coffee BIGINT,
  FOREIGN KEY (player_id) REFERENCES player(id)
);

-- small ice
-- fridge ice
-- natural heat
-- ice block

-- sugar water syrup
-- natural fructose syrup
-- grenadine
-- molasses



-- the other items..
-- farm items .. in here?

-- more items'

-- currency items
-- farm items
-- m2m items
