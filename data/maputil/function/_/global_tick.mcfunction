execute as @a unless score @s maputil._id matches 1.. at @s run function maputil:_/player/first_join

execute as @a unless score @s maputil._leave_game matches -1 at @s run function #maputil:player_event/on_login
scoreboard players set @a maputil._leave_game -1

execute as @a[predicate=maputil:_/respawn] at @s run function #maputil:player_event/on_respawn

execute as @e[type=area_effect_cloud, tag=!maputil._identified] at @s run function maputil:_/aec/identify
execute as @e[type=interaction, tag=maputil.interaction] at @s run function maputil:_/interaction/tick

function #maputil:tick
