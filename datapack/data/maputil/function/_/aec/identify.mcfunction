data modify storage maputil:aec custom_effects set value []
data modify storage maputil:aec custom_effects set from entity @s potion_contents.custom_effects
tag @s add maputil._identified
function #maputil:entity_event/on_aec_spawned
