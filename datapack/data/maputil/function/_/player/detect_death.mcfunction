tag @s add maputil._hurt
# @e has living check
execute unless entity @e[type=player, tag=maputil._hurt] run function #maputil:player_event/on_die
tag @s remove maputil._hurt

advancement revoke @s only maputil:_/detect_death
