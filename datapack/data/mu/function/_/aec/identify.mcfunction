data modify storage mu:aec custom_effects set value []
data modify storage mu:aec custom_effects set from entity @s potion_contents.custom_effects
tag @s add mu._identified
function #mu:entity_event/on_aec_spawned
