execute if data storage maputil:_ root.custom_data.on_interact.as_player run data modify storage maputil:_ root.macro.function set from storage maputil:_ root.custom_data.on_interact.as_player
execute if data storage maputil:_ root.custom_data.on_interact.as_player on target run function maputil:callback_macro with storage maputil:_ root.macro

execute if data storage maputil:_ root.custom_data.on_interact.as_this run data modify storage maputil:_ root.macro.function set from storage maputil:_ root.custom_data.on_interact.as_this
execute if data storage maputil:_ root.custom_data.on_interact.as_this run function maputil:callback_macro with storage maputil:_ root.macro

data remove entity @s interaction
