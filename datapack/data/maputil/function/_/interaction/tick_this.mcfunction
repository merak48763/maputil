scoreboard players set #left_clicked maputil._ 0
execute on attacker run scoreboard players set #left_clicked maputil._ 1
scoreboard players set #right_clicked maputil._ 0
execute on target run scoreboard players set #right_clicked maputil._ 1

# Not clicked
execute if score #left_clicked maputil._ matches 0 if score #right_clicked maputil._ matches 0 run return fail

# Load data
data modify storage maputil:_ root.marker_data set value {interaction: {}}
execute on passengers if entity @s[type=marker, tag=maputil.interaction] run data modify storage maputil:_ root.marker_data set from entity @s data

# Right click
execute if score #right_clicked maputil._ matches 1 run function maputil:_/interaction/process_right_click

# Mutual exclusive interaction
execute if score #right_clicked maputil._ matches 1 \
  if data storage maputil:_ root.marker_data.interaction{right_click: {}, mutual_exclusive: true} \
  run return run data remove entity @s attack

# Left click
execute if score #left_clicked maputil._ matches 1 run function maputil:_/interaction/process_left_click
