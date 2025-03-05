execute unless score @s maputil._leave_game matches -1 run function maputil:_/player/login
scoreboard players set @s maputil._leave_game -1

execute if predicate maputil:_/player/respawn at @s run function #maputil:player_event/on_respawn
