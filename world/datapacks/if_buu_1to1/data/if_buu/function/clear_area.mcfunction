# Clear 1:1 building bounding volume before rebuilding
fill ~-74 ~-6 ~-34 ~-44 ~4 ~34 minecraft:air
fill ~-43 ~-6 ~-34 ~-12 ~4 ~34 minecraft:air
fill ~-11 ~-6 ~-34 ~22 ~4 ~34 minecraft:air
fill ~-74 ~5 ~-34 ~-44 ~15 ~34 minecraft:air
fill ~-43 ~5 ~-34 ~-12 ~15 ~34 minecraft:air
fill ~-11 ~5 ~-34 ~22 ~15 ~34 minecraft:air
fill ~-74 ~16 ~-34 ~-44 ~26 ~34 minecraft:air
fill ~-43 ~16 ~-34 ~-12 ~26 ~34 minecraft:air
fill ~-11 ~16 ~-34 ~22 ~26 ~34 minecraft:air
fill ~-74 ~27 ~-34 ~-44 ~37 ~34 minecraft:air
fill ~-43 ~27 ~-34 ~-12 ~37 ~34 minecraft:air
fill ~-11 ~27 ~-34 ~22 ~37 ~34 minecraft:air
fill ~-74 ~38 ~-34 ~-44 ~48 ~34 minecraft:air
fill ~-43 ~38 ~-34 ~-12 ~48 ~34 minecraft:air
fill ~-11 ~38 ~-34 ~22 ~48 ~34 minecraft:air
fill ~-74 ~49 ~-34 ~-44 ~59 ~34 minecraft:air
fill ~-43 ~49 ~-34 ~-12 ~59 ~34 minecraft:air
fill ~-11 ~49 ~-34 ~22 ~59 ~34 minecraft:air
fill ~-74 ~60 ~-34 ~-44 ~66 ~34 minecraft:air
fill ~-43 ~60 ~-34 ~-12 ~66 ~34 minecraft:air
fill ~-11 ~60 ~-34 ~22 ~66 ~34 minecraft:air
kill @e[type=minecraft:marker,tag=if_buu_origin]
tellraw @a {"text":"[IF-BUU 1:1] Cleared building zone.","color":"yellow"}
