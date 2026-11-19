"""
Exact 1:1 Floor-by-Floor Interior Layouts for Floors 1 to 7
Derived directly from the 7 official Informatics Building fire-escape floor plans
(references/floorplans/floor_01.jpg .. floor_07.jpg).

Local Building Coordinates (1 block = 1 meter):
  lx: 0 .. 54 (West -> East)   | Minecraft X = lx - 27 (-27 .. +27)
  lz: 0 .. 48 (North -> South) | Minecraft Z = lz - 24 (-24 .. +24)

Compass Alignment (Matches official map compass rose 100%):
  North (-Z, lz=0)  = Main Entrance Plaza, Wheelchair Ramp, Curved Podium & Trees
  East  (+X, lx=54) = Fueang Fa Road side
  South (+Z, lz=48) = Elevator Core, Main Staircase, Back Spine
  West  (-X, lx=0)  = Restrooms Wing & NW Wing (SMO / 2F Terrace / C04 / T05)
"""

import json


def to_mc(lx: int, lz: int) -> tuple[int, int]:
    return lx - 27, lz - 24


def fill_l(lx1: int, y1: int, lz1: int, lx2: int, y2: int, lz2: int, block: str, mode: str = "") -> str:
    x1, z1 = to_mc(lx1, lz1)
    x2, z2 = to_mc(lx2, lz2)
    xa, xb = min(x1, x2), max(x1, x2)
    ya, yb = min(y1, y2), max(y1, y2)
    za, zb = min(z1, z2), max(z1, z2)
    suffix = f" {mode}" if mode else ""
    return f"fill ~{xa} ~{ya} ~{za} ~{xb} ~{yb} ~{zb} {block}{suffix}"


def set_l(lx: int, y: int, lz: int, block: str) -> str:
    x, z = to_mc(lx, lz)
    return f"setblock ~{x} ~{y} ~{z} {block}"


def sign_l(lx: int, y: int, lz: int, facing: str, l1: str, l2: str = "", l3: str = "", l4: str = "") -> str:
    x, z = to_mc(lx, lz)
    msgs = [json.dumps(s.replace("'", ""), ensure_ascii=False) for s in (l1, l2, l3, l4)]
    nbt = "{front_text:{messages:[" + ",".join(f'\'{{"text":{m}}}\'' for m in msgs) + "]}}"
    return f"setblock ~{x} ~{y} ~{z} minecraft:oak_wall_sign[facing={facing}]{nbt}"


def text_l(lx: float, y: float, lz: float, text: str, yaw: float, scale: float = 0.85) -> str:
    x, z = lx - 27.0, lz - 24.0
    escaped = json.dumps(text, ensure_ascii=False)
    return (
        f'summon minecraft:text_display ~{x} ~{y} ~{z} '
        f'{{Tags:["if_buu_label"],text:{{text:{escaped},color:"white",bold:true}},'
        f'Rotation:[{yaw}f,0f],billboard:"fixed",background:0,'
        f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
        f'translation:[0f,0f,0f],scale:[{scale}f,{scale}f,{scale}f]}}}}'
    )


def build_restrooms_sw(yf: int, yc: int) -> list[str]:
    """1F & 2F Restrooms in SW corner (lx=0..8, lz=34..48)."""
    return [
        fill_l(0, yf + 1, 34, 8, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        # Partition Disabled / Men's / Ladies'
        fill_l(1, yf + 1, 38, 7, yc - 1, 38, "minecraft:white_concrete"),
        fill_l(1, yf + 1, 43, 7, yc - 1, 43, "minecraft:white_concrete"),
        # Doors on East side (lx=8)
        fill_l(8, yf + 1, 36, 8, yf + 2, 36, "minecraft:air"),
        fill_l(8, yf + 1, 40, 8, yf + 2, 40, "minecraft:air"),
        fill_l(8, yf + 1, 45, 8, yf + 2, 45, "minecraft:air"),
        set_l(4, yc - 1, 36, "minecraft:sea_lantern"),
        set_l(4, yc - 1, 40, "minecraft:sea_lantern"),
        set_l(4, yc - 1, 45, "minecraft:sea_lantern"),
        sign_l(9, yf + 2, 40, "east", "Restrooms", "Disabled/M/F"),
    ]


def build_restrooms_west_3_to_7(yf: int, yc: int) -> list[str]:
    """3F-7F Restrooms: Men's & Disabled (lx=0..4, lz=19..33), Ladies' (lx=0..7, lz=34..48)."""
    return [
        # Men's & Disabled along West wall North of E-W corridor
        fill_l(0, yf + 1, 19, 4, yc - 1, 33, "minecraft:white_concrete", "hollow"),
        fill_l(1, yf + 1, 29, 3, yc - 1, 29, "minecraft:white_concrete"),
        fill_l(4, yf + 1, 24, 4, yf + 2, 24, "minecraft:air"),
        fill_l(4, yf + 1, 31, 4, yf + 2, 31, "minecraft:air"),
        set_l(2, yc - 1, 24, "minecraft:sea_lantern"),
        set_l(2, yc - 1, 31, "minecraft:sea_lantern"),
        # Ladies' in SW corner
        fill_l(0, yf + 1, 34, 7, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(7, yf + 1, 40, 7, yf + 2, 41, "minecraft:air"),
        set_l(3, yc - 1, 41, "minecraft:sea_lantern"),
        sign_l(5, yf + 2, 24, "east", "Men's /", "Disabled"),
        sign_l(8, yf + 2, 41, "east", "Ladies' Room"),
    ]


def build_floor_1() -> list[str]:
    yf, yc = 0, 6
    cmds = [
        "# === FLOOR 1 (Exact Plan Layout) ===",
        *build_restrooms_sw(yf, yc),
        # NW: IF-109 Student Union (SMO) (lx=2..14, lz=3..14) + Co-Working Space (lx=5..14, lz=15..28)
        fill_l(2, yf + 1, 3, 14, yc - 1, 14, "minecraft:white_stained_glass", "hollow"),
        fill_l(14, yf + 1, 8, 14, yf + 3, 10, "minecraft:air"),
        set_l(8, yf + 1, 8, "minecraft:oak_planks"),
        set_l(8, yc - 1, 8, "minecraft:sea_lantern"),
        sign_l(15, yf + 2, 9, "east", "IF-109", "Student Union", "(SMO)"),

        # Co-working round tables (lx=5..14, lz=15..26)
        fill_l(5, yf + 1, 15, 14, yc - 1, 26, "minecraft:white_stained_glass", "hollow"),
        fill_l(14, yf + 1, 20, 14, yf + 3, 21, "minecraft:air"),
        fill_l(9, yf + 1, 20, 10, yf + 1, 21, "minecraft:oak_slab"),
        set_l(9, yc - 1, 20, "minecraft:sea_lantern"),
        sign_l(15, yf + 2, 20, "east", "Co-Working", "Space"),

        # 1F Indoor Wheelchair Ramp along North-Center Entrance (lx=23..30, lz=6..9)
        fill_l(23, yf, 6, 30, yf, 9, "minecraft:smooth_quartz_slab"),
        fill_l(23, yf + 1, 9, 30, yf + 1, 9, "minecraft:iron_bars"),

        # 1F Open Study Tables & Benches (East side lx=34..52, lz=12..30)
        *[fill_l(x, yf + 1, z, x + 3, yf + 1, z, "minecraft:quartz_slab") for x in (34, 39) for z in (21, 25)],
        *[fill_l(x, yf + 1, z + 1, x + 3, yf + 1, z + 1, "minecraft:light_blue_carpet") for x in (34, 39) for z in (21, 25)],
        *[fill_l(x, yf + 1, z, x + 1, yf + 1, z + 2, "minecraft:quartz_slab") for x in (46, 50) for z in (13, 19, 25)],

        # 1F Leather Lounge Sofas near Lobby & Security Guard Post
        fill_l(25, yf + 1, 25, 25, yf + 1, 28, "minecraft:dark_oak_stairs[facing=east]"),
        set_l(41, yf + 1, 16, "minecraft:blue_concrete"),
        sign_l(41, yf + 2, 16, "north", "Security Check"),

        # South-East Rooms: IF-115 Control, IF-112, IF-111, Electric, Garbage Room
        fill_l(27, yf + 1, 35, 42, yc - 1, 41, "minecraft:white_concrete", "hollow"),
        fill_l(32, yf + 1, 35, 32, yc - 1, 41, "minecraft:white_concrete"),
        fill_l(36, yf + 1, 35, 36, yc - 1, 41, "minecraft:white_concrete"),
        fill_l(29, yf + 1, 35, 29, yf + 2, 35, "minecraft:air"),
        fill_l(34, yf + 1, 35, 34, yf + 2, 35, "minecraft:air"),
        fill_l(39, yf + 1, 35, 39, yf + 2, 35, "minecraft:air"),
        sign_l(29, yf + 2, 34, "north", "IF-115", "Control Room"),
        sign_l(34, yf + 2, 34, "north", "IF-112"),
        sign_l(39, yf + 2, 34, "north", "IF-111"),

        # Behind IF-115..111: Server/Control + Electric + Garbage Room
        fill_l(27, yf + 1, 42, 42, yc - 1, 48, "minecraft:gray_concrete", "hollow"),
        fill_l(43, yf + 1, 42, 48, yc - 1, 48, "minecraft:light_gray_concrete", "hollow"),
        fill_l(45, yf + 1, 42, 45, yf + 2, 42, "minecraft:air"),
        sign_l(45, yf + 2, 41, "north", "Garbage Room", "ห้องแยกขยะ"),
    ]
    return cmds


def build_floor_2() -> list[str]:
    yf, yc = 6, 12
    cmds = [
        "# === FLOOR 2 (Exact Plan Layout) ===",
        *build_restrooms_sw(yf, yc),
        # NW: 2F Outdoor Astroturf Terrace (lx=2..17, lz=3..16, matching outside1.jpg!)
        fill_l(2, yf, 3, 17, yf, 16, "minecraft:green_wool"),
        # Light-blue outdoor picnic tables on astroturf (outside1.jpg)
        *[fill_l(x, yf + 1, z, x + 2, yf + 1, z, "minecraft:light_blue_concrete") for x in (6, 12) for z in (7, 12)],
        # Glass railing along West & North edge of 2F Terrace
        fill_l(2, yf + 1, 3, 2, yf + 1, 16, "minecraft:light_blue_stained_glass_pane"),
        fill_l(2, yf + 1, 3, 10, yf + 1, 3, "minecraft:light_blue_stained_glass_pane"),

        # West-Center: IF-208 Informatics Library (lx=5..18, lz=17..30)
        fill_l(5, yf + 1, 17, 18, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_l(18, yf + 1, 22, 18, yf + 3, 24, "minecraft:air"),
        *[fill_l(7, yf + 1, z, 15, yf + 3, z, "minecraft:bookshelf") for z in (19, 23, 27)],
        set_l(11, yc - 1, 23, "minecraft:sea_lantern"),
        sign_l(19, yf + 2, 23, "east", "IF-208", "Informatics", "Library"),

        # North-Center Curved Conference Room IF-212 (lx=26..40, lz=5..16)
        fill_l(26, yf + 1, 5, 40, yc - 1, 16, "minecraft:white_stained_glass", "hollow"),
        fill_l(32, yf + 1, 16, 33, yf + 3, 16, "minecraft:air"),
        fill_l(30, yf + 1, 9, 36, yf + 1, 12, "minecraft:dark_oak_planks"),
        set_l(33, yc - 1, 10, "minecraft:sea_lantern"),
        sign_l(33, yf + 2, 17, "south", "IF-212", "Conference Room"),

        # Center Glass-Walled Offices: IF-210 & IF-211 (matching 2_1.jpg!)
        fill_l(23, yf + 1, 20, 32, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_l(27, yf + 1, 20, 28, yf + 3, 20, "minecraft:air"),
        fill_l(25, yf + 1, 24, 30, yf + 1, 26, "minecraft:quartz_slab"),
        set_l(27, yc - 1, 25, "minecraft:sea_lantern"),
        sign_l(27, yf + 2, 19, "north", "IF-210", "Academic Office"),

        fill_l(34, yf + 1, 20, 44, yc - 1, 30, "minecraft:white_stained_glass", "hollow"),
        fill_l(38, yf + 1, 20, 39, yf + 3, 20, "minecraft:air"),
        fill_l(36, yf + 1, 24, 42, yf + 1, 26, "minecraft:quartz_slab"),
        set_l(39, yc - 1, 25, "minecraft:sea_lantern"),
        sign_l(39, yf + 2, 19, "north", "IF-211", "Informatics", "Office"),
        # Blue waiting chairs in front of IF-210/211 (seen in 2_1.jpg)
        fill_l(34, yf + 1, 19, 36, yf + 1, 19, "minecraft:blue_concrete"),

        # East Executive Wing: IF-215 .. IF-219 (lx=47..54, lz=3..30)
        *[
            cmd
            for idx, (z1, z2, rname) in enumerate([
                (3, 8, "IF-215"),
                (8, 13, "IF-216"),
                (13, 18, "IF-217"),
                (18, 24, "IF-218"),
                (24, 30, "IF-219"),
            ])
            for cmd in [
                fill_l(47, yf + 1, z1, 54, yc - 1, z2, "minecraft:white_concrete", "hollow"),
                fill_l(47, yf + 1, (z1 + z2) // 2, 47, yf + 2, (z1 + z2) // 2, "minecraft:air"),
                set_l(51, yf + 1, (z1 + z2) // 2, "minecraft:dark_oak_slab"),
                set_l(50, yc - 1, (z1 + z2) // 2, "minecraft:sea_lantern"),
                sign_l(46, yf + 2, (z1 + z2) // 2, "west", rname, "Executive Room"),
            ]
        ],

        # South-East: IF-223, Toilet, IF-220 Pantry/Dining
        fill_l(27, yf + 1, 35, 35, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(31, yf + 1, 35, 31, yf + 2, 35, "minecraft:air"),
        fill_l(36, yf + 1, 35, 42, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(39, yf + 1, 35, 39, yf + 2, 35, "minecraft:air"),
        sign_l(39, yf + 2, 34, "north", "IF-223", "Executive Room"),
        fill_l(43, yf + 1, 35, 46, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(44, yf + 1, 35, 44, yf + 2, 35, "minecraft:air"),
        fill_l(47, yf + 1, 35, 51, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(48, yf + 1, 35, 49, yf + 2, 35, "minecraft:air"),
        sign_l(49, yf + 2, 34, "north", "IF-220", "Dining/Pantry"),
    ]
    return cmds


def build_floor_3_or_4(floor_num: int, yf: int, yc: int) -> list[str]:
    prefix = f"IF-{floor_num}"
    cmds = [
        f"# === FLOOR {floor_num} (Exact Plan Layout) ===",
        *build_restrooms_west_3_to_7(yf, yc),
        # NW Computer Lab: IF-3C04 / IF-4C04 (lx=5..18, lz=6..26)
        fill_l(5, yf + 1, 6, 18, yc - 1, 26, "minecraft:light_blue_terracotta", "hollow"),
        fill_l(18, yf + 1, 14, 18, yf + 3, 16, "minecraft:air"),
        fill_l(9, yf + 1, 9, 9, yf + 1, 22, "minecraft:quartz_slab"),
        fill_l(14, yf + 1, 9, 14, yf + 1, 22, "minecraft:quartz_slab"),
        *[set_l(9, yf + 2, z, "minecraft:black_concrete") for z in range(10, 22, 2)],
        *[set_l(14, yf + 2, z, "minecraft:black_concrete") for z in range(10, 22, 2)],
        *[set_l(10, yf + 1, z, "minecraft:warped_stairs[facing=west]") for z in range(10, 22, 2)],
        *[set_l(13, yf + 1, z, "minecraft:warped_stairs[facing=east]") for z in range(10, 22, 2)],
        set_l(11, yc - 1, 15, "minecraft:sea_lantern"),
        sign_l(19, yf + 2, 15, "east", f"{prefix}C04", "Computer Lab"),

        # NE Giant 210-Seat Lecture Hall: IF-3M210 / IF-4M210 (lx=23..51, lz=3..19)
        fill_l(23, yf + 1, 3, 51, yc - 1, 19, "minecraft:white_terracotta", "hollow"),
        fill_l(23, yf + 1, 10, 23, yf + 3, 12, "minecraft:air"),
        fill_l(46, yf + 1, 19, 48, yf + 3, 19, "minecraft:air"),
        # Giant projector screen on West wall (lx=24) & tiered cyan seating facing West
        fill_l(24, yf + 2, 7, 24, yc - 1, 15, "minecraft:white_concrete"),
        fill_l(27, yf + 1, 9, 27, yf + 1, 13, "minecraft:dark_oak_planks"),
        fill_l(31, yf + 1, 5, 32, yf + 1, 17, "minecraft:warped_stairs[facing=west]"),
        fill_l(35, yf + 1, 5, 38, yf + 1, 17, "minecraft:smooth_quartz"),
        fill_l(35, yf + 2, 5, 36, yf + 2, 17, "minecraft:warped_stairs[facing=west]"),
        fill_l(39, yf + 1, 5, 44, yf + 2, 17, "minecraft:smooth_quartz"),
        fill_l(39, yf + 3, 5, 42, yf + 3, 17, "minecraft:warped_stairs[facing=west]"),
        set_l(35, yc - 1, 11, "minecraft:sea_lantern"),
        sign_l(22, yf + 2, 11, "west", f"{prefix}M210", "Lecture Hall", "210 Seats"),

        # SE 3 Deep Computer Labs: IF-xC01, IF-xC02, IF-xC03 (lx=23..50, lz=24..48)
        *[
            cmd
            for idx, (x1, x2, rname) in enumerate([
                (23, 32, f"{prefix}C01"),
                (32, 41, f"{prefix}C02"),
                (41, 50, f"{prefix}C03"),
            ])
            for cmd in [
                fill_l(x1, yf + 1, 24, x2, yc - 1, 48, "minecraft:light_blue_terracotta", "hollow"),
                fill_l(x1 + 3, yf + 1, 24, x1 + 5, yf + 3, 24, "minecraft:air"),
                # Two deep computer desk rows running N-S (CompRoom1.jpg)
                fill_l(x1 + 2, yf + 1, 28, x1 + 2, yf + 1, 44, "minecraft:quartz_slab"),
                fill_l(x2 - 2, yf + 1, 28, x2 - 2, yf + 1, 44, "minecraft:quartz_slab"),
                *[set_l(x1 + 2, yf + 2, z, "minecraft:black_concrete") for z in range(29, 44, 3)],
                *[set_l(x2 - 2, yf + 2, z, "minecraft:black_concrete") for z in range(29, 44, 3)],
                *[set_l(x1 + 3, yf + 1, z, "minecraft:warped_stairs[facing=west]") for z in range(29, 44, 3)],
                *[set_l(x2 - 3, yf + 1, z, "minecraft:warped_stairs[facing=east]") for z in range(29, 44, 3)],
                set_l((x1 + x2) // 2, yc - 1, 36, "minecraft:sea_lantern"),
                sign_l(x1 + 4, yf + 2, 23, "north", rname, "Computer Lab"),
            ]
        ],
    ]
    return cmds


def build_floor_5() -> list[str]:
    yf, yc = 22, 27
    cmds = [
        "# === FLOOR 5 (Exact Plan Layout — incl. 2-Storey IF-5M210 Lecture Hall!) ===",
        *build_restrooms_west_3_to_7(yf, yc),
        # NW: IF-5T05 Lecture Room (lx=5..18, lz=7..30)
        fill_l(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_l(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in range(11, 25, 4)],
        set_l(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_l(19, yf + 2, 25, "east", "IF-5T05", "Lecture Room"),

        # NE: 2-Storey Tall Giant Lecture Hall IF-5M210 (lx=23..51, lz=3..18, ceiling goes up through 6F to Y=31!)
        fill_l(23, yf + 1, 3, 51, 31, 18, "minecraft:white_terracotta", "hollow"),
        fill_l(23, yf + 1, 10, 23, yf + 3, 12, "minecraft:air"),
        fill_l(24, yf + 2, 7, 24, 29, 14, "minecraft:white_concrete"),
        fill_l(27, yf + 1, 9, 27, yf + 1, 12, "minecraft:dark_oak_planks"),
        fill_l(31, yf + 1, 5, 32, yf + 1, 16, "minecraft:warped_stairs[facing=west]"),
        fill_l(35, yf + 1, 5, 38, yf + 1, 16, "minecraft:smooth_quartz"),
        fill_l(35, yf + 2, 5, 36, yf + 2, 16, "minecraft:warped_stairs[facing=west]"),
        fill_l(39, yf + 1, 5, 45, yf + 2, 16, "minecraft:smooth_quartz"),
        fill_l(39, yf + 3, 5, 43, yf + 3, 16, "minecraft:warped_stairs[facing=west]"),
        set_l(37, 30, 10, "minecraft:sea_lantern"),
        sign_l(22, yf + 2, 11, "west", "IF-5M210", "Lecture Hall", "210 Seats (2F)"),

        # Middle Row: Small room + IF-5T04 + IF-5T03 (lz=19..30)
        fill_l(23, yf + 1, 19, 27, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(27, yf + 1, 19, 37, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(31, yf + 1, 30, 33, yf + 3, 30, "minecraft:air"),
        sign_l(32, yf + 2, 31, "south", "IF-5T04", "Lecture Room"),
        fill_l(37, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(42, yf + 1, 30, 44, yf + 3, 30, "minecraft:air"),
        sign_l(43, yf + 2, 31, "south", "IF-5T03", "Lecture Room"),

        # South-East Row: IF-5T01 & IF-5T02 (lz=34..48)
        fill_l(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        sign_l(29, yf + 2, 33, "north", "IF-5T01", "Lecture Room"),
        fill_l(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        sign_l(42, yf + 2, 33, "north", "IF-5T02", "Lecture Room"),
    ]
    return cmds


def build_floor_6() -> list[str]:
    yf, yc = 27, 32
    cmds = [
        "# === FLOOR 6 (Exact Plan Layout — NE Roof Void above IF-5M210) ===",
        *build_restrooms_west_3_to_7(yf, yc),
        # NW: IF-6T05 Lecture Room (lx=5..18, lz=7..30)
        fill_l(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_l(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in range(11, 25, 4)],
        set_l(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_l(19, yf + 2, 25, "east", "IF-6T05", "Lecture Room"),

        # NE: Corrugated/ribbed sloping roof deck above 5M210 (inaccessible void!)
        fill_l(23, yf, 3, 51, yf, 18, "minecraft:gray_concrete"),
        *[fill_l(x, yf + 1, 4, x, yf + 1, 17, "minecraft:polished_andesite_slab") for x in range(24, 51, 2)],

        # Middle Row: Small room + IF-6T04 + IF-6T03 (lz=19..30)
        fill_l(23, yf + 1, 19, 27, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(27, yf + 1, 19, 37, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(31, yf + 1, 30, 33, yf + 3, 30, "minecraft:air"),
        sign_l(32, yf + 2, 31, "south", "IF-6T04", "Lecture Room"),
        fill_l(37, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(42, yf + 1, 30, 44, yf + 3, 30, "minecraft:air"),
        sign_l(43, yf + 2, 31, "south", "IF-6T03", "Lecture Room"),

        # South-East Row: IF-6T01 & IF-6T02 (lz=34..48)
        fill_l(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        sign_l(29, yf + 2, 33, "north", "IF-6T01", "Lecture Room"),
        fill_l(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        sign_l(42, yf + 2, 33, "north", "IF-6T02", "Lecture Room"),
    ]
    return cmds


def build_floor_7() -> list[str]:
    yf, yc = 32, 37
    cmds = [
        "# === FLOOR 7 (Exact Plan Layout + BUU Open House 2026 Innovation Hub!) ===",
        *build_restrooms_west_3_to_7(yf, yc),

        # NW: IF-7T05 (lx=5..18, lz=7..30) -> FabLab & Maker Space
        fill_l(5, yf + 1, 7, 18, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(18, yf + 1, 24, 18, yf + 3, 26, "minecraft:air"),
        *[fill_l(8, yf + 1, z, 15, yf + 1, z, "minecraft:oak_slab") for z in (12, 18)],
        set_l(10, yf + 1, 15, "minecraft:crafting_table"),
        set_l(12, yf + 1, 15, "minecraft:crafter"),
        set_l(14, yf + 1, 15, "minecraft:iron_block"),
        set_l(11, yc - 1, 18, "minecraft:sea_lantern"),
        sign_l(19, yf + 2, 25, "east", "IF-7T05", "FabLab &", "Maker Space"),

        # Middle Row: Small room + IF-7T04 (DMI Lab) + IF-7T03 (Vision Lab) (lz=19..30)
        fill_l(25, yf + 1, 19, 28, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        # IF-7T04: DMI Lab (AI/AR/VR & Industry 5.0 Demo)
        fill_l(28, yf + 1, 19, 38, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(32, yf + 1, 30, 34, yf + 3, 30, "minecraft:air"),
        fill_l(29, yf + 1, 20, 37, yf + 1, 29, "minecraft:cyan_carpet"),
        fill_l(30, yf + 1, 22, 35, yf + 1, 22, "minecraft:smooth_stone_slab"),
        set_l(31, yf + 2, 22, "minecraft:crafter"),
        set_l(33, yf + 2, 22, "minecraft:redstone_lamp[lit=true]"),
        set_l(35, yf + 2, 22, "minecraft:tinted_glass"),
        set_l(33, yc - 1, 24, "minecraft:sea_lantern"),
        text_l(33.0, yf + 3.2, 25.0, "IF-7T04: DMI Lab (AI/AR/VR & Industry 5.0)", 0.0, 0.75),
        sign_l(33, yf + 2, 31, "south", "IF-7T04", "DMI Lab", "AI/AR/VR Demo"),

        # IF-7T03: Vision Lab (AI Vision in Action & Robot Arm Controls)
        fill_l(38, yf + 1, 19, 49, yc - 1, 30, "minecraft:white_concrete", "hollow"),
        fill_l(43, yf + 1, 30, 45, yf + 3, 30, "minecraft:air"),
        fill_l(39, yf + 1, 20, 48, yf + 1, 29, "minecraft:light_blue_carpet"),
        # AI Vision Monitor Wall
        fill_l(40, yf + 1, 21, 45, yf + 3, 21, "minecraft:black_concrete"),
        fill_l(41, yf + 2, 22, 44, yf + 2, 22, "minecraft:sea_lantern"),
        # Articulated Robot Arm Prop
        set_l(43, yf + 1, 26, "minecraft:iron_block"),
        set_l(43, yf + 2, 26, "minecraft:oxidized_copper"),
        set_l(43, yf + 3, 26, "minecraft:lightning_rod[facing=up]"),
        set_l(44, yf + 3, 26, "minecraft:end_rod[facing=east]"),
        set_l(41, yf + 1, 26, "minecraft:lever[face=floor,facing=north]"),
        set_l(43, yc - 1, 24, "minecraft:sea_lantern"),
        text_l(43.5, yf + 3.2, 25.0, "IF-7T03: Vision Lab (AI Vision & Robot Arm)", 0.0, 0.75),
        sign_l(44, yf + 2, 31, "south", "IF-7T03", "Vision Lab", "Robot Arm Demo"),

        # South-East Row: IF-7T01 & IF-7T02 (Co-Working & Open House Showcase) (lz=34..48)
        fill_l(23, yf + 1, 34, 36, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(28, yf + 1, 34, 30, yf + 3, 34, "minecraft:air"),
        fill_l(26, yf + 1, 39, 32, yf + 1, 43, "minecraft:oak_slab"),
        set_l(29, yc - 1, 41, "minecraft:sea_lantern"),
        sign_l(29, yf + 2, 33, "north", "IF-7T01", "Innovation", "Co-Working"),

        fill_l(36, yf + 1, 34, 49, yc - 1, 48, "minecraft:white_concrete", "hollow"),
        fill_l(41, yf + 1, 34, 43, yf + 3, 34, "minecraft:air"),
        fill_l(39, yf + 1, 39, 45, yf + 1, 43, "minecraft:quartz_slab"),
        set_l(42, yc - 1, 41, "minecraft:sea_lantern"),
        sign_l(42, yf + 2, 33, "north", "IF-7T02", "Open House", "Showcase"),
    ]
    return cmds


def build_all_floors_1_to_7() -> list[str]:
    cmds = []
    cmds.extend(build_floor_1())
    cmds.extend(build_floor_2())
    cmds.extend(build_floor_3_or_4(3, 12, 17))
    cmds.extend(build_floor_3_or_4(4, 17, 22))
    cmds.extend(build_floor_5())
    cmds.extend(build_floor_6())
    cmds.extend(build_floor_7())
    return cmds
