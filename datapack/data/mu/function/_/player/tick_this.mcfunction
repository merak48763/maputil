execute unless score @s mu._leave_game matches -1 run function mu:_/player/login
scoreboard players set @s mu._leave_game -1

execute if predicate mu:_/player/respawn at @s run function #mu:player_event/on_respawn
