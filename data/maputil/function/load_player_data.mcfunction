execute unless entity @s[type=player] run return run function maputil:_/report_error/not_as_player {function: "maputil:load_player_data"}

# Cache hit
execute if score #cache_data maputil._id = @s maputil._id run return 1

# Cache miss
# Save cached data if needed
execute store result storage maputil:_ root.macro.id int 1 run scoreboard players get #cache_data maputil._id
execute if score #cache_data maputil._id matches 1.. run function maputil:_/player/save_data_macro with storage maputil:_ root.macro

# Load data
execute store result storage maputil:_ root.macro.id int 1 run scoreboard players get @s maputil._id
function maputil:_/player/load_data_macro with storage maputil:_ root.macro

# Set cache
scoreboard players operation #cache_data maputil._id = @s maputil._id

return 1
