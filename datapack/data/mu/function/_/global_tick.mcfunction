execute as @a unless score @s mu._id matches 1.. at @s run function mu:_/player/first_join
execute as @a at @s run function mu:_/player/tick_this

execute as @e[type=area_effect_cloud, tag=!mu._identified] at @s run function mu:_/aec/identify
execute if entity @a[predicate=mu:_/player/trigger_interaction, limit=1] run function mu:_/interaction/tick_all

function #mu:tick
