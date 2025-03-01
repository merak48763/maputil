function maputil:load_player_data
data modify storage maputil:player_data root.maputil.uuid set from entity @s UUID

function #maputil:player_event/on_login
