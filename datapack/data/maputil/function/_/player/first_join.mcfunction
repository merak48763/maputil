scoreboard players operation @s maputil._id = #next maputil._id
scoreboard players add #next maputil._id 1

function maputil:load_player_data
data modify storage maputil:player_data root.maputil.uuid set from entity @s UUID

function #maputil:player_event/on_first_join
