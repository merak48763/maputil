schedule function mu:_/scheduled_1s 1s replace

execute as @e[type=text_display, tag=mu.translated] run function mu:_/text_display/refresh_this
execute as @e[type=marker, tag=mu.translated] run function mu:_/text_display/refresh_sign
