execute unless entity @s[type=player] run return run function mu:_/report_error/not_as_player {function: "mu:load_player_data"}

# Cache hit
execute if score #cache_data mu._id = @s mu._id run return 1

# Cache miss
# Save cached data if needed
execute store result storage mu:_ root.macro.id int 1 run scoreboard players get #cache_data mu._id
execute if score #cache_data mu._id matches 1.. run function mu:_/player/save_data_macro with storage mu:_ root.macro

# Load data
data modify storage mu:player_data root set value {}
execute store result storage mu:_ root.macro.id int 1 run scoreboard players get @s mu._id
function mu:_/player/load_data_macro with storage mu:_ root.macro

# Set cache
scoreboard players operation #cache_data mu._id = @s mu._id

return 1
