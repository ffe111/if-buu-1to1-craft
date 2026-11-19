"""
Generate a Minecraft Java 1.21+ Datapack (world/datapacks/if_buu_1to1) — v3.0
True Google Maps / Satellite Orientation (90 deg Clockwise from Fire-Escape Maps):
  East  (+X, pz=0)  = Fueang Fa Road, Main Entrance Plaza, Curved Podium & C-Arch
  West  (-X, pz=48) = Elevator/Main Stair Spine & West Motorcycle Parking
  North (-Z, px=0)  = Restrooms Wing, 11F Solar Roof & 8F NW Wing
  South (+Z, px=54) = SE C-Arch Fins (6 ribs), IF-5M210 Striped Roof & South 5F Bldg

All 11 floors (B1, 1F-8F, 9F, 10F, 11F) mapped from official floor plans + site photos.
"""

import json
import math
from pathlib import Path

from floorplans_all import build_all_floors, fill_p, set_p, sign_p, text_p, to_mc

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
        "# 01 - Fueang Fa Rd (East +X), Entrance Plaza, Crosswalk, Moto Parking (West -X & SE Bay)",
        fill(-46, -1, -34, 46, -1, 34, "minecraft:grass_block"),
        # Fueang Fa Road running North-South on East (+X = 33 .. 43)
        fill(33, -1, -34, 43, -1, 34, "minecraft:gray_concrete"),
        fill(38, -1, -34, 38, -1, 34, "minecraft:yellow_concrete"),
        # Pedestrian Crosswalk North-East
        *[fill(34, -1, z, 42, -1, z + 1, "minecraft:white_concrete") for z in range(-28, -21, 3)],
        # Brick sidewalk (+X = 30 .. 32)
        fill(30, -1, -34, 32, -1, 34, "minecraft:bricks"),
        # East Front Plaza (+X = 24 .. 29, Z = -28 .. +28)
        fill(24, -1, -28, 29, -1, 28, "minecraft:light_gray_concrete"),
        fill(24, -1, -12, 29, -1, -11, "minecraft:smooth_quartz"),
        fill(24, -1, 14, 29, -1, 15, "minecraft:smooth_quartz"),
        # Front granite entrance steps on East face (px=25..42 -> Z=-2..15, X=24..26)
        fill(25, 0, -2, 26, 0, 15, "minecraft:smooth_quartz_slab"),
        fill(24, 0, -2, 24, 0, 15, "minecraft:smooth_quartz"),
        # SE Under-Wall Motorcycle Parking Bay (seen in c_arch_closeup.jpg!)
        fill(16, -1, 25, 29, -1, 31, "minecraft:gray_concrete"),
        *[fill(x, -1, 26, x, -1, 30, "minecraft:white_concrete") for x in range(18, 29, 3)],
        # Trees along East sidewalk & front plaza
        *[fill(31, 0, z, 31, 2, z, "minecraft:oak_log") for z in (-18, -10, 6, 14)],
        *[fill(30, 3, z - 1, 32, 4, z + 1, "minecraft:oak_leaves[persistent=true]") for z in (-18, -10, 6, 14)],
        # West Motorcycle Parking lot (-44 .. -28, Z = -22 .. +22)
        fill(-44, -1, -22, -28, -1, 22, "minecraft:gray_concrete"),
        *[fill(-43, -1, z, -29, -1, z, "minecraft:white_concrete") for z in range(-18, 20, 6)],
        # Guest Spawn Pad on East Plaza facing West into the entrance
        setblock(30, -1, 5, "minecraft:sea_lantern"),
        setblock(30, 0, 5, "minecraft:light_gray_carpet"),
    ]
    return cmds


def gen_basement_and_grid() -> list[str]:
    cmds = [
        "# 02 - Basement Car Park (B1) & Structural Column Grid (True Satellite Orientation)",
        fill_p(5, -5, 18, 51, -1, 47, "minecraft:air"),
        fill_p(5, -6, 18, 51, -6, 47, "minecraft:gray_concrete"),
        *[fill_p(10, -6, z, 20, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        *[fill_p(30, -6, z, 46, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        fill_p(5, -5, 18, 51, -1, 18, "minecraft:stone_bricks"),
        fill_p(5, -5, 47, 51, -1, 47, "minecraft:stone_bricks"),
        fill_p(5, -5, 18, 5, -1, 47, "minecraft:stone_bricks"),
        fill_p(51, -5, 18, 51, -1, 47, "minecraft:stone_bricks"),
    ]
    pxs = [5, 18, 23, 32, 41, 50]
    pzs = [3, 19, 30, 34, 48]
    for px in pxs:
        for pz in pzs:
            if px >= 32 and pz == 3:
                top_y = 26
            elif px <= 18 and pz <= 18:
                top_y = 41
            else:
                top_y = 58
            cmds.append(fill_p(px, -5, pz, px, top_y, pz, "minecraft:white_concrete"))
    return cmds


def gen_slabs_and_core(spec: dict) -> list[str]:
    cmds = ["# 03 - 11 Floor Slabs (exact footprints 1F-11F), Main/Fire Stairs & Glass Elevator Lobbies"]
    floors = spec["floors"]

    for fl in floors:
        fid = fl["id"]
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        if fid in ("B1", "RF"):
            continue

        mat = "minecraft:smooth_sandstone" if fid in ("1F", "2F", "11F") else "minecraft:smooth_quartz"

        if fid in ("1F", "2F"):
            cmds.append(fill_p(0, yf, 34, 53, yf, 48, mat))
            cmds.append(fill_p(2, yf, 3, 52, yf, 33, mat))
            if fid == "1F":
                cmds.append(fill_p(22, yf, 0, 52, yf, 3, mat))
        elif fid in ("3F", "4F", "5F"):
            cmds.append(fill_p(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_p(5, yf, 6, 51, yf, 18, mat))
            cmds.append(fill_p(11, yf, 0, 51, yf, 5, mat))
        elif fid == "6F":
            # Skip 6F slab inside 2-storey void above IF-5M210 (px=24..50, pz=4..17)
            cmds.append(fill_p(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_p(5, yf, 6, 22, yf, 18, mat))
            cmds.append(fill_p(11, yf, 0, 22, yf, 5, mat))
        elif fid in ("7F", "8F"):
            # SE Podium wing stepped back
            cmds.append(fill_p(0, yf, 19, 53, yf, 48, mat))
            cmds.append(fill_p(5, yf, 6, 23, yf, 18, mat))
            cmds.append(fill_p(11, yf, 0, 23, yf, 5, mat))
        else:
            # 9F, 10F, 11F: Upper rectangular tower crown (matches floor_10, floor_11 & satellite!)
            cmds.append(fill_p(5, yf, 19, 50, yf, 48, mat))
            cmds.append(fill_p(0, yf, 30, 5, yf, 48, mat))

        # Signature checkerboard accent floor tiles
        if fid in ("1F", "2F", "7F", "11F"):
            for px in range(19, 50, 4):
                cmds.append(set_p(px, yf, 32, "minecraft:gray_concrete" if px % 8 == 0 else "minecraft:light_gray_concrete"))
            for pz in range(20, 36, 4):
                cmds.append(set_p(20, yf, pz, "minecraft:gray_concrete" if pz % 8 == 0 else "minecraft:light_gray_concrete"))

        # Corridor ceiling downlights
        z_top = 20 if fid in ("9F", "10F", "11F") else 6
        for pz in range(z_top, 36, 5):
            cmds.append(set_p(20, yc - 1, pz, "minecraft:sea_lantern"))
        for px in range(14, 50, 5):
            cmds.append(set_p(px, yc - 1, 32, "minecraft:sea_lantern"))

    # --- 3 Passenger Elevators (px=15..18, pz=36..48) + Fireman's Elevator (px=22..26, pz=39..48) ---
    cmds.append(fill_p(15, -5, 36, 18, 58, 48, "minecraft:light_gray_concrete", "hollow"))
    cmds.append(fill_p(22, -5, 39, 26, 58, 48, "minecraft:light_gray_concrete", "hollow"))

    for idx, fl in enumerate(floors):
        if fl["id"] == "RF":
            continue
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        fid = fl["id"]

        for ez in (38, 42, 46):
            cmds.append(fill_p(18, yf + 1, ez, 18, yf + 3, ez, "minecraft:air"))
            cmds.append(fill_p(17, yf + 1, ez, 17, yf + 3, ez, "minecraft:iron_block"))
        cmds.append(fill_p(24, yf + 1, 39, 24, yf + 3, 39, "minecraft:air"))
        cmds.append(fill_p(24, yf + 1, 40, 24, yf + 3, 40, "minecraft:iron_block"))

        if fid != "B1":
            # Glass-Walled Elevator Lobby (Lift.jpg & 7thFloor.jpg)
            cmds.append(fill_p(19, yc - 1, 35, 21, yc - 1, 46, "minecraft:blue_terracotta"))
            cmds.append(fill_p(19, yc - 1, 35, 21, yc - 1, 36, "minecraft:stripped_oak_wood"))
            cmds.append(fill_p(19, yf + 1, 35, 21, yc - 1, 35, "minecraft:white_stained_glass"))
            cmds.append(fill_p(20, yf + 1, 35, 21, yf + 3, 35, "minecraft:air"))
            cmds.append(set_p(20, yc - 1, 40, "minecraft:sea_lantern"))
            cmds.append(set_p(22, yf + 1, 36, "minecraft:yellow_concrete"))
            cmds.append(set_p(22, yf + 1, 37, "minecraft:blue_concrete"))
            cmds.append(set_p(23, yf + 1, 36, "minecraft:green_concrete"))
            cmds.append(set_p(23, yf + 1, 37, "minecraft:red_concrete"))

        cmds.append(sign_p(19, yf + 2, 37, "east", f"[ {fid} ]", fl["name"][:15], "/trigger", "if_floor set 1..11"))

        # Walkable Main Staircase (px=9..14, pz=35..48)
        if idx < len(floors) - 2:
            next_yf = floors[idx + 1]["y_floor"]
            height = next_yf - yf
            cmds.append(fill_p(9, next_yf, 36, 13, next_yf, 44, "minecraft:air"))
            cmds.append(fill_p(9, yf + 1, 35, 14, next_yf, 35, "minecraft:white_concrete"))
            cmds.append(fill_p(9, yf + 1, 35, 11, yf + 3, 35, "minecraft:air"))
            for s in range(height):
                sz = 37 + min(s, 6)
                cmds.append(fill_p(9, yf + 1 + s, sz, 13, yf + 1 + s, sz, "minecraft:smooth_quartz_stairs[facing=south]"))

            # NNW Fire Exit Staircase (px=12..18, pz=0..4) up to 8F (roof level 42)
            if idx <= 7:
                cmds.append(fill_p(12, next_yf, 1, 17, next_yf, 3, "minecraft:air"))
                for s in range(height):
                    sx = 17 - min(s, 5)
                    cmds.append(fill_p(sx, yf + 1 + s, 1, sx, yf + 1 + s, 3, "minecraft:stone_brick_stairs[facing=west]"))

            # SE/East Fire Exit Staircase (px=50..53, pz=35..45)
            cmds.append(fill_p(51, next_yf, 36, 52, next_yf, 43, "minecraft:air"))
            for s in range(height):
                sz = 37 + min(s, 6)
                cmds.append(fill_p(51, yf + 1 + s, sz, 52, yf + 1 + s, sz, "minecraft:stone_brick_stairs[facing=south]"))

    cmds.append(fill_p(11, -5, 0, 18, 41, 4, "minecraft:light_gray_concrete", "hollow"))
    for idx, fl in enumerate(floors):
        if fl["id"] == "RF":
            continue
        yf = fl["y_floor"]
        if idx <= 7:
            cmds.append(fill_p(18, yf + 1, 2, 18, yf + 2, 3, "minecraft:air"))
        cmds.append(fill_p(50, yf + 1, 32, 50, yf + 2, 33, "minecraft:air"))
    return cmds


def gen_podium_and_arch() -> list[str]:
    cmds = [
        "# 04 - v3.1 Refined East-Facing Podium, 6-Ribbed C-Arch (c_arch_closeup.jpg) & Flagpoles",
        fill_p(22, 0, -4, 52, 0, 4, "minecraft:smooth_sandstone"),
        # Cobalt Blue Entrance Core Wall on South-East side (c_arch_closeup.jpg!)
        fill_p(47, 0, 1, 52, 11, 4, "minecraft:blue_concrete"),
        # Basement ventilation louvers under SE gray shear wall (c_arch_closeup.jpg)
        fill_p(52, 0, 5, 52, 1, 18, "minecraft:blackstone_wall"),
        # 3 Flagpoles on SE front planter (seen in 3rd street-view photo!)
        *[fill(30, 0, z, 30, 8, z, "minecraft:iron_bars") for z in (16, 18, 20)],

        # 6 Slender White Columns under Oculus Skylight (Front.jpg & c_arch_closeup.jpg)
        fill_p(46, 0, -4, 46, 21, -4, "minecraft:quartz_pillar"),
        fill_p(48, 0, -5, 48, 21, -5, "minecraft:quartz_pillar"),
        fill_p(50, 0, -4, 50, 21, -4, "minecraft:quartz_pillar"),
        fill_p(47, 0, -2, 47, 21, -2, "minecraft:quartz_pillar"),
        fill_p(49, 0, -2, 49, 21, -2, "minecraft:quartz_pillar"),
        fill_p(23, 0, -3, 23, 21, -3, "minecraft:quartz_pillar"),

        # Podium Upper Facade Box facing East (+X) toward Fueang Fa Rd (px=24..50, pz=1, Y=12..21)
        fill_p(24, 12, 1, 50, 21, 1, "minecraft:light_gray_concrete"),
        fill_p(24, 15, 1, 50, 15, 1, "minecraft:polished_andesite"),
        fill_p(24, 18, 1, 50, 18, 1, "minecraft:polished_andesite"),
        fill_p(24, 12, 1, 31, 13, 1, "minecraft:air"),
        fill_p(27, 16, 1, 32, 16, 1, "minecraft:blue_concrete"),
        fill_p(40, 17, 1, 46, 17, 1, "minecraft:blue_concrete"),
        fill_p(34, 15, 1, 39, 15, 1, "minecraft:light_blue_stained_glass"),
        fill_p(28, 19, 1, 33, 19, 1, "minecraft:light_blue_stained_glass"),
        # Recessed 2F glass curtain wall under Podium Box
        fill_p(24, 7, 3, 46, 11, 3, "minecraft:cyan_stained_glass"),
        fill_p(24, 9, 3, 46, 9, 3, "minecraft:gray_concrete"),
    ]

    # Sweeping Curved East Canopy Roof (Y=22..23, facing Fueang Fa Road +X up to mc_x=29)
    for px in range(21, 53):
        pz_min = -5 if px <= 40 else round(-5 + (px - 40) * 0.45)
        cmds.append(fill_p(px, 22, pz_min, px, 22, 5, "minecraft:smooth_quartz"))
        cmds.append(fill_p(px, 23, pz_min, px, 23, 5, "minecraft:smooth_quartz_slab"))
        # Crisp bright white fascia edge on the East overhang
        cmds.append(set_p(px, 23, pz_min, "minecraft:white_concrete"))

    # Oculus Skylight Cutout
    cmds.append(fill_p(47, 22, -4, 49, 23, -2, "minecraft:air"))

    # 6 Parallel Ribbed Silver C-Arch Fins curving smoothly on South-East side (c_arch_closeup.jpg!)
    # Ribs sit at distinct East-West positions (pz = -4, -2, 0, 2, 4, 6 -> mc_x = 28, 26, 24, 22, 20, 18)
    # and curve outward to the South (+Z, px=55) and back under Y=6!
    fin_pzs = [-4, -2, 0, 2, 4, 6]
    seen_pts = set()
    for deg in range(-15, 195, 2):
        rad = math.radians(deg)
        cpx = round(47 + 8.5 * math.sin(rad))
        cy = round(14.5 + 8.0 * math.cos(rad))
        for cpz in fin_pzs:
            pt = (cpx, cy, cpz)
            if pt not in seen_pts:
                seen_pts.add(pt)
                cmds.append(set_p(cpx, cy, cpz, "minecraft:white_concrete"))
                cmds.append(set_p(cpx, cy, cpz + 1, "minecraft:smooth_quartz"))

    # Outer curved white ribbon connecting the outer edge (pz=-5 -> mc_x=+29)
    for deg in range(-15, 195, 2):
        rad = math.radians(deg)
        cpx = round(47 + 8.5 * math.sin(rad))
        cy = round(14.5 + 8.0 * math.cos(rad))
        cmds.append(set_p(cpx, cy, -5, "minecraft:light_gray_concrete"))

    # Podium Front Sign facing East (+X -> mc_yaw = -90)
    cmds.append(text_p(38.0, 18.5, 0.2, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", 180.0, 1.35))
    return cmds


def gen_facade_shell() -> list[str]:
    cmds = [
        "# 05 - v3.0 Exterior Tower Shell (True Satellite Orientation: 9F-11F Rectangular Crown)",
        # West Facade (pz=48, mc_x=-24)
        fill_p(5, 1, 48, 50, 58, 48, "minecraft:light_gray_concrete", "keep"),
        *[fill_p(25, y + 1, 48, 48, y + 3, 48, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],

        # North Facade: 1F-8F NW Wing (px=5, pz=6..18) + Restrooms (px=0, pz=19..48) + 9F-11F North Wall (px=5, pz=19..29)
        fill_p(0, 1, 19, 0, 41, 48, "minecraft:light_gray_concrete", "keep"),
        fill_p(0, 42, 30, 0, 58, 48, "minecraft:light_gray_concrete", "keep"),
        fill_p(5, 1, 6, 5, 41, 18, "minecraft:light_gray_concrete", "keep"),
        fill_p(5, 42, 19, 5, 58, 29, "minecraft:light_gray_concrete", "keep"),
        *[fill_p(5, y + 1, 8, 5, y + 3, 17, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(5, y + 1, 20, 5, y + 3, 28, "minecraft:cyan_stained_glass") for y in (42, 47, 52)],

        # South Facade (px=53 for 1F-8F, px=50 for 9F-11F) + SE Shear Wall & Cobalt Blue Corner (c_arch_closeup.jpg)
        fill_p(53, 1, 19, 53, 41, 48, "minecraft:light_gray_concrete", "keep"),
        fill_p(50, 42, 19, 50, 58, 48, "minecraft:light_gray_concrete", "keep"),
        *[fill_p(53, y + 1, 21, 53, y + 3, 46, "minecraft:light_blue_stained_glass") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(50, y + 1, 21, 50, y + 3, 46, "minecraft:light_blue_stained_glass") for y in (42, 47, 52)],
        # Dark louver screen along South-East shear wall
        *[fill_p(54, y, 22, 54, y, 36, "minecraft:deepslate_brick_wall") for y in range(13, 41, 2)],
        # Cobalt Blue vertical stripes on South-West & South-East corners
        fill_p(53, 0, 47, 54, 41, 48, "minecraft:blue_concrete"),
        fill_p(50, 42, 47, 51, 58, 48, "minecraft:blue_concrete"),
        fill_p(51, 0, 3, 52, 26, 4, "minecraft:blue_concrete"),

        # East Facade facing Fueang Fa Road (1F-8F NW pz=6, 6F-11F main East wall pz=19)
        fill_p(5, 1, 6, 23, 41, 6, "minecraft:light_gray_concrete", "keep"),
        *[fill_p(7, y + 1, 6, 17, y + 3, 6, "minecraft:light_blue_stained_glass") for y in (12, 17, 22, 27, 32, 37)],
        fill_p(24, 32, 19, 53, 41, 19, "minecraft:light_blue_stained_glass", "keep"),
        fill_p(5, 42, 19, 50, 58, 19, "minecraft:light_blue_stained_glass", "keep"),
        *[fill_p(px, 32, 19, px, 58, 19, "minecraft:gray_concrete") for px in range(24, 51, 5)],
        fill_p(4, 0, 6, 5, 41, 7, "minecraft:blue_concrete"),
        fill_p(4, 42, 18, 5, 58, 19, "minecraft:blue_concrete"),

        # Protruding 3-storey glass box at 6F-8F (px=21..27, pz=14..20)
        fill_p(21, 27, 14, 27, 41, 20, "minecraft:light_blue_stained_glass", "hollow"),
        fill_p(21, 32, 14, 27, 32, 20, "minecraft:white_concrete"),
        fill_p(21, 37, 14, 27, 37, 20, "minecraft:white_concrete"),

        # White Projecting Floor Ledges
        *[fill_p(5, y, 5, 24, y, 5, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(24, y, 18, 54, y, 18, "minecraft:smooth_quartz") for y in (32, 37)],
        *[fill_p(5, y, 18, 51, y, 18, "minecraft:smooth_quartz") for y in (42, 47, 52)],
        *[fill_p(54, y, 18, 54, y, 49, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(51, y, 18, 51, y, 49, "minecraft:smooth_quartz") for y in (42, 47, 52)],

        # Green Rooftop Terrace Gardens on 7F & 9F step-backs (matching Scale Model!)
        fill_p(26, 33, 6, 48, 33, 15, "minecraft:grass_block"),
        *[fill_p(px, 34, 9, px + 2, 35, 11, "minecraft:oak_leaves[persistent=true]") for px in (30, 38, 44)],
        fill_p(7, 42, 7, 21, 42, 16, "minecraft:grass_block"),
        *[fill_p(px, 43, 10, px + 2, 44, 12, "minecraft:oak_leaves[persistent=true]") for px in (9, 16)],
    ]
    return cmds


def gen_roof_and_solar() -> list[str]:
    cmds = [
        "# 06 - v3.0 11F Roof Crown, Attic Band, 3D Signs & True Satellite Solar Panel Layout",
        fill_p(5, 59, 19, 50, 59, 48, "minecraft:gray_concrete"),
        fill_p(0, 59, 30, 5, 59, 48, "minecraft:gray_concrete"),
        # Light-gray attic facade band facing East (+X, pz=18) & South (+Z, px=51)
        fill_p(5, 59, 18, 50, 61, 18, "minecraft:light_gray_concrete"),
        fill_p(51, 59, 18, 51, 61, 48, "minecraft:light_gray_concrete"),
        # Overhanging flat roof canopy (Y=63..64)
        fill_p(-1, 63, 17, 52, 63, 49, "minecraft:light_gray_concrete"),
        fill_p(-1, 64, 17, 52, 64, 49, "minecraft:polished_deepslate"),
        # Gold BUU seal & crisp 3D text_display Faculty Sign facing East (Fueang Fa Rd) & South
        fill_p(18, 60, 17, 19, 61, 17, "minecraft:gold_block"),
        text_p(30.0, 60.6, 16.5, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", 180.0, 2.1),
        text_p(52.2, 60.6, 33.0, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", -90.0, 2.0),
        # 3 Rows of Solar Panels on North half of 11F Roof (px=8..25) running East-West (matches ESRI z19!)
        fill_p(8, 65, 22, 11, 65, 44, "minecraft:daylight_detector"),
        fill_p(14, 65, 22, 17, 65, 44, "minecraft:daylight_detector"),
        fill_p(20, 65, 22, 23, 65, 44, "minecraft:daylight_detector"),
        # Ribbed metal roof strips on South half of 11F roof (matches ESRI z19!)
        *[fill_p(px, 65, 21, px, 65, 45, "minecraft:smooth_quartz_slab") for px in range(28, 49, 2)],
    ]
    return cmds


def gen_interiors() -> list[str]:
    return [
        "# 07 - v3.0 Exact Floor-Plan Interiors (1F-11F)",
        *build_all_floors(),
    ]


def gen_campus_context() -> list[str]:
    cmds = [
        "# 09 - v3.1 True Campus Surroundings (Science CL + Circular Pond East across Fueang Fa Rd, Yellow Bldg NE, 6F Bldg South)",
        # 1) East Across Fueang Fa Rd (X = +44..+80): Science CL Gray Skylight Building + Circular Pond!
        fill(44, -1, -36, 80, -1, 36, "minecraft:grass_block"),
        fill(44, -1, -28, 48, -1, 28, "minecraft:light_gray_concrete"),
        # Circular Pond in front of Science CL (X=+52, Z=+14, matches tile_19_409126_242626.jpg & 5426_View-2-1.jpg!)
    ]
    for dx in range(-9, 10):
        for dz in range(-9, 10):
            r = math.hypot(dx, dz)
            px, pz = 52 + dx, 14 + dz
            if r <= 6.0:
                cmds.append(setblock(px, -1, pz, "minecraft:water"))
            elif r <= 8.0:
                cmds.append(setblock(px, 0, pz, "minecraft:smooth_quartz_slab"))
                cmds.append(setblock(px, -1, pz, "minecraft:smooth_quartz"))

    # Science CL Gray Building with 5 skylight bays (East across road, X=+58..+78, Z=-6..+26)
    cmds.extend([
        fill(58, 0, -6, 78, 16, 26, "minecraft:light_gray_concrete", "hollow"),
        *[fill(59, 17, z, 77, 17, z + 2, "minecraft:light_blue_stained_glass") for z in (-3, 3, 9, 15, 21)],
        fill(58, 17, -6, 78, 17, 26, "minecraft:gray_concrete", "keep"),
        # Yellow Science / Computer Center Building across Fueang Fa Rd to North-East (X=+49..+70, Z=-34..-10)
        fill(49, 0, -34, 70, 16, -10, "minecraft:smooth_sandstone", "hollow"),
        *[fill(49, y, -31, 49, y + 1, -13, "minecraft:black_stained_glass") for y in (3, 8, 12)],
        fill(48, 17, -35, 71, 17, -9, "minecraft:gray_concrete"),
        # White & Teal Curved Building front facing road at X=+48..+56, Z=-8..+4 (seen in Front.jpg!)
        fill(48, 0, -8, 57, 14, 4, "minecraft:white_concrete", "hollow"),
        fill(47, 15, -9, 58, 15, 5, "minecraft:cyan_concrete"),
    ])

    # 2) South Adjacent 6-Storey Gray/Blue Building (Z = +34..+54, X = -22..+24)
    cmds.extend([
        fill(-22, -1, 34, 24, -1, 54, "minecraft:light_gray_concrete"),
        fill(-22, 0, 34, 24, 24, 54, "minecraft:light_gray_concrete", "hollow"),
        fill(-4, 1, 34, 6, 23, 34, "minecraft:light_blue_concrete"),
        *[fill(x, y, 34, x + 2, y + 1, 34, "minecraft:black_stained_glass") for y in (4, 9, 14, 19) for x in range(-18, 20, 8)],
        fill(-23, 25, 33, 25, 25, 55, "minecraft:gray_concrete"),
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
        'tellraw @s [{"text":"พิมพ์ /trigger if_floor set <เลขชั้น> หรือคลิกชั้นที่ต้องการ (แปลนจริงครบ 1F-11F!):","color":"gray"}]',
    ]

    tick_cmds = [
        "scoreboard players enable @a if_floor",
    ]

    floor_num_map = [
        (0, "B1", -5, "ลานจอดรถใต้ดิน (Basement Car Park)"),
        (1, "1F", 0, "โถงกิจกรรม / สโมสร IF-109 / ประตูม้วน IF-104 / IF-111..115"),
        (2, "2F", 6, "ห้องสมุด IF-208 / สำนักงาน IF-210..211 / ผู้บริหาร IF-215..223"),
        (3, "3F", 12, "ห้องคอมฯ IF-3C01..04 / ห้องบรรยาย IF-3M210"),
        (4, "4F", 17, "ห้องคอมฯ IF-4C01..04 / ห้องบรรยาย IF-4M210"),
        (5, "5F", 22, "ห้องบรรยาย IF-5T01..05 / ห้องบรรยาย 2 ชั้น IF-5M210"),
        (6, "6F", 27, "ห้องบรรยาย IF-6T01..05"),
        (7, "7F", 32, "★ Open House Innovation Hub (IF-7T01..05: Vision/DMI/FabLab)"),
        (8, "8F", 37, "ห้องปฏิบัติการ & Working Space IF-8R01..08"),
        (9, "9F", 42, "ห้องพักอาจารย์ IF-908A..D"),
        (10, "10F", 47, "ห้องประชุม IF-10M32 / IF-10M60 / IF-1008..1011"),
        (11, "11F", 52, "ห้องนิทรรศการ Exhibition Hall IF-11M280 & IF-1109"),
    ]

    # Elevator Lobby Star at (px=20, pz=36) -> (mc_x=-12, mc_z=-7), facing East (+X, yaw=-90) down N-S corridor!
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
            f"run tp @s ~{el_x} ~{tp_y} ~{el_z} -90 0"
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
            "description": "IF-BUU 1:1 Craft v3.0 — Complete 1F-11F Floor Plans + True Satellite Orientation",
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
        for x_start, x_end in [(-60, -30), (-29, 0), (1, 35), (36, 70)]:
            for z_start, z_end in [(-54, -20), (-19, 18), (19, 58)]:
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
            'tellraw @a {"text":"[IF-BUU 1:1 v3.0] Built complete 1F-11F Faculty of Informatics 1:1!","color":"aqua"}',
        ],
    )

    print(f"Generated v3.0 Complete Datapack -> {DP_ROOT}")
    for f in sorted(FUNC_DIR.glob("*.mcfunction")):
        line_count = len(f.read_text(encoding="utf-8").splitlines())
        print(f"  - if_buu:{f.stem} ({line_count} lines)")


if __name__ == "__main__":
    main()
