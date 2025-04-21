scoreboard players set #left_clicked mu._ 0
execute on attacker run scoreboard players set #left_clicked mu._ 1
scoreboard players set #right_clicked mu._ 0
execute on target run scoreboard players set #right_clicked mu._ 1

# Not clicked
execute if score #left_clicked mu._ matches 0 if score #right_clicked mu._ matches 0 run return fail

# Load data
data modify storage mu:_ root.custom_data set from entity @s data.mu

# Right click
execute if score #right_clicked mu._ matches 1 run function mu:_/interaction/process_right_click

# Left click
execute if score #left_clicked mu._ matches 1 run function mu:_/interaction/process_left_click
