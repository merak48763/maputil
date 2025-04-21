tag @s add mu._hurt
# @e has living check
# distance=0 works in this case
execute unless entity @e[type=player, tag=mu._hurt, distance=0] run function #mu:player_event/on_die
tag @s remove mu._hurt

advancement revoke @s only mu:_/detect_death
