$tellraw @a {translate: "mu.function.error", "fallback": "[mu] Error: %s", color: "red", with: [{translate: "mu.function.error.not_as_player", "fallback": "function %s must be run as a player", with: ["$(function)"]}]}
return fail
