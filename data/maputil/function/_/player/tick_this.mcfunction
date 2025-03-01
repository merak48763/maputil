execute unless score @s maputil._leave_game matches -1 run function #maputil:player_event/on_login
scoreboard players set @s maputil._leave_game -1

execute if predicate maputil:_/respawn at @s run function #maputil:player_event/on_respawn
