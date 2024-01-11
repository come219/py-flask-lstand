
-- insert default reciepe in recipe 1 
-- inserts into player 25..
INSERT INTO player_recipe1 ( recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients) VALUES ( 'Default Recipe', FALSE, 25, 'Medium', '', '["Cool", "Dry", "Balanced", "Mild" ]', 5.99, 'Small', '{"water": {"amount": 169.0}, "ice": {"amount": 0.0}, "sugar": {"amount": 0.0}, "salts": {"amount": 0.0}, "base": {"lemon": {"amount": 3}, "lime": {"amount": 1}}, "others": {"tea": {"amount": 0.0}}}' );


-- insert into recipe2, recipe3, recipe4. 



-- 		[
--          1,
--          "Default Recipe",
--          25,
--          1,
--          "Medium",
--          "",
--          "[\"Cool\", \"Dry\", \"Balanced\", \"Mild\"]",
--          5.99,
--          "Cups",
--          "{\"Base\": {\"Lemons\": {\"amount\": 3}}, \"Salts\": {\"Salt\": {\"amount\": 0.0}}, \"Others\": {\"Tea\": {\"amount\": 0.0}}, \"Sugars\": {\"Sugar\": {\"amount\": 0.0}}, \"Cooling\": {\"Ice\": {\"amount\": 0.0}}, \"Liquids\": {\"Water\": {\"amount\": 169.0}}}"
--        ]