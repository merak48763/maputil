execute if data storage maputil:_ root.custom_data.on_attack.player on attacker run function maputil:callback_macro with storage maputil:_ root.custom_data.on_attack.player
execute if data storage maputil:_ root.custom_data.on_attack.this run function maputil:callback_macro with storage maputil:_ root.custom_data.on_attack.this

data remove entity @s attack
