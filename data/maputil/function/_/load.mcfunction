scoreboard objectives add maputil._ dummy {"text": "don't touch", "color": "gray"}
scoreboard objectives add maputil._id dummy {"text": "don't touch", "color": "gray"}
execute unless score #next maputil._id matches 1.. run scoreboard players set #next maputil._id 1
execute unless score #cache_data maputil._id matches 0.. run scoreboard players set #cache_data maputil._id 0
scoreboard objectives add maputil._leave_game custom:leave_game {"text": "don't touch", "color": "gray"}

execute unless data storage maputil:player_data root run data modify storage maputil:player_data root set value {}

schedule function maputil:_/scheduled_1s 0.4s replace
schedule function maputil:_/scheduled_10s 0.7s replace
