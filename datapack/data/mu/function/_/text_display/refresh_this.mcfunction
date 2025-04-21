# modifying custom data has no effect
execute store result score #shadow mu._ run data get entity @s shadow

execute if score #shadow mu._ matches 0 run data modify entity @s shadow set value 1b
execute if score #shadow mu._ matches 0 run return run data modify entity @s shadow set value 0b

data modify entity @s shadow set value 0b
data modify entity @s shadow set value 1b
