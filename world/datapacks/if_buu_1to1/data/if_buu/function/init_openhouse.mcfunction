# Setup Open House /trigger elevator scoreboard and spawn origin marker
scoreboard objectives add if_floor trigger
kill @e[type=minecraft:marker,tag=if_buu_origin]
summon minecraft:marker ~0 ~0 ~0 {Tags:["if_buu_origin"]}
scoreboard players enable @a if_floor
