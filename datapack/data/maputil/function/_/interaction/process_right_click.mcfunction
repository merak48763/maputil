execute if data storage maputil:_ root.custom_data.on_interact.player on target run function maputil:callback_macro with storage maputil:_ root.custom_data.on_interact.player
execute if data storage maputil:_ root.custom_data.on_interact.this run function maputil:callback_macro with storage maputil:_ root.custom_data.on_interact.this

data remove entity @s interaction
