INSERT INTO player_recipe1 ( 
            recipe_name, recipe_active, player_id, quality, flavour_string, flavour_effects, pricing, cups, ingredients) 
            VALUES ( 'Default Recipe', FALSE, 25, 'Medium', '',
            '["Cool", "Dry", "Balanced", "Mild" ]', 5.99, 'Cups',
            '{
                "Liquids": {
                    "water": {"amount": 169.0}
                },

                "Cooling": {
                    "ice": {"amount": 0.0}
                },


                "Sugars": {
                    "sugar": {"amount": 0.0}
                },
                "Salts": {
                    "salt": {"amount": 0.0}
                },

                "Base": {
                    "lemons": {"amount": 3}
                },

                "Others": {
                    "tea": {"amount": 0.0}
                }
            }' );