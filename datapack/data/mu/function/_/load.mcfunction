scoreboard objectives add mu._ dummy {"text": "don't touch", "color": "gray"}
scoreboard objectives add mu._id dummy {"text": "don't touch", "color": "gray"}
execute unless score #next mu._id matches 1.. run scoreboard players set #next mu._id 1
execute unless score #cache_data mu._id matches 0.. run scoreboard players set #cache_data mu._id 0
scoreboard objectives add mu._leave_game custom:leave_game {"text": "don't touch", "color": "gray"}

execute unless data storage mu:player_data root run data modify storage mu:player_data root set value {}

schedule function mu:_/scheduled_1s 0.4s replace
