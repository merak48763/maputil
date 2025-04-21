function mu:load_player_data
data modify storage mu:player_data root.mu.uuid set from entity @s UUID

function #mu:player_event/on_login
