execute if data storage mu:_ root.custom_data.on_interact.as_player run data modify storage mu:_ root.macro.function set from storage mu:_ root.custom_data.on_interact.as_player
execute if data storage mu:_ root.custom_data.on_interact.as_player on target run function mu:callback_macro with storage mu:_ root.macro

execute if data storage mu:_ root.custom_data.on_interact.as_this run data modify storage mu:_ root.macro.function set from storage mu:_ root.custom_data.on_interact.as_this
execute if data storage mu:_ root.custom_data.on_interact.as_this run function mu:callback_macro with storage mu:_ root.macro

data remove entity @s interaction
