"""
Generate a Minecraft Java 1.21+ Datapack (world/datapacks/if_buu_1to1) — v3.0 (Floor-Plan Accurate)
Aligns the entire building directly to the official Informatics Map compass rose (floor_01..07):
  North (-Z, lz=0)  = Main Entrance Plaza, Wheelchair Ramp, Curved Podium & Trees
  East  (+X, lx=54) = Fueang Fa Road side
  South (+Z, lz=48) = Elevator Core, Main Staircase, Back Spine
  West  (-X, lx=0)  = Restrooms Wing & NW Wing (SMO / 2F Terrace / C04 / T05)

Local coordinates (lx=0..54, lz=0..48) -> Minecraft (X = lx - 27, Z = lz - 24).
"""

import json
import math
from pathlib import Path

from floorplans_1_to_7 import build_all_floors_1_to_7, fill_l, set_l, sign_l, text_l, to_mc

BASE_DIR = Path(__file__).resolve().parent.parent
SPEC_PATH = BASE_DIR / "data" / "building_spec.json"
DP_ROOT = BASE_DIR / "world" / "datapacks" / "if_buu_1to1"
FUNC_DIR = DP_ROOT / "data" / "if_buu" / "function"
TAGS_FUNC_DIR = DP_ROOT / "data" / "minecraft" / "tags" / "function"


def fill(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, block: str, mode: str = "") -> str:
    xa, xb = min(x1, x2), max(x1, x2)
    ya, yb = min(y1, y2), max(y1, y2)
    za, zb = min(z1, z2), max(z1, z2)
    suffix = f" {mode}" if mode else ""
    return f"fill ~{xa} ~{ya} ~{za} ~{xb} ~{yb} ~{zb} {block}{suffix}"


def setblock(x: int, y: int, z: int, block: str) -> str:
    return f"setblock ~{x} ~{y} ~{z} {block}"


def write_func(name: str, lines: list[str]) -> Path:
    FUNC_DIR.mkdir(parents=True, exist_ok=True)
    path = FUNC_DIR / f"{name}.mcfunction"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def gen_site_and_road() -> list[str]:
    cmds = [
        "# 01 - Site Plaza (North), Fueang Fa Road (East), Crosswalk & West Moto Parking",
        fill(-46, -1, -38, 44, -1, 34, "minecraft:grass_block"),
        # Fueang Fa Road on East (+X = 32 .. 42, Z = -38 .. 34)
        fill(32, -1, -38, 42, -1, 34, "minecraft:gray_concrete"),
        fill(37, -1, -38, 37, -1, 34, "minecraft:yellow_concrete"),
        # Pedestrian Crosswalk NE near entrance
        *[fill(33, -1, z, 41, -1, z + 1, "minecraft:white_concrete") for z in range(-32, -25, 3)],
        # Brick sidewalk along East (+X = 29 .. 31) & North entrance plaza
        fill(29, -1, -38, 31, -1, 34, "minecraft:bricks"),
        fill(-28, -1, -36, 28, -1, -24, "minecraft:light_gray_concrete"),
        # Cream concrete plaza strips (Front.jpg)
        fill(-12, -1, -36, -11, -1, -24, "minecraft:smooth_quartz"),
        fill(14, -1, -36, 15, -1, -24, "minecraft:smooth_quartz"),
        # Front granite entrance steps on North side (lx=25..42 -> X=-2..15, Z=-26..-24)
        fill(-2, 0, -26, 15, 0, -25, "minecraft:smooth_quartz_slab"),
        fill(-2, 0, -24, 15, 0, -24, "minecraft:smooth_quartz"),
        # Trees along North curve & East sidewalk (from floor_01.jpg!)
        *[fill(x, 0, -26, x, 2, -26, "minecraft:oak_log") for x in (6, 12, 18, 24)],
        *[fill(x - 1, 3, -27, x + 1, 4, -25, "minecraft:oak_leaves[persistent=true]") for x in (6, 12, 18, 24)],
        # West Motorcycle Parking lot (-44 .. -31, Z = -20 .. +22)
        fill(-44, -1, -20, -31, -1, 22, "minecraft:gray_concrete"),
        *[fill(-43, -1, z, -32, -1, z, "minecraft:white_concrete") for z in range(-16, 20, 6)],
        # Guest Spawn Pad on North Plaza looking South into entrance
        setblock(4, -1, -30, "minecraft:sea_lantern"),
        setblock(4, 0, -30, "minecraft:light_gray_carpet"),
    ]
    return cmds


def gen_basement_and_grid() -> list[str]:
    cmds = [
        "# 02 - Basement Car Park (B1) & Structural Column Grid (aligned to floor plans)",
        fill_l(5, -5, 18, 51, -1, 47, "minecraft:air"),
        fill_l(5, -6, 18, 51, -6, 47, "minecraft:gray_concrete"),
        *[fill_l(10, -6, z, 20, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        *[fill_l(30, -6, z, 46, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        fill_l(5, -5, 18, 51, -1, 18, "minecraft:stone_bricks"),
        fill_l(5, -5, 47, 51, -1, 47, "minecraft:stone_bricks"),
        fill_l(5, -5, 18, 5, -1, 47, "minecraft:stone_bricks"),
        fill_l(51, -5, 18, 51, -1, 47, "minecraft:stone_bricks"),
    ]
    # Structural columns from official floor plans
    lxs = [5, 18, 23, 32, 41, 50]
    lzs = [3, 19, 30, 34, 48]
    for lx in lxs:
        for lz in lzs:
            # Skip NE stepped-back columns above 5F (Y=26) or 6F (Y=31)
            if lx >= 32 and lz == 3:
                top_y = 26
            else:
                top_y = 58
            cmds.append(fill_l(lx, -5, lz, lx, top_y, lz, "minecraft:white_concrete"))
    return cmds


def gen_slabs_and_core(spec: dict) -> list[str]:
    cmds = ["# 03 - 11 Floor Slabs (exact floor footprints), Main/Fire Stairs & Glass Elevator Lobbies"]
    floors = spec["floors"]

    for fl in floors:
        fid = fl["id"]
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        if fid in ("B1", "RF"):
            continue

        mat = "minecraft:smooth_sandstone" if fid in ("1F", "2F", "11F") else "minecraft:smooth_quartz"

        if fid in ("1F", "2F"):
            # Full footprint with SW restrooms + NW wing + curved NE front
            cmds.append(fill_l(0, yf, 34, 53, yf, 48, mat))
            cmds.append(fill_l(2, yf, 3, 52, yf, 33, mat))
            if fid == "1F":
                cmds.append(fill_l(22, yf, 0, 52, yf, 3, mat))
        elif fid in ("3F", "4F", "5F"):
            # Main tower + NE Podium hall (3M210 / 4M210 / 5M210)
            cmds.append(fill_l(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_l(5, yf, 6, 51, yf, 18, mat))
            cmds.append(fill_l(11, yf, 0, 51, yf, 5, mat))
        elif fid == "6F":
            # Skip 6F floor slab inside 2-storey void above IF-5M210 (lx=24..50, lz=4..17)!
            cmds.append(fill_l(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_l(5, yf, 6, 22, yf, 18, mat))
            cmds.append(fill_l(11, yf, 0, 22, yf, 5, mat))
        else:
            # 7F - 11F: NE corner stepped back completely (open air above 5M210!)
            cmds.append(fill_l(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_l(5, yf, 6, 23, yf, 18, mat))
            cmds.append(fill_l(11, yf, 0, 23, yf, 5, mat))

        # Accent floor tiles in corridors & lobbies (matching VR Tour panoramas)
        if fid in ("1F", "2F", "7F", "11F"):
            for lx in range(19, 50, 4):
                cmds.append(set_l(lx, yf, 32, "minecraft:gray_concrete" if lx % 8 == 0 else "minecraft:light_gray_concrete"))
            for lz in range(8, 36, 4):
                cmds.append(set_l(20, yf, lz, "minecraft:gray_concrete" if lz % 8 == 0 else "minecraft:light_gray_concrete"))

        # Corridor ceiling lights (N-S & E-W corridors)
        for lz in range(6, 36, 5):
            cmds.append(set_l(20, yc - 1, lz, "minecraft:sea_lantern"))
        for lx in range(14, 50, 5):
            cmds.append(set_l(lx, yc - 1, 32, "minecraft:sea_lantern"))

    # --- 3 Passenger Elevators (lx=15..18, lz=36..48) + Fireman's Elevator (lx=22..26, lz=39..48) ---
    cmds.append(fill_l(15, -5, 36, 18, 58, 48, "minecraft:light_gray_concrete", "hollow"))
    cmds.append(fill_l(22, -5, 39, 26, 58, 48, "minecraft:light_gray_concrete", "hollow"))

    for idx, fl in enumerate(floors):
        if fl["id"] == "RF":
            continue
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        fid = fl["id"]

        # 3 Elevator openings facing East (lx=18) into Elevator Lobby (lx=19..21)
        for ez in (38, 42, 46):
            cmds.append(fill_l(18, yf + 1, ez, 18, yf + 3, ez, "minecraft:air"))
            cmds.append(fill_l(17, yf + 1, ez, 17, yf + 3, ez, "minecraft:iron_block"))
        # Fireman's elevator door facing North (lz=39)
        cmds.append(fill_l(24, yf + 1, 39, 24, yf + 3, 39, "minecraft:air"))
        cmds.append(fill_l(24, yf + 1, 40, 24, yf + 3, 40, "minecraft:iron_block"))

        if fid != "B1":
            # Authentic Glass-Walled Elevator Lobby (Lift.jpg & 7thFloor.jpg) at lx=19..21, lz=35..46
            cmds.append(fill_l(19, yc - 1, 35, 21, yc - 1, 46, "minecraft:blue_terracotta"))
            cmds.append(fill_l(19, yc - 1, 35, 21, yc - 1, 36, "minecraft:stripped_oak_wood"))
            # Glass double-door front at lz=35
            cmds.append(fill_l(19, yf + 1, 35, 21, yc - 1, 35, "minecraft:white_stained_glass"))
            cmds.append(fill_l(20, yf + 1, 35, 21, yf + 3, 35, "minecraft:air"))
            cmds.append(set_l(20, yc - 1, 40, "minecraft:sea_lantern"))
            # 4-color recycling bins near lobby
            cmds.append(set_l(22, yf + 1, 36, "minecraft:yellow_concrete"))
            cmds.append(set_l(22, yf + 1, 37, "minecraft:blue_concrete"))
            cmds.append(set_l(23, yf + 1, 36, "minecraft:green_concrete"))
            cmds.append(set_l(23, yf + 1, 37, "minecraft:red_concrete"))

        # Yellow Star Floor Sign right at Elevator Lobby (lx=19, lz=36)
        cmds.append(sign_l(19, yf + 2, 37, "east", f"[ {fid} ]", fl["name"][:15], "/trigger", "if_floor set 1..11"))

        # --- Walkable Main Staircase (lx=9..14, lz=35..48) ---
        if idx < len(floors) - 2:
            next_yf = floors[idx + 1]["y_floor"]
            height = next_yf - yf
            cmds.append(fill_l(9, next_yf, 36, 13, next_yf, 44, "minecraft:air"))
            cmds.append(fill_l(9, yf + 1, 35, 14, next_yf, 35, "minecraft:white_concrete"))
            cmds.append(fill_l(9, yf + 1, 35, 11, yf + 3, 35, "minecraft:air"))  # entrance from corridor
            for s in range(height):
                sz = 37 + min(s, 6)
                cmds.append(fill_l(9, yf + 1 + s, sz, 13, yf + 1 + s, sz, "minecraft:smooth_quartz_stairs[facing=south]"))

            # --- NNW Fire Exit Staircase (lx=12..18, lz=0..4) ---
            cmds.append(fill_l(12, next_yf, 1, 17, next_yf, 3, "minecraft:air"))
            for s in range(height):
                sx = 17 - min(s, 5)
                cmds.append(fill_l(sx, yf + 1 + s, 1, sx, yf + 1 + s, 3, "minecraft:stone_brick_stairs[facing=west]"))

            # --- SE Fire Exit Staircase (lx=50..53, lz=35..45) ---
            cmds.append(fill_l(51, next_yf, 36, 52, next_yf, 43, "minecraft:air"))
            for s in range(height):
                sz = 37 + min(s, 6)
                cmds.append(fill_l(51, yf + 1 + s, sz, 52, yf + 1 + s, sz, "minecraft:stone_brick_stairs[facing=south]"))

    # Enclose NNW & SE Fire Stairwells
    cmds.append(fill_l(11, -5, 0, 18, 58, 4, "minecraft:light_gray_concrete", "hollow"))
    for fl in floors:
        if fl["id"] == "RF":
            continue
        yf = fl["y_floor"]
        cmds.append(fill_l(18, yf + 1, 2, 18, yf + 2, 3, "minecraft:air"))  # NNW exit door to corridor
        cmds.append(fill_l(50, yf + 1, 32, 50, yf + 2, 33, "minecraft:air"))  # SE exit door
    return cmds


def gen_podium_and_arch() -> list[str]:
    cmds = [
        "# 04 - Curved North/NE Podium (1F-5F) & 5-Ribbed Sweeping C-Shaped Canopy Arch",
        # North Entrance Terrace & Canopy Pillars (lx=21..52, lz=-5..4)
        fill_l(22, 0, -4, 52, 0, 4, "minecraft:smooth_sandstone"),
        # Cobalt Blue Entrance Core Wall on NE side (seen in Front.jpg & SMO.jpg!)
        fill_l(47, 0, 1, 52, 11, 4, "minecraft:blue_concrete"),

        # Left (East) cluster of 6 slender white pillars under oculus skylight (Front.jpg)
        fill_l(46, 0, -4, 46, 21, -4, "minecraft:quartz_pillar"),
        fill_l(48, 0, -5, 48, 21, -5, "minecraft:quartz_pillar"),
        fill_l(50, 0, -4, 50, 21, -4, "minecraft:quartz_pillar"),
        fill_l(47, 0, -2, 47, 21, -2, "minecraft:quartz_pillar"),
        fill_l(49, 0, -2, 49, 21, -2, "minecraft:quartz_pillar"),
        # Right (West) tall white pillar
        fill_l(23, 0, -3, 23, 21, -3, "minecraft:quartz_pillar"),

        # Podium Upper Facade Box on North face (lx=24..50, lz=1..2, Y=12..21)
        fill_l(24, 12, 1, 50, 21, 1, "minecraft:light_gray_concrete"),
        fill_l(24, 15, 1, 50, 15, 1, "minecraft:polished_andesite"),
        fill_l(24, 18, 1, 50, 18, 1, "minecraft:polished_andesite"),
        fill_l(24, 12, 1, 31, 13, 1, "minecraft:air"),  # angled underside on West
        fill_l(27, 16, 1, 32, 16, 1, "minecraft:blue_concrete"),
        fill_l(40, 17, 1, 46, 17, 1, "minecraft:blue_concrete"),
        fill_l(34, 15, 1, 39, 15, 1, "minecraft:light_blue_stained_glass"),
        fill_l(28, 19, 1, 33, 19, 1, "minecraft:light_blue_stained_glass"),
    ]

    # Sweeping Curved North Canopy Roof (Y=22..23, lx=21..53, lz=-6..6)
    for lx in range(21, 54):
        lz_min = -6 if lx <= 42 else round(-6 + (lx - 42) * 0.5)
        cmds.append(fill_l(lx, 22, lz_min, lx, 22, 5, "minecraft:smooth_quartz"))
        cmds.append(fill_l(lx, 23, lz_min, lx, 23, 5, "minecraft:light_gray_concrete"))

    # Oculus cutout above 6 pillars
    cmds.append(fill_l(47, 22, -4, 49, 23, -2, "minecraft:air"))

    # 5 Ribbed Silver C-Arch Fins curving down on East/NE side (lx=46..54)
    fin_lzs = [-3, -1, 1, 3, 5]
    seen_pts = set()
    for deg in range(-70, 195, 2):
        rad = math.radians(deg)
        clx = round(47 + 7.5 * math.sin(rad))
        cy = round(14.5 + 8.0 * math.cos(rad))
        for clz in fin_lzs:
            for dz in (0, 1):
                pt = (clx, cy, clz + dz)
                if pt not in seen_pts:
                    seen_pts.add(pt)
                    mat = "minecraft:smooth_quartz" if dz == 0 else "minecraft:light_gray_concrete"
                    cmds.append(set_l(clx, cy, clz + dz, mat))

    # Podium Front Sign (facing North -Z -> yaw=180)
    cmds.append(text_l(38.0, 18.5, 0.3, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", 180.0, 1.35))
    return cmds


def gen_facade_shell() -> list[str]:
    cmds = [
        "# 05 - v3.0 Exterior Tower Shell Aligned to Floor Plans (N=-Z, E=+X, S=+Z, W=-X)",
        # West Facade (lx=0, lz=19..48 & lx=5, lz=6..18)
        fill_l(0, 1, 19, 0, 58, 48, "minecraft:light_gray_concrete", "keep"),
        fill_l(5, 1, 6, 5, 58, 18, "minecraft:light_gray_concrete", "keep"),
        *[fill_l(5, y + 1, 8, 5, y + 3, 17, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],

        # South Back Spine Facade (lz=48, lx=0..53)
        fill_l(0, 1, 48, 53, 58, 48, "minecraft:light_gray_concrete", "keep"),
        *[fill_l(25, y + 1, 48, 48, y + 3, 48, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],

        # East Facade facing Fueang Fa Road (lx=53 up to 5F/6F on North half; lx=53 on lz=19..48 up to 11F)
        fill_l(53, 1, 19, 53, 58, 48, "minecraft:light_gray_concrete", "keep"),
        *[fill_l(53, y + 1, 21, 53, y + 3, 46, "minecraft:light_blue_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],
        # Dark horizontal window mullions & Cobalt Blue vertical stripes on East corners
        fill_l(53, 0, 47, 54, 58, 48, "minecraft:blue_concrete"),
        fill_l(51, 0, 3, 52, 26, 4, "minecraft:blue_concrete"),

        # North Tower Facade (above 6F-11F step-back at lz=19, lx=24..53, and NW wing at lz=6, lx=5..23)
        fill_l(5, 1, 6, 23, 58, 6, "minecraft:light_gray_concrete", "keep"),
        *[fill_l(7, y + 1, 6, 17, y + 3, 6, "minecraft:light_blue_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],
        fill_l(24, 32, 19, 53, 58, 19, "minecraft:light_blue_stained_glass", "keep"),
        *[fill_l(x, 32, 19, x, 58, 19, "minecraft:gray_concrete") for x in range(24, 54, 5)],
        # Cobalt blue strip on NW corner & NE stepped-back corner
        fill_l(4, 0, 6, 5, 58, 7, "minecraft:blue_concrete"),
        fill_l(23, 32, 18, 24, 58, 19, "minecraft:blue_concrete"),

        # Protruding 3-storey glass box at 6F-8F overlooking step-back terrace (lx=21..27, lz=14..20, Y=27..41)
        fill_l(21, 27, 14, 27, 41, 20, "minecraft:light_blue_stained_glass", "hollow"),
        fill_l(21, 32, 14, 27, 32, 20, "minecraft:white_concrete"),
        fill_l(21, 37, 14, 27, 37, 20, "minecraft:white_concrete"),

        # White projecting floor ledges along North & East tower faces
        *[fill_l(5, y, 5, 24, y, 5, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],
        *[fill_l(24, y, 18, 54, y, 18, "minecraft:smooth_quartz") for y in (32, 37, 42, 47, 52)],
        *[fill_l(54, y, 18, 54, y, 49, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],
    ]
    return cmds


def gen_roof_and_solar() -> list[str]:
    cmds = [
        "# 06 - v3.0 Roof Overhang, Attic Band, 3D Faculty Sign & 3 Solar Panel Arrays",
        fill_l(0, 59, 19, 53, 59, 48, "minecraft:gray_concrete"),
        fill_l(5, 59, 6, 23, 59, 18, "minecraft:gray_concrete"),
        # Light-gray attic facade band on North & East faces (Y=59..61)
        fill_l(24, 59, 18, 53, 61, 18, "minecraft:light_gray_concrete"),
        fill_l(54, 59, 18, 54, 61, 48, "minecraft:light_gray_concrete"),
        # Overhanging flat roof canopy (Y=63..64)
        fill_l(-1, 63, 17, 55, 63, 49, "minecraft:light_gray_concrete"),
        fill_l(4, 63, 4, 25, 63, 17, "minecraft:light_gray_concrete"),
        fill_l(-1, 64, 17, 55, 64, 49, "minecraft:polished_deepslate"),
        fill_l(4, 64, 4, 25, 64, 17, "minecraft:polished_deepslate"),
        # Gold seal & crisp 3D text_display sign facing North (-Z -> yaw=180) and East (+X -> yaw=-90)
        fill_l(33, 60, 17, 34, 61, 17, "minecraft:gold_block"),
        text_l(42.0, 60.6, 16.8, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", 180.0, 2.0),
        text_l(55.2, 60.6, 33.0, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", -90.0, 2.0),
        # 3 Rows of Solar Panels on 11F roof (matching ESRI z19 satellite!)
        fill_l(8, 65, 24, 46, 65, 27, "minecraft:daylight_detector"),
        fill_l(8, 65, 31, 46, 65, 34, "minecraft:daylight_detector"),
        fill_l(8, 65, 38, 46, 65, 41, "minecraft:daylight_detector"),
    ]
    return cmds


def gen_interiors() -> list[str]:
    cmds = [
        "# 07 - v3.0 Exact Floor-Plan Interiors (1F-7F) + Baseline Floors (8F-11F)",
        *build_all_floors_1_to_7(),

        # --- Baseline Floors 8F-11F (awaiting user's floor_08..11 plans!) ---
        # 8F (Y=37): Research Labs & Eastern Software Park BUU (IF-8R08)
        fill_l(23, 38, 34, 49, 41, 48, "minecraft:white_concrete", "hollow"),
        fill_l(28, 38, 34, 30, 40, 34, "minecraft:air"),
        sign_l(29, 39, 33, "north", "IF-8R08", "Eastern Software", "Park BUU"),

        # 9F (Y=42): Lecturer Offices (IF-908A..D)
        *[fill_l(x, 43, 34, x, 46, 48, "minecraft:white_concrete") for x in (28, 35, 42)],
        sign_l(29, 44, 33, "north", "9F Offices", "IF-908A - D"),

        # 10F (Y=47): Hall of Fame & Conference Rooms (IF-10M56 / IF-10M60)
        fill_l(23, 48, 19, 49, 51, 30, "minecraft:white_concrete", "hollow"),
        fill_l(34, 48, 30, 36, 50, 30, "minecraft:air"),
        fill_l(30, 48, 23, 42, 48, 26, "minecraft:dark_oak_planks"),
        *[set_l(x, 48, 35, "minecraft:quartz_pillar") for x in (26, 30, 34)],
        *[set_l(x, 49, 35, "minecraft:gold_block") for x in (26, 30, 34)],
        sign_l(35, 49, 31, "south", "IF-10M56 / 60", "Conference &", "Hall of Fame"),

        # 11F (Y=52): Exhibition Hall (IF-11M280) + Red Fire Hose Cabinets
        set_l(22, 53, 31, "minecraft:red_concrete"),
        set_l(22, 54, 31, "minecraft:red_concrete"),
        *[fill_l(x, 53, 38, x + 2, 53, 40, "minecraft:blue_concrete") for x in (26, 34, 42)],
        *[set_l(x + 1, 54, 39, "minecraft:sea_lantern") for x in (26, 34, 42)],
        sign_l(23, 54, 33, "north", "11F Exhibition", "Hall IF-11M280", "Open House 2026"),
    ]
    return cmds


def gen_campus_context() -> list[str]:
    cmds = [
        "# 09 - v3.0 Surrounding BUU Campus Landmarks (NW Fountain, South Bldg, East Comp Center)",
        # NW Circular Fountain Plaza (X=-56..-32, Z=-46..-22)
        fill(-56, -1, -46, -32, -1, -22, "minecraft:light_gray_concrete"),
    ]
    for dx in range(-10, 11):
        for dz in range(-10, 11):
            r = math.hypot(dx, dz)
            px, pz = -44 + dx, -34 + dz
            if r <= 6.5:
                cmds.append(setblock(px, -1, pz, "minecraft:water"))
            elif r <= 8.5:
                cmds.append(setblock(px, 0, pz, "minecraft:smooth_quartz_slab"))
                cmds.append(setblock(px, -1, pz, "minecraft:smooth_quartz"))

    # South Adjacent 5-Storey Gray/Blue Building (Z = +32..+52, X = -24..+22)
    cmds.extend([
        fill(-24, -1, 32, 22, -1, 52, "minecraft:light_gray_concrete"),
        fill(-24, 0, 32, 22, 24, 52, "minecraft:light_gray_concrete", "hollow"),
        fill(-4, 1, 32, 6, 23, 32, "minecraft:light_blue_concrete"),
        *[fill(x, y, 32, x + 2, y + 1, 32, "minecraft:black_stained_glass") for y in (4, 9, 14, 19) for x in range(-20, 18, 8)],
        fill(-25, 25, 31, 23, 25, 53, "minecraft:gray_concrete"),
    ])

    # East Across Fueang Fa Rd: Computer Center / Science CL Frontage (X = +46..+66, Z = -28..+24)
    cmds.extend([
        fill(43, -1, -34, 68, -1, 28, "minecraft:grass_block"),
        fill(43, -1, -28, 46, -1, 24, "minecraft:light_gray_concrete"),
        fill(47, 0, -2, 65, 18, 22, "minecraft:white_concrete", "hollow"),
        *[fill(47, y, 0, 47, y, 20, "minecraft:cyan_stained_glass") for y in (3, 7, 11, 15)],
        fill(45, 19, -4, 66, 19, 23, "minecraft:cyan_concrete"),
        fill(47, 0, -28, 65, 16, -6, "minecraft:smooth_sandstone", "hollow"),
        *[fill(47, y, -25, 47, y, -9, "minecraft:black_stained_glass") for y in (3, 8, 13)],
        fill(46, 17, -29, 66, 17, -5, "minecraft:gray_concrete"),
    ])
    return cmds


def gen_interactive_openhouse(spec: dict) -> dict[str, list[str]]:
    init_cmds = [
        "# Setup Open House /trigger elevator scoreboard and spawn origin marker",
        "scoreboard objectives add if_floor trigger",
        "kill @e[type=minecraft:marker,tag=if_buu_origin]",
        'summon minecraft:marker ~0 ~0 ~0 {Tags:["if_buu_origin"]}',
        "scoreboard players enable @a if_floor",
    ]

    menu_lines = [
        'tellraw @s [{"text":"\\n=== ลิฟต์อาคารคณะวิทยาการสารสนเทศ (IF-BUU 1:1 v3.0) ===","color":"aqua","bold":true}]',
        'tellraw @s [{"text":"พิมพ์ /trigger if_floor set <เลขชั้น> หรือคลิกชั้นที่ต้องการ:","color":"gray"}]',
    ]

    tick_cmds = [
        "scoreboard players enable @a if_floor",
    ]

    floor_num_map = [
        (0, "B1", -5, "ลานจอดรถใต้ดิน (Basement Car Park)"),
        (1, "1F", 0, "โถงกิจกรรม / สโมสรนิสิต IF-109 / Co-Working / IF-111..115"),
        (2, "2F", 6, "ห้องสมุด IF-208 / สำนักงาน IF-210..211 / ผู้บริหาร IF-215..223"),
        (3, "3F", 12, "ห้องคอมฯ IF-3C01..04 / ห้องบรรยาย IF-3M210"),
        (4, "4F", 17, "ห้องคอมฯ IF-4C01..04 / ห้องบรรยาย IF-4M210"),
        (5, "5F", 22, "ห้องบรรยาย IF-5T01..05 / ห้องบรรยาย 2 ชั้น IF-5M210"),
        (6, "6F", 27, "ห้องบรรยาย IF-6T01..05"),
        (7, "7F", 32, "★ Open House Innovation Hub (IF-7T01..05: Vision/DMI/FabLab)"),
        (8, "8F", 37, "ห้องปฏิบัติการวิจัย / Eastern Software Park BUU"),
        (9, "9F", 42, "ห้องพักอาจารย์ IF-908A..D"),
        (10, "10F", 47, "ห้องเกียรติยศ (Hall of Fame) / ห้องประชุม"),
        (11, "11F", 52, "ห้องนิทรรศการ Exhibition Hall (IF-11M280)"),
    ]

    # Elevator Lobby Star is at local (lx=20, lz=36) -> Minecraft (-7, +12), facing North (yaw=180)
    el_x, el_z = to_mc(20, 36)

    for num, code, y_fl, desc in floor_num_map:
        tp_y = y_fl + 1
        score_val = 99 if num == 0 else num
        color = "green" if num == 7 else "gold"
        menu_lines.append(
            f'tellraw @s [{{"text":"[{code}] ","color":"{color}","bold":true,'
            f'"click_event":{{"action":"run_command","command":"/trigger if_floor set {score_val}"}}}},'
            f'{{"text":"{desc}","color":"white"}}]'
        )
        tick_cmds.append(
            f"execute as @a[scores={{if_floor={score_val}}}] at @e[type=minecraft:marker,tag=if_buu_origin,limit=1] "
            f"run tp @s ~{el_x} ~{tp_y} ~{el_z} 180 0"
        )
        tick_cmds.append(
            f'execute as @a[scores={{if_floor={score_val}}}] run title @s actionbar '
            f'{{"text":"ชั้น {code} — {desc}","color":"aqua"}}'
        )
        tick_cmds.append(f"scoreboard players reset @a[scores={{if_floor={score_val}}}] if_floor")

    guide_cmds = [
        "function if_buu:elevator_menu",
        'tellraw @s [{"text":"[7F Innovation Hub] ","color":"green","bold":true,'
        '"click_event":{"action":"run_command","command":"/trigger if_floor set 7"}},'
        '{"text":"กดเพื่อวาร์ปไปยังชั้น 7 โซนจัดแสดง BUU Open House 2026!","color":"gray"}]',
    ]

    return {
        "init_openhouse": init_cmds,
        "elevator_menu": menu_lines,
        "elevator_tick": tick_cmds,
        "give_guide": guide_cmds,
    }


def main():
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    DP_ROOT.mkdir(parents=True, exist_ok=True)
    FUNC_DIR.mkdir(parents=True, exist_ok=True)
    TAGS_FUNC_DIR.mkdir(parents=True, exist_ok=True)

    pack_meta = {
        "pack": {
            "pack_format": 48,
            "supported_formats": {"min_inclusive": 26, "max_inclusive": 120},
            "min_format": 26,
            "max_format": 120,
            "description": "IF-BUU 1:1 Craft v3.0 — Floor-Plan Accurate Interiors (1F-7F)",
        }
    }
    (DP_ROOT / "pack.mcmeta").write_text(json.dumps(pack_meta, indent=2), encoding="utf-8")

    write_func("01_site_road", gen_site_and_road())
    write_func("02_basement_and_grid", gen_basement_and_grid())
    write_func("03_slabs_and_core", gen_slabs_and_core(spec))
    write_func("04_podium_and_arch", gen_podium_and_arch())
    write_func("05_facade_shell", gen_facade_shell())
    write_func("06_roof_and_solar", gen_roof_and_solar())
    write_func("07_interiors", gen_interiors())
    write_func("09_campus_context", gen_campus_context())

    interactive = gen_interactive_openhouse(spec)
    for fname, flines in interactive.items():
        write_func(fname, flines)

    (TAGS_FUNC_DIR / "tick.json").write_text(json.dumps({"values": ["if_buu:elevator_tick"]}, indent=2), encoding="utf-8")
    (TAGS_FUNC_DIR / "load.json").write_text(json.dumps({"values": ["if_buu:init_openhouse"]}, indent=2), encoding="utf-8")

    clear_cmds = ["# Clear 1:1 building + surrounding campus context before rebuilding"]
    for y_start, y_end in [(-6, 4), (5, 15), (16, 26), (27, 37), (38, 48), (49, 59), (60, 68)]:
        for x_start, x_end in [(-60, -30), (-29, 0), (1, 30), (31, 68)]:
            for z_start, z_end in [(-50, -20), (-19, 15), (16, 54)]:
                clear_cmds.append(fill(x_start, y_start, z_start, x_end, y_end, z_end, "minecraft:air"))
    clear_cmds.append("kill @e[type=minecraft:marker,tag=if_buu_origin]")
    clear_cmds.append("kill @e[type=minecraft:text_display,tag=if_buu_label]")
    clear_cmds.append('tellraw @a {"text":"[IF-BUU 1:1 v3.0] Cleared building & campus zone.","color":"yellow"}')
    write_func("clear_area", clear_cmds)

    write_func(
        "build_all",
        [
            "kill @e[type=minecraft:text_display,tag=if_buu_label]",
            "function if_buu:01_site_road",
            "function if_buu:02_basement_and_grid",
            "function if_buu:03_slabs_and_core",
            "function if_buu:04_podium_and_arch",
            "function if_buu:05_facade_shell",
            "function if_buu:06_roof_and_solar",
            "function if_buu:07_interiors",
            "function if_buu:09_campus_context",
            "function if_buu:init_openhouse",
            'tellraw @a {"text":"[IF-BUU 1:1 v3.0] Built Floor-Plan Accurate 1F-7F + Campus Context!","color":"aqua"}',
        ],
    )

    print(f"Generated v3.0 Floor-Plan Accurate Datapack -> {DP_ROOT}")
    for f in sorted(FUNC_DIR.glob("*.mcfunction")):
        line_count = len(f.read_text(encoding="utf-8").splitlines())
        print(f"  - if_buu:{f.stem} ({line_count} lines)")


if __name__ == "__main__":
    main()
