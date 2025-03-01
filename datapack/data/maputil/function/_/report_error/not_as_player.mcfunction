$tellraw @a {translate: "maputil.function.error", "fallback": "[maputil] Error: %s", color: "red", with: [{translate: "maputil.function.error.not_as_player", "fallback": "function %s must be run as a player", with: ["$(function)"]}]}
return fail
