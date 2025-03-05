schedule function maputil:_/scheduled_1s 1s replace

execute as @e[type=text_display, predicate=maputil:_/entity/translated] run function maputil:_/text_display/refresh_this
execute as @e[type=marker, tag=maputil.translated] run function maputil:_/text_display/refresh_sign
