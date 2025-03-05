execute as @a unless score @s maputil._id matches 1.. at @s run function maputil:_/player/first_join
execute as @a at @s run function maputil:_/player/tick_this

execute as @e[type=area_effect_cloud, tag=!maputil._identified] at @s run function maputil:_/aec/identify
execute if entity @a[predicate=maputil:_/player/trigger_interaction, limit=1] run function maputil:_/interaction/tick_all

function #maputil:tick
