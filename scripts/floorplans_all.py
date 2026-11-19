"""
Exact 1:1 Floor-by-Floor Interior Layouts for Floors 1 to 11
Derived directly from official Informatics Building fire-escape floor plans:
  - Floors 1-7: references/floorplans/floor_01.jpg .. floor_07.jpg
  - Floor 8, 10, 11: references/floorplans/floor_08.jpg, floor_10.jpg, floor_11.jpg
  - Floor 1 details: floor_01_shutter.jpg, floor_01_booth.jpg, floor_01_undercroft.jpg

True Google Maps / ESRI Satellite Orientation (90 deg Clockwise from Plan Top):
  Plan Top    (pz=0)  -> East  (+X) facing Fueang Fa Road & Front Plaza
  Plan Bottom (pz=48) -> West  (-X) Elevator/Main Stair Spine & West Moto Parking
  Plan Left   (px=0)  -> North (-Z) Restrooms Wing, 11F Solar Roof & NW Wing
  Plan Right  (px=54) -> South (+Z) C-Arch Canopy Fins, 5M210 Wing & South Bldg

Transform:
  mc_x = 24 - pz   (spans -24 .. +24)
  mc_z = px - 27   (spans -27 .. +27)
"""

import json

ROTATE_FACING = {
    "north": "east",
    "east": "south",
    "south": "west",
    "west": "north",
    "up": "up",
    "down": "down",
}


def to_mc(px: int, pz: int) -> tuple[int, int]:
    return 24 - pz, px - 27


def rot_block(block: str) -> str:
    if "facing=" not in block:
        return block
    for k, v in ROTATE_FACING.items():
        if f"facing={k}" in block:
            return block.replace(f"facing={k}", f"facing={v}")
    return block


def fill_p(px1: int, y1: int, pz1: int, px2: int, y2: int, pz2: int, block: str, mode: str = "") -> str:
    x1, z1 = to_mc(px1, pz1)
    x2, z2 = to_mc(px2, pz2)
    xa, xb = min(x1, x2), max(x1, x2)
    ya, yb = min(y1, y2), max(y1, y2)
    za, zb = min(z1, z2), max(z1, z2)
    suffix = f" {mode}" if mode else ""
    return f"fill ~{xa} ~{ya} ~{za} ~{xb} ~{yb} ~{zb} {rot_block(block)}{suffix}"


def set_p(px: int, y: int, pz: int, block: str) -> str:
    x, z = to_mc(px, pz)
    return f"setblock ~{x} ~{y} ~{z} {rot_block(block)}"


def sign_p(px: int, y: int, pz: int, plan_facing: str, l1: str, l2: str = "", l3: str = "", l4: str = "") -> str:
    x, z = to_mc(px, pz)
    mc_facing = ROTATE_FACING.get(plan_facing, plan_facing)
    msgs = [json.dumps(s.replace("'", ""), ensure_ascii=False) for s in (l1, l2, l3, l4)]
    nbt = "{front_text:{messages:[" + ",".join(f'\'{{"text":{m}}}\'' for m in msgs) + "]}}"
    return f"setblock ~{x} ~{y} ~{z} minecraft:oak_wall_sign[facing={mc_facing}]{nbt}"


def text_p(px: float, y: float, pz: float, text: str, plan_yaw: float, scale: float = 0.85) -> str:
    x, z = 24.0 - pz, px - 27.0
    mc_yaw = (plan_yaw + 90.0) % 360.0
    if mc_yaw > 180.0:
        mc_yaw -= 360.0
    escaped = json.dumps(text, ensure_ascii=False)
    return (
        f'summon minecraft:text_display ~{x} ~{y} ~{z} '
        f'{{Tags:["if_buu_label"],text:{{text:{escaped},color:"white",bold:true}},'
        f'Rotation:[{mc_yaw}f,0f],billboard:"fixed",background:0,'
        f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
        f'translation:[0f,0f,0f],scale:[{scale}f,{scale}f,{scale}f]}}}}'
    )


def build_restrooms_sw(yf: int, yc: int) -> list[str]:
    """1F & 2F Restrooms in Plan SW corner (px=0..8, pz=34..48)."""
    return [
        fill_p(0, yf + 1, 34, 8, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(1, yf + 1, 38, 7, yc - 1, 38, "minecraft:white_concrete"),
        fill_p(1, yf + 1, 43, 7, yc - 1, 43, "minecraft:white_concrete"),
        fill_p(8, yf + 1, 36, 8, yf + 2, 36, "minecraft:air"),
        fill_p(8, yf + 1, 40, 8, yf + 2, 40, "minecraft:air"),
        fill_p(8, yf + 1, 45, 8, yf + 2, 45, "minecraft:air"),
        set_p(4, yc - 1, 36, "minecraft:sea_lantern"),
        set_p(4, yc - 1, 40, "minecraft:sea_lantern"),
        set_p(4, yc - 1, 45, "minecraft:sea_lantern"),
        sign_p(9, yf + 2, 40, "east", "Restrooms", "Disabled/M/F"),
    ]


def build_restrooms_west_3_to_8(yf: int, yc: int) -> list[str]:
    """3F-8F Restrooms: Men's & Disabled (px=0..4, pz=19..33), Ladies' (px=0..7, pz=34..48)."""
    return [
        fill_p(0, yf + 1, 19, 4, yc - 1, 33, "minecraft:white_concrete", "hollow"),
        fill_p(1, yf + 1, 29, 3, yc - 1, 29, "minecraft:white_concrete"),
        fill_p(4, yf + 1, 24, 4, yf + 2, 24, "minecraft:air"),
        fill_p(4, yf + 1, 31, 4, yf + 2, 31, "minecraft:air"),
        set_p(2, yc - 1, 24, "minecraft:sea_lantern"),
        set_p(2, yc - 1, 31, "minecraft:sea_lantern"),
        fill_p(0, yf + 1, 34, 7, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(7, yf + 1, 40, 7, yf + 2, 41, "minecraft:air"),
        set_p(3, yc - 1, 41, "minecraft:sea_lantern"),
        sign_p(5, yf + 2, 24, "east", "Men /", "Disabled"),
        sign_p(8, yf + 2, 41, "east", "Ladies Room"),
    ]


def build_restrooms_9_to_11(yf: int, yc: int) -> list[str]:
    """9F-11F Restrooms along stepped-in West wall (px=0..4, pz=30..48)."""
    return [
        fill_p(0, yf + 1, 30, 6, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(1, yf + 1, 36, 5, yc - 1, 36, "minecraft:white_concrete"),
        fill_p(1, yf + 1, 42, 5, yc - 1, 42, "minecraft:white_concrete"),
        fill_p(6, yf + 1, 33, 6, yf + 2, 33, "minecraft:air"),
        fill_p(6, yf + 1, 39, 6, yf + 2, 39, "minecraft:air"),
        fill_p(6, yf + 1, 45, 6, yf + 2, 45, "minecraft:air"),
        set_p(3, yc - 1, 33, "minecraft:sea_lantern"),
        set_p(3, yc - 1, 39, "minecraft:sea_lantern"),
        set_p(3, yc - 1, 45, "minecraft:sea_lantern"),
        sign_p(7, yf + 2, 39, "east", "Restrooms", "Disabled/M/F"),
    ]


def build_floor_1() -> list[str]:
    yf, yc = 0, 6
    cmds = [
        "# === FLOOR 1 (Exact Plan + Real 1F Photos: Shutter, Glass Booth, Undercroft) ===",
        *build_restrooms_sw(yf, yc),
        # NW: IF-109 Student Union (SMO) & Co-Working Space
        fill_p(2, yf + 1, 3, 14, yc - 1, 14, "minecraft:white_stained_glass", "hollow"),
        fill_p(14, yf + 1, 8, 14, yf + 3, 10, "minecraft:air"),
        set_p(8, yf + 1, 8, "minecraft:oak_planks"),
        set_p(8, yc - 1, 8, "minecraft:sea_lantern"),
        sign_p(15, yf + 2, 9, "east", "IF-109", "Student Union", "(SMO)"),

        fill_p(5, yf + 1, 15, 14, yc - 1, 26, "minecraft:white_stained_glass", "hollow"),
        fill_p(14, yf + 1, 20, 14, yf + 3, 21, "minecraft:air"),
        fill_p(9, yf + 1, 20, 10, yf + 1, 21, "minecraft:oak_slab"),
        set_p(9, yc - 1, 20, "minecraft:sea_lantern"),
        sign_p(15, yf + 2, 20, "east", "Co-Working", "Space"),

        # 1F Glass Automatic Entrance Wall & Glass Security/Info Booth (floor_01_booth.jpg!)
        fill_p(15, yf + 1, 28, 26, yc - 1, 28, "minecraft:white_stained_glass"),
        fill_p(19, yf + 1, 28, 21, yf + 3, 28, "minecraft:air"),
        fill_p(14, yf + 1, 29, 18, yc - 1, 32, "minecraft:white_stained_glass", "hollow"),
        sign_p(16, yf + 2, 28, "north", "Stairs ->", "Toilets ->"),

        # Rolling Metal Shutter + IF-104 Utility Door near SW Corridor (floor_01_shutter.jpg!)
        fill_p(27, yf + 1, 35, 31, yf + 4, 35, "minecraft:polished_andesite"),
        fill_p(28, yf + 2, 35, 30, yf + 3, 35, "minecraft:iron_bars"),
        sign_p(26, yf + 2, 34, "north", "IF-104", "Rolling Shutter"),

        # 1F Indoor Wheelchair Ramp (px=23..30, pz=6..9)
        fill_p(23, yf, 6, 30, yf, 9, "minecraft:smooth_quartz_slab"),
        fill_p(23, yf + 1, 9, 30, yf + 1, 9, "minecraft:iron_bars"),

        # 1F Undercroft Study Tables & Benches (floor_01_undercroft.jpg)
        *[fill_p(x, yf + 1, z, x + 3, yf + 1, z, "minecraft:quartz_slab") for x in (34, 39) for z in (21, 25)],
        *[fill_p(x, yf + 1, z + 1, x + 3, yf + 1, z + 1, "minecraft:light_blue_carpet") for x in (34, 39) for z in (21, 25)],
        *[fill_p(x, yf + 1, z, x + 1, yf + 1, z + 2, "minecraft:quartz_slab") for x in (46, 50) for z in (13, 19, 25)],

        # Security check & Leather sofas
        fill_p(25, yf + 1, 25, 25, yf + 1, 28, "minecraft:dark_oak_stairs[facing=east]"),
        set_p(41, yf + 1, 16, "minecraft:blue_concrete"),
        sign_p(41, yf + 2, 16, "north", "Security Check"),

        # South-East Rooms: IF-115 Control, IF-112, IF-111, Electric, Garbage Room
        fill_p(32, yf + 1, 35, 43, yc - 1, 41, "minecraft:white_concrete", "hollow"),
        fill_p(35, yf + 1, 35, 35, yc - 1, 41, "minecraft:white_concrete"),
        fill_p(39, yf + 1, 35, 39, yc - 1, 41, "minecraft:white_concrete"),
        fill_p(33, yf + 1, 35, 33, yf + 2, 35, "minecraft:air"),
        fill_p(37, yf + 1, 35, 37, yf + 2, 35, "minecraft:air"),
        fill_p(41, yf + 1, 35, 41, yf + 2, 35, "minecraft:air"),
        sign_p(33, yf + 2, 34, "north", "IF-115", "Control Room"),
        sign_p(37, yf + 2, 34, "north", "IF-112"),
        sign_p(41, yf + 2, 34, "north", "IF-111"),
        fill_p(27, yf + 1, 42, 42, yc - 1, 48, "minecraft:gray_concrete", "hollow"),
        fill_p(43, yf + 1, 42, 48, yc - 1, 48, "minecraft:light_gray_concrete", "hollow"),
        fill_p(45, yf + 1, 42, 45, yf + 2, 42, "minecraft:air"),
        sign_p(45, yf + 2, 41, "north", "Garbage Room", "ห้องแยกขยะ"),
    ]
    return cmds


def build_floor_2() -> list[str]:
    yf, yc = 6, 12
    cmds = [
        "# === FLOOR 2 (Exact Plan Layout) ===",
        *build_restrooms_sw(yf, yc),
        # NW: 2F Outdoor Astroturf Terrace (outside1.jpg)
        fill_p(2, yf, 3, 17, yf, 16, "minecraft:green_wool"),
        *[fill_p(x, yf + 1, z, x + 2, yf + 1, z, "minecraft:light_blue_concrete") for x in (6, 12) for z in (7, 12)],
        fill_p(2, yf + 1, 3, 2, yf + 1, 16, "minecraft:light_blue_stained_glass_pane"),
        fill_p(2, yf + 1, 3, 10, yf + 1, 3, "minecraft:light_blue_stained_glass_pane"),

        # West-Center: IF-208 Informatics Library
        fill_p(5, yf + 1, 17, 18, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_p(18, yf + 1, 22, 18, yf + 3, 24, "minecraft:air"),
        *[fill_p(7, yf + 1, z, 15, yf + 3, z, "minecraft:bookshelf") for z in (19, 23, 27)],
        set_p(11, yc - 1, 23, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 23, "east", "IF-208", "Informatics", "Library"),

        # Curved Conference Room IF-212
        fill_p(26, yf + 1, 5, 40, yc - 1, 16, "minecraft:white_stained_glass", "hollow"),
        fill_p(32, yf + 1, 16, 33, yf + 3, 16, "minecraft:air"),
        fill_p(30, yf + 1, 9, 36, yf + 1, 12, "minecraft:dark_oak_planks"),
        set_p(33, yc - 1, 10, "minecraft:sea_lantern"),
        sign_p(33, yf + 2, 17, "south", "IF-212", "Conference Room"),

        # Center Glass Offices IF-210 & IF-211 (2_1.jpg)
        fill_p(23, yf + 1, 20, 32, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_p(27, yf + 1, 20, 28, yf + 3, 20, "minecraft:air"),
        fill_p(25, yf + 1, 24, 30, yf + 1, 26, "minecraft:quartz_slab"),
        set_p(27, yc - 1, 25, "minecraft:sea_lantern"),
        sign_p(27, yf + 2, 19, "north", "IF-210", "Academic Office"),

        fill_p(34, yf + 1, 20, 44, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_p(38, yf + 1, 20, 39, yf + 3, 20, "minecraft:air"),
        fill_p(36, yf + 1, 24, 42, yf + 1, 26, "minecraft:quartz_slab"),
        set_p(39, yc - 1, 25, "minecraft:sea_lantern"),
        sign_p(39, yf + 2, 19, "north", "IF-211", "Informatics", "Office"),
        fill_p(34, yf + 1, 19, 36, yf + 1, 19, "minecraft:blue_concrete"),

        # Executive Wing IF-215 .. IF-219
        *[
            cmd
            for z1, z2, rname in [(3, 8, "IF-215"), (8, 13, "IF-216"), (13, 18, "IF-217"), (18, 24, "IF-218"), (24, 30, "IF-219")]
            for cmd in [
                fill_p(47, yf + 1, z1, 54, yc - 1, z2, "minecraft:white_concrete", "hollow"),
                fill_p(47, yf + 1, (z1 + z2) // 2, 47, yf + 2, (z1 + z2) // 2, "minecraft:air"),
                set_p(51, yf + 1, (z1 + z2) // 2, "minecraft:dark_oak_slab"),
                set_p(50, yc - 1, (z1 + z2) // 2, "minecraft:sea_lantern"),
                sign_p(46, yf + 2, (z1 + z2) // 2, "west", rname, "Executive Room"),
            ]
        ],

        # South-East: IF-223, Toilet, IF-220 Dining/Pantry
        fill_p(27, yf + 1, 35, 35, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(31, yf + 1, 35, 31, yf + 2, 35, "minecraft:air"),
        fill_p(36, yf + 1, 35, 42, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(39, yf + 1, 35, 39, yf + 2, 35, "minecraft:air"),
        sign_p(39, yf + 2, 34, "north", "IF-223", "Executive Room"),
        fill_p(43, yf + 1, 35, 46, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(44, yf + 1, 35, 44, yf + 2, 35, "minecraft:air"),
        fill_p(47, yf + 1, 35, 51, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(48, yf + 1, 35, 49, yf + 2, 35, "minecraft:air"),
        sign_p(49, yf + 2, 34, "north", "IF-220", "Dining/Pantry"),
    ]
    return cmds


def build_floor_3_or_4(floor_num: int, yf: int, yc: int) -> list[str]:
    prefix = f"IF-{floor_num}"
    cmds = [
        f"# === FLOOR {floor_num} (Exact Plan Layout) ===",
        *build_restrooms_west_3_to_8(yf, yc),
        # NW Computer Lab: IF-3C04 / IF-4C04
        fill_p(5, yf + 1, 6, 18, yc - 1, 26, "minecraft:light_blue_terracotta", "hollow"),
        fill_p(18, yf + 1, 14, 18, yf + 3, 16, "minecraft:air"),
        fill_p(9, yf + 1, 9, 9, yf + 1, 22, "minecraft:quartz_slab"),
        fill_p(14, yf + 1, 9, 14, yf + 1, 22, "minecraft:quartz_slab"),
        *[set_p(9, yf + 2, z, "minecraft:black_concrete") for z in range(10, 22, 2)],
        *[set_p(14, yf + 2, z, "minecraft:black_concrete") for z in range(10, 22, 2)],
        *[set_p(10, yf + 1, z, "minecraft:warped_stairs[facing=west]") for z in range(10, 22, 2)],
        *[set_p(13, yf + 1, z, "minecraft:warped_stairs[facing=east]") for z in range(10, 22, 2)],
        set_p(11, yc - 1, 15, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 15, "east", f"{prefix}C04", "Computer Lab"),

        # NE Giant 210-Seat Lecture Hall: IF-3M210 / IF-4M210
        fill_p(23, yf + 1, 3, 51, yc - 1, 19, "minecraft:white_terracotta", "hollow"),
        fill_p(23, yf + 1, 10, 23, yf + 3, 12, "minecraft:air"),
        fill_p(46, yf + 1, 19, 48, yf + 3, 19, "minecraft:air"),
        fill_p(24, yf + 2, 7, 24, yc - 1, 15, "minecraft:white_concrete"),
        fill_p(27, yf + 1, 9, 27, yf + 1, 13, "minecraft:dark_oak_planks"),
        fill_p(31, yf + 1, 5, 32, yf + 1, 17, "minecraft:warped_stairs[facing=west]"),
        fill_p(35, yf + 1, 5, 38, yf + 1, 17, "minecraft:smooth_quartz"),
        fill_p(35, yf + 2, 5, 36, yf + 2, 17, "minecraft:warped_stairs[facing=west]"),
        fill_p(39, yf + 1, 5, 44, yf + 2, 17, "minecraft:smooth_quartz"),
        fill_p(39, yf + 3, 5, 42, yf + 3, 17, "minecraft:warped_stairs[facing=west]"),
        set_p(35, yc - 1, 11, "minecraft:sea_lantern"),
        sign_p(22, yf + 2, 11, "west", f"{prefix}M210", "Lecture Hall", "210 Seats"),

        # SE 3 Deep Computer Labs: IF-xC01..03
        *[
            cmd
            for x1, x2, rname in [(23, 32, f"{prefix}C01"), (32, 41, f"{prefix}C02"), (41, 50, f"{prefix}C03")]
            for cmd in [
                fill_p(x1, yf + 1, 24, x2, yc - 1, 48, "minecraft:light_blue_terracotta", "hollow"),
                fill_p(x1 + 3, yf + 1, 24, x1 + 5, yf + 3, 24, "minecraft:air"),
                fill_p(x1 + 2, yf + 1, 28, x1 + 2, yf + 1, 44, "minecraft:quartz_slab"),
                fill_p(x2 - 2, yf + 1, 28, x2 - 2, yf + 1, 44, "minecraft:quartz_slab"),
                *[set_p(x1 + 2, yf + 2, z, "minecraft:black_concrete") for z in range(29, 44, 3)],
                *[set_p(x2 - 2, yf + 2, z, "minecraft:black_concrete") for z in range(29, 44, 3)],
                *[set_p(x1 + 3, yf + 1, z, "minecraft:warped_stairs[facing=west]") for z in range(29, 44, 3)],
                *[set_p(x2 - 3, yf + 1, z, "minecraft:warped_stairs[facing=east]") for z in range(29, 44, 3)],
                set_p((x1 + x2) // 2, yc - 1, 36, "minecraft:sea_lantern"),
                sign_p(x1 + 4, yf + 2, 23, "north", rname, "Computer Lab"),
            ]
        ],
    ]
    return cmds


def build_floor_5() -> list[str]:
    yf, yc = 22, 27
    cmds = [
        "# === FLOOR 5 (Exact Plan Layout — 2-Storey IF-5M210!) ===",
        *build_restrooms_west_3_to_8(yf, yc),
        fill_p(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_p(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in range(11, 25, 4)],
        set_p(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 25, "east", "IF-5T05", "Lecture Room"),

        # 2-Storey Tall IF-5M210
        fill_p(23, yf + 1, 3, 51, 31, 18, "minecraft:white_terracotta", "hollow"),
        fill_p(23, yf + 1, 10, 23, yf + 3, 12, "minecraft:air"),
        fill_p(24, yf + 2, 7, 24, 29, 14, "minecraft:white_concrete"),
        fill_p(27, yf + 1, 9, 27, yf + 1, 12, "minecraft:dark_oak_planks"),
        fill_p(31, yf + 1, 5, 32, yf + 1, 16, "minecraft:warped_stairs[facing=west]"),
        fill_p(35, yf + 1, 5, 38, yf + 1, 16, "minecraft:smooth_quartz"),
        fill_p(35, yf + 2, 5, 36, yf + 2, 16, "minecraft:warped_stairs[facing=west]"),
        fill_p(39, yf + 1, 5, 45, yf + 2, 16, "minecraft:smooth_quartz"),
        fill_p(39, yf + 3, 5, 43, yf + 3, 16, "minecraft:warped_stairs[facing=west]"),
        set_p(37, 30, 10, "minecraft:sea_lantern"),
        sign_p(22, yf + 2, 11, "west", "IF-5M210", "Lecture Hall", "210 Seats (2F)"),

        fill_p(23, yf + 1, 19, 27, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(27, yf + 1, 19, 37, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(31, yf + 1, 30, 33, yf + 3, 30, "minecraft:air"),
        sign_p(32, yf + 2, 31, "south", "IF-5T04", "Lecture Room"),
        fill_p(37, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(42, yf + 1, 30, 44, yf + 3, 30, "minecraft:air"),
        sign_p(43, yf + 2, 31, "south", "IF-5T03", "Lecture Room"),

        fill_p(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        sign_p(29, yf + 2, 33, "north", "IF-5T01", "Lecture Room"),
        fill_p(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        sign_p(42, yf + 2, 33, "north", "IF-5T02", "Lecture Room"),
    ]
    return cmds


def build_floor_6() -> list[str]:
    yf, yc = 27, 32
    cmds = [
        "# === FLOOR 6 (Exact Plan Layout — Striped Roof above IF-5M210) ===",
        *build_restrooms_west_3_to_8(yf, yc),
        fill_p(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_p(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in range(11, 25, 4)],
        set_p(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 25, "east", "IF-6T05", "Lecture Room"),

        # Striped corrugated metal roof deck above 5M210 (matches satellite tile!)
        fill_p(23, yc, 3, 51, yc, 18, "minecraft:gray_concrete"),
        *[fill_p(x, yc + 1, 4, x, yc + 1, 17, "minecraft:polished_andesite_slab") for x in range(24, 51, 2)],

        fill_p(23, yf + 1, 19, 27, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(27, yf + 1, 19, 37, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(31, yf + 1, 30, 33, yf + 3, 30, "minecraft:air"),
        sign_p(32, yf + 2, 31, "south", "IF-6T04", "Lecture Room"),
        fill_p(37, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(42, yf + 1, 30, 44, yf + 3, 30, "minecraft:air"),
        sign_p(43, yf + 2, 31, "south", "IF-6T03", "Lecture Room"),

        fill_p(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        sign_p(29, yf + 2, 33, "north", "IF-6T01", "Lecture Room"),
        fill_p(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        sign_p(42, yf + 2, 33, "north", "IF-6T02", "Lecture Room"),
    ]
    return cmds


def build_floor_7() -> list[str]:
    yf, yc = 32, 37
    cmds = [
        "# === FLOOR 7 (Exact Plan Layout + BUU Open House 2026 Innovation Hub!) ===",
        *build_restrooms_west_3_to_8(yf, yc),
        # IF-7T05: FabLab & Maker Space
        fill_p(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_p(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in (12, 18)],
        set_p(10, yf + 1, 15, "minecraft:crafting_table"),
        set_p(12, yf + 1, 15, "minecraft:crafter"),
        set_p(14, yf + 1, 15, "minecraft:iron_block"),
        set_p(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 25, "east", "IF-7T05", "FabLab &", "Maker Space"),

        fill_p(25, yf + 1, 19, 28, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        # IF-7T04: DMI Lab
        fill_p(28, yf + 1, 19, 38, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(32, yf + 1, 30, 34, yf + 3, 30, "minecraft:air"),
        fill_p(29, yf + 1, 20, 37, yf + 1, 29, "minecraft:cyan_carpet"),
        fill_p(30, yf + 1, 22, 35, yf + 1, 22, "minecraft:smooth_stone_slab"),
        set_p(31, yf + 2, 22, "minecraft:crafter"),
        set_p(33, yf + 2, 22, "minecraft:redstone_lamp[lit=true]"),
        set_p(35, yf + 2, 22, "minecraft:tinted_glass"),
        set_p(33, yc - 1, 24, "minecraft:sea_lantern"),
        text_p(33.0, yf + 3.2, 25.0, "IF-7T04: DMI Lab (AI/AR/VR & Industry 5.0)", 0.0, 0.75),
        sign_p(33, yf + 2, 31, "south", "IF-7T04", "DMI Lab", "AI/AR/VR Demo"),

        # IF-7T03: Vision Lab
        fill_p(38, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(43, yf + 1, 30, 45, yf + 3, 30, "minecraft:air"),
        fill_p(39, yf + 1, 20, 48, yf + 1, 29, "minecraft:light_blue_carpet"),
        fill_p(40, yf + 1, 21, 45, yf + 3, 21, "minecraft:black_concrete"),
        fill_p(41, yf + 2, 22, 44, yf + 2, 22, "minecraft:sea_lantern"),
        set_p(43, yf + 1, 26, "minecraft:iron_block"),
        set_p(43, yf + 2, 26, "minecraft:oxidized_copper"),
        set_p(43, yf + 3, 26, "minecraft:lightning_rod[facing=up]"),
        set_p(44, yf + 3, 26, "minecraft:end_rod[facing=east]"),
        set_p(41, yf + 1, 26, "minecraft:lever[face=floor,facing=north]"),
        set_p(43, yc - 1, 24, "minecraft:sea_lantern"),
        text_p(43.5, yf + 3.2, 25.0, "IF-7T03: Vision Lab (AI Vision & Robot Arm)", 0.0, 0.75),
        sign_p(44, yf + 2, 31, "south", "IF-7T03", "Vision Lab", "Robot Arm Demo"),

        # IF-7T01 & IF-7T02
        fill_p(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        fill_p(26, yf + 1, 39, 32, yf + 1, 43, "minecraft:oak_slab"),
        set_p(29, yc - 1, 41, "minecraft:sea_lantern"),
        sign_p(29, yf + 2, 33, "north", "IF-7T01", "Innovation", "Co-Working"),

        fill_p(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        fill_p(39, yf + 1, 39, 45, yf + 1, 43, "minecraft:quartz_slab"),
        set_p(42, yc - 1, 41, "minecraft:sea_lantern"),
        sign_p(42, yf + 2, 33, "north", "IF-7T02", "Open House", "Showcase"),
    ]
    return cmds


def build_floor_8() -> list[str]:
    yf, yc = 37, 42
    cmds = [
        "# === FLOOR 8 (Exact Plan Layout — IF-8R01 .. IF-8R08 Working Spaces!) ===",
        *build_restrooms_west_3_to_8(yf, yc),
        # NW Wing: IF-8R08 (North, pz=6..18) & IF-8R07 (South, pz=18..30)
        fill_p(5, yf + 1, 6, 18, yc - 1, 18, "minecraft:white_concrete", "hollow"),
        fill_p(18, yf + 1, 11, 18, yf + 3, 13, "minecraft:air"),
        fill_p(8, yf + 1, 10, 14, yf + 1, 14, "minecraft:quartz_slab"),
        set_p(11, yc - 1, 12, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 12, "east", "IF-8R08", "Eastern Software", "Park BUU"),

        fill_p(5, yf + 1, 18, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_p(18, yf + 1, 23, 18, yf + 3, 25, "minecraft:air"),
        fill_p(8, yf + 1, 22, 14, yf + 1, 26, "minecraft:quartz_slab"),
        set_p(11, yc - 1, 24, "minecraft:sea_lantern"),
        sign_p(19, yf + 2, 24, "east", "IF-8R07", "Working Space"),

        # Middle Row: IF-8R06, IF-8R05, IF-8R04 (pz=19..30)
        *[
            cmd
            for x1, x2, rname in [(24, 33, "IF-8R06"), (33, 41, "IF-8R05"), (41, 49, "IF-8R04")]
            for cmd in [
                fill_p(x1, yf + 1, 19, x2, yc - 1, 30, "minecraft:white_concrete", "hollow"),
                fill_p(x1 + 3, yf + 1, 30, x1 + 4, yf + 3, 30, "minecraft:air"),
                fill_p(x1 + 2, yf + 1, 23, x2 - 2, yf + 1, 26, "minecraft:oak_slab"),
                set_p((x1 + x2) // 2, yc - 1, 24, "minecraft:sea_lantern"),
                sign_p(x1 + 4, yf + 2, 31, "south", rname, "Working Space"),
            ]
        ],

        # South-East Row: IF-8R01, IF-8R02, IF-8R03 (pz=34..48)
        *[
            cmd
            for x1, x2, rname in [(23, 32, "IF-8R01"), (32, 41, "IF-8R02"), (41, 50, "IF-8R03")]
            for cmd in [
                fill_p(x1, yf + 1, 34, x2, yc - 1, 48, "minecraft:white_concrete", "hollow"),
                fill_p(x1 + 3, yf + 1, 34, x1 + 4, yf + 3, 34, "minecraft:air"),
                fill_p(x1 + 2, yf + 1, 39, x2 - 2, yf + 1, 43, "minecraft:oak_slab"),
                set_p((x1 + x2) // 2, yc - 1, 41, "minecraft:sea_lantern"),
                sign_p(x1 + 4, yf + 2, 33, "north", rname, "Working Space"),
            ]
        ],
    ]
    return cmds


def build_floor_9() -> list[str]:
    yf, yc = 42, 47
    cmds = [
        "# === FLOOR 9 (Lecturer Offices IF-908A..D on Upper Rectangular Tower) ===",
        *build_restrooms_9_to_11(yf, yc),
        *[
            cmd
            for x1, x2, rname in [(5, 16, "IF-908A"), (24, 36, "IF-908B"), (36, 49, "IF-908C")]
            for cmd in [
                fill_p(x1, yf + 1, 19, x2, yc - 1, 30, "minecraft:white_concrete", "hollow"),
                fill_p(x1 + 4, yf + 1, 30, x1 + 5, yf + 3, 30, "minecraft:air"),
                set_p((x1 + x2) // 2, yc - 1, 24, "minecraft:sea_lantern"),
                sign_p(x1 + 4, yf + 2, 31, "south", rname, "Lecturer Office"),
            ]
        ],
        fill_p(23, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        fill_p(35, yf + 1, 35, 35, yc - 1, 47, "minecraft:white_concrete"),
        sign_p(29, yf + 2, 33, "north", "IF-908D", "Lecturer Offices"),
    ]
    return cmds


def build_floor_10() -> list[str]:
    yf, yc = 47, 52
    cmds = [
        "# === FLOOR 10 (Exact Plan Layout — IF-1008..1011 & IF-10M32 / IF-10M60) ===",
        *build_restrooms_9_to_11(yf, yc),
        # North-West: IF-1011 (pz=19..24) & IF-1010 Dining (pz=24..29)
        fill_p(5, yf + 1, 19, 16, yc - 1, 24, "minecraft:white_concrete", "hollow"),
        fill_p(16, yf + 1, 21, 16, yf + 2, 22, "minecraft:air"),
        sign_p(17, yf + 2, 21, "east", "IF-1011"),
        fill_p(5, yf + 1, 24, 16, yc - 1, 29, "minecraft:white_concrete", "hollow"),
        fill_p(16, yf + 1, 26, 16, yf + 2, 27, "minecraft:air"),
        sign_p(17, yf + 2, 26, "east", "IF-1010", "Dining/Pantry"),

        # North-East Row: Meeting Room IF-, IF-1009 (Dining), IF-1008 (pz=19..29)
        fill_p(24, yf + 1, 19, 36, yc - 1, 29, "minecraft:white_concrete", "hollow"),
        fill_p(29, yf + 1, 29, 31, yf + 3, 29, "minecraft:air"),
        fill_p(27, yf + 1, 23, 33, yf + 1, 25, "minecraft:dark_oak_planks"),
        set_p(30, yc - 1, 24, "minecraft:sea_lantern"),
        sign_p(30, yf + 2, 30, "south", "IF- Hall", "Meeting Room"),

        fill_p(36, yf + 1, 19, 42, yc - 1, 29, "minecraft:white_concrete", "hollow"),
        fill_p(39, yf + 1, 29, 39, yf + 2, 29, "minecraft:air"),
        sign_p(39, yf + 2, 30, "south", "IF-1009", "Dining"),

        fill_p(42, yf + 1, 19, 49, yc - 1, 29, "minecraft:white_concrete", "hollow"),
        fill_p(45, yf + 1, 29, 46, yf + 2, 29, "minecraft:air"),
        sign_p(45, yf + 2, 30, "south", "IF-1008"),

        # South-East Row: IF-10M32 (Meeting 32) & IF-10M60 (Conference 60)
        fill_p(23, yf + 1, 34, 33, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(27, yf + 1, 34, 29, yf + 3, 34, "minecraft:air"),
        fill_p(26, yf + 1, 38, 30, yf + 1, 44, "minecraft:dark_oak_planks"),
        set_p(28, yc - 1, 41, "minecraft:sea_lantern"),
        sign_p(28, yf + 2, 33, "north", "IF-10M32", "Meeting Room"),

        fill_p(33, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(40, yf + 1, 34, 42, yf + 3, 34, "minecraft:air"),
        fill_p(37, yf + 1, 38, 45, yf + 1, 44, "minecraft:dark_oak_planks"),
        set_p(41, yc - 1, 41, "minecraft:sea_lantern"),
        sign_p(41, yf + 2, 33, "north", "IF-10M60", "Conference 60"),
    ]
    return cmds


def build_floor_11() -> list[str]:
    yf, yc = 52, 59
    cmds = [
        "# === FLOOR 11 (Exact Plan Layout — IF-1109 & Giant Exhibition Hall IF-11M280) ===",
        *build_restrooms_9_to_11(yf, yc),
        # NW Corner Room: IF-1109 (px=5..15, pz=19..29)
        fill_p(5, yf + 1, 19, 15, yc - 1, 29, "minecraft:white_concrete", "hollow"),
        fill_p(10, yf + 1, 29, 11, yf + 3, 29, "minecraft:air"),
        set_p(10, yc - 1, 24, "minecraft:sea_lantern"),
        sign_p(10, yf + 2, 30, "south", "IF-1109"),

        # Main Exhibition Hall IF-11M280 (px=23..50, pz=23..48)
        fill_p(23, yf + 1, 23, 50, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_p(23, yf + 1, 27, 23, yf + 3, 30, "minecraft:air"),  # Main entrance from corridor
        fill_p(34, yf + 1, 23, 36, yf + 3, 23, "minecraft:air"),  # North corridor entrance
        # Red Fire Hose Cabinet (11thFloor.jpg)
        set_p(22, yf + 1, 24, "minecraft:red_concrete"),
        set_p(22, yf + 2, 24, "minecraft:red_concrete"),
        # Exhibition Showcase Booths & Stage inside IF-11M280
        fill_p(44, yf + 1, 29, 48, yf + 1, 42, "minecraft:oak_planks"),
        *[fill_p(px, yf + 1, pz, px + 2, yf + 1, pz + 2, "minecraft:blue_concrete") for px in (27, 35) for pz in (28, 39)],
        *[set_p(px + 1, yf + 2, pz + 1, "minecraft:sea_lantern") for px in (27, 35) for pz in (28, 39)],
        *[set_p(px, yc - 1, pz, "minecraft:sea_lantern") for px in (29, 38, 46) for pz in (29, 36, 43)],
        text_p(36.0, yf + 4.5, 35.5, "IF-11M280 Exhibition Hall (Open House 2026)", -90.0, 1.1),
        sign_p(22, yf + 2, 29, "west", "IF-11M280", "Exhibition Hall", "280 Seats"),
    ]
    return cmds


def build_all_floors() -> list[str]:
    cmds = []
    cmds.extend(build_floor_1())
    cmds.extend(build_floor_2())
    cmds.extend(build_floor_3_or_4(3, 12, 17))
    cmds.extend(build_floor_3_or_4(4, 17, 22))
    cmds.extend(build_floor_5())
    cmds.extend(build_floor_6())
    cmds.extend(build_floor_7())
    cmds.extend(build_floor_8())
    cmds.extend(build_floor_9())
    cmds.extend(build_floor_10())
    cmds.extend(build_floor_11())
    return cmds
