-- game items sql
--
CREATE TABLE item (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2),
  category VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


  --  balance BIGINT,
  --  mtx_coins BIGINT,
  --  casino_chips BIGINT,
  --  token_spins BIGINT,
  --  lemons BIGINT,
  --  limes BIGINT,
  --  shiny_lemons BIGINT,
  --  shiny_limes BIGINT,
  --  sugar BIGINT,
  --  salts BIGINT,
  --  honey BIGINT,
  --  water BIGINT,
  --  sodas BIGINT,
  --  milk BIGINT,
  --  alcohol BIGINT,
  --  ice BIGINT,
  --  heating BIGINT,
  --  cups BIGINT,
  --  tea BIGINT,
  --  coffee BIGINT,

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