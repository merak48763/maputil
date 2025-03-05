scoreboard players set #left_clicked maputil._ 0
execute on attacker run scoreboard players set #left_clicked maputil._ 1
scoreboard players set #right_clicked maputil._ 0
execute on target run scoreboard players set #right_clicked maputil._ 1

# Not clicked
execute if score #left_clicked maputil._ matches 0 if score #right_clicked maputil._ matches 0 run return fail

# Load data
data modify storage maputil:_ root.custom_data set from entity @s data.maputil

# Right click
execute if score #right_clicked maputil._ matches 1 run function maputil:_/interaction/process_right_click

# Left click
execute if score #left_clicked maputil._ matches 1 run function maputil:_/interaction/process_left_click
