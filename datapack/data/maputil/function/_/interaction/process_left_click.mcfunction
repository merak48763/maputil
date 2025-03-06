execute if data storage maputil:_ root.custom_data.on_attack.as_player run data modify storage maputil:_ root.macro.function set from storage maputil:_ root.custom_data.on_attack.as_player
execute if data storage maputil:_ root.custom_data.on_attack.as_player on attacker run function maputil:callback_macro with storage maputil:_ root.macro

execute if data storage maputil:_ root.custom_data.on_attack.as_this run data modify storage maputil:_ root.macro.function set from storage maputil:_ root.custom_data.on_attack.as_this
execute if data storage maputil:_ root.custom_data.on_attack.as_this run function maputil:callback_macro with storage maputil:_ root.macro

data remove entity @s attack
