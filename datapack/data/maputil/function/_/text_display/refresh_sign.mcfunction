execute unless block ~ ~ ~ #all_signs run return run kill @s
execute unless data block ~ ~ ~ components.minecraft:custom_data.maputil.translated run return run kill @s
execute store result block ~ ~ ~ components.minecraft:custom_data.maputil.translated._ int 1 run time query gametime
