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


def car(x0: int, z0: int, color: str, along_x: bool = True, y0: int = 0) -> list[str]:
    """Simple 4x2 block car prop (body + tinted cabin)."""
    if along_x:
        return [fill(x0, y0, z0, x0 + 3, y0, z0 + 1, f"minecraft:{color}_concrete"),
                fill(x0 + 1, y0 + 1, z0, x0 + 2, y0 + 1, z0 + 1, "minecraft:black_stained_glass")]
    return [fill(x0, y0, z0, x0 + 1, y0, z0 + 3, f"minecraft:{color}_concrete"),
            fill(x0, y0 + 1, z0 + 1, x0 + 1, y0 + 1, z0 + 2, "minecraft:black_stained_glass")]


def moto(x: int, z: int, y0: int = 0, seat: str = "blue") -> list[str]:
    """Motorcycle prop: dark frame + coloured seat."""
    return [setblock(x, y0, z, "minecraft:polished_blackstone_wall"),
            setblock(x, y0 + 1, z, f"minecraft:{seat}_carpet")]


def arrow_x(x: int, y: int, z: int, direction: int, block: str = "minecraft:white_concrete") -> list[str]:
    """Painted road arrow along X. direction=-1 points West, +1 points East."""
    tip = x if direction < 0 else x + 3
    return [fill(x, y, z, x + 3, y, z, block),
            setblock(tip - direction, y, z - 1, block),
            setblock(tip - direction, y, z + 1, block)]


def gen_site_and_road() -> list[str]:
    cmds = [
        "# 01 - v3.2 Site Plan: Fueang Fa Rd (East), official North drop-off loop & barrier gate,",
        "#      West motorcycle parking, B1 car ramp, SE front motorcycle bay under the C-Arch",
        fill(-50, -1, -50, 46, -1, 34, "minecraft:grass_block"),
        # --- Fueang Fa Road (main road, North-South, East of building) ---
        fill(33, -1, -50, 43, -1, 34, "minecraft:gray_concrete"),
        fill(38, -1, -50, 38, -1, 34, "minecraft:yellow_concrete"),
        fill(33, -1, -50, 33, -1, 34, "minecraft:white_concrete"),
        fill(43, -1, -50, 43, -1, 34, "minecraft:white_concrete"),
        # Pedestrian crosswalk just south of the drive-in
        *[fill(34, -1, z, 42, -1, z + 1, "minecraft:white_concrete") for z in range(-24, -17, 3)],
        # Brick sidewalk along East + front plaza + wide entrance steps
        fill(30, -1, -50, 32, -1, 34, "minecraft:bricks"),
        fill(24, -1, -26, 29, -1, 26, "minecraft:light_gray_concrete"),
        fill(24, -1, -12, 29, -1, -11, "minecraft:smooth_quartz"),
        fill(24, -1, 14, 29, -1, 15, "minecraft:smooth_quartz"),
        fill(25, 0, -2, 26, 0, 15, "minecraft:smooth_quartz_slab"),
        fill(24, 0, -2, 24, 0, 15, "minecraft:smooth_quartz"),
        # Trees + street lamps along East sidewalk
        *[fill(31, 0, z, 31, 2, z, "minecraft:oak_log") for z in (-46, -18, -10, 6, 22)],
        *[fill(30, 3, z - 1, 32, 4, z + 1, "minecraft:oak_leaves[persistent=true]") for z in (-46, -18, -10, 6, 22)],
        *[fill(30, 0, z, 30, 5, z, "minecraft:iron_bars") for z in (-42, -2, 30)],
        *[setblock(30, 6, z, "minecraft:sea_lantern") for z in (-42, -2, 30)],

        # --- North drop-off loop (official IF traffic plan) ---
        fill(-24, -1, -27, 29, -1, -26, "minecraft:light_gray_concrete"),
        fill(-43, -1, -39, 32, -1, -28, "minecraft:gray_concrete"),
        # Solid white line separating the motorcycle lane (north) from the car lane
        fill(-30, -1, -37, 32, -1, -37, "minecraft:white_concrete"),
        # Raised drop-off lane next to the building (cars drive UP to 1F level) + slab ramp
        fill(-16, 0, -30, 26, 0, -28, "minecraft:smooth_stone"),
        fill(27, 0, -30, 30, 0, -28, "minecraft:smooth_stone_slab"),
        fill(-16, 0, -30, -16, 0, -28, "minecraft:red_concrete"),
        # Central island with planting + quartz noses
        fill(-12, 0, -32, 22, 0, -31, "minecraft:grass_block"),
        fill(-13, 0, -32, -13, 0, -31, "minecraft:smooth_quartz"),
        fill(23, 0, -32, 23, 0, -31, "minecraft:smooth_quartz"),
        *[fill(x, 1, -32, x, 2, -32, "minecraft:oak_log") for x in (-6, 4, 14)],
        *[fill(x - 1, 3, -33, x + 1, 3, -31, "minecraft:oak_leaves[persistent=true]") for x in (-6, 4, 14)],
        *[setblock(x, 1, -31, "minecraft:flowering_azalea") for x in (-10, -1, 9, 19)],
        # Contraflow warning zone (cars exiting East toward Fueang Fa Rd)
        fill(-10, -1, -34, 29, -1, -34, "minecraft:orange_concrete"),
        # Painted arrows
        *arrow_x(-2, -1, -35, -1), *arrow_x(16, -1, -35, -1),
        *arrow_x(-36, -1, -38, -1), *arrow_x(8, -1, -38, -1),
        *arrow_x(2, 1, -29, -1),
        # Barrier gate (yellow/black boom) across the west end of the car lanes
        fill(-20, 0, -28, -20, 1, -28, "minecraft:iron_block"),
        *[setblock(-20, 1, z, "minecraft:cut_sandstone_slab" if z % 2 == 0 else "minecraft:blackstone_slab") for z in range(-36, -28)],
        # Cars: pickup waiting at drop-off + car on the loop
        *car(6, -30, "white", y0=1),
        *car(-4, -36, "light_gray"),

        # --- West service lane -> West motorcycle parking -> B1 car ramp ---
        fill(-43, -1, -39, -39, -1, 20, "minecraft:gray_concrete"),
        *[fill(-41, -1, z, -41, -1, z + 1, "minecraft:white_concrete") for z in range(-30, 20, 4)],
        fill(-38, -1, -24, -25, -1, 12, "minecraft:gray_concrete"),
        *[fill(-38, -1, z, -34, -1, z, "minecraft:white_concrete") for z in range(-23, 12, 2)],
        *[fill(-29, -1, z, -25, -1, z, "minecraft:white_concrete") for z in range(-23, 12, 2)],
        *[c for z in range(-22, 12, 2) for c in moto(-36, z)],
        *[c for z in range(-22, 12, 4) for c in moto(-27, z, seat="red")],

        # --- South lane + SE front motorcycle bay under the C-Arch (c_arch_closeup.jpg) ---
        fill(-24, -1, 27, 32, -1, 33, "minecraft:gray_concrete"),
        *[fill(x, -1, 27, x, -1, 30, "minecraft:white_concrete") for x in range(6, 30, 2)],
        *arrow_x(-12, -1, 32, 1, "minecraft:yellow_concrete"), *arrow_x(12, -1, 32, 1, "minecraft:yellow_concrete"),
        *[c for x in range(7, 29, 2) for c in moto(x, 28)],

        # Guest spawn pad on the East plaza
        setblock(30, -1, 5, "minecraft:sea_lantern"),
        setblock(30, 0, 5, "minecraft:light_gray_carpet"),
    ]
    return cmds

def gen_basement_and_grid() -> list[str]:
    cmds = [
        "# 02 - v3.2 Basement Car Park (B1), West B1 car ramp & structural column grid",
        fill_p(5, -5, 18, 51, -1, 47, "minecraft:air"),
        fill_p(5, -6, 18, 51, -6, 47, "minecraft:gray_concrete"),
        *[fill_p(10, -6, z, 20, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        *[fill_p(30, -6, z, 46, -6, z, "minecraft:yellow_concrete") for z in range(22, 44, 6)],
        fill_p(5, -5, 18, 51, -1, 18, "minecraft:stone_bricks"),
        fill_p(5, -5, 47, 51, -1, 47, "minecraft:stone_bricks"),
        fill_p(5, -5, 18, 5, -1, 47, "minecraft:stone_bricks"),
        fill_p(51, -5, 18, 51, -1, 47, "minecraft:stone_bricks"),
        *[setblock(x, -1, z, "minecraft:sea_lantern") for x in range(-20, 6, 6) for z in range(-19, 23, 6)],
        *car(-20, -18, "white", y0=-5), *car(-20, -12, "black", y0=-5), *car(-8, 6, "red", y0=-5),
        *car(-2, 6, "blue", y0=-5), *car(-14, 18, "light_gray", y0=-5),
    ]
    # West B1 ramp (X -38 -> -24, Z 16..20) from ground (Y=-1) down to the B1 floor (Y=-6)
    for i, x in enumerate(range(-38, -23)):
        y = -1 - round(i * 5 / 14)
        cmds.append(fill(x, y, 16, x, y, 20, "minecraft:gray_concrete"))
        if y < -1:
            cmds.append(fill(x, y + 1, 16, x, -1, 20, "minecraft:air"))
        cmds.append(fill(x, y, 15, x, 0, 15, "minecraft:stone_bricks"))
        cmds.append(fill(x, y, 21, x, 0, 21, "minecraft:stone_bricks"))
    cmds.append(fill(-24, -5, 16, -23, -1, 20, "minecraft:air"))
    cmds.append(fill(-34, -1, 18, -31, -1, 18, "minecraft:yellow_concrete"))

    pxs = [5, 18, 23, 32, 41, 50]
    pzs = [3, 19, 30, 34, 48]
    for px in pxs:
        for pz in pzs:
            if pz < 19:
                top_y = 41 if px <= 23 else 31
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

    cmds.append(fill_p(11, -5, 0, 18, 41, 4, "minecraft:white_concrete", "outline"))
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
        "# 04 - v3.2 Podium (photo-matched): undercroft + 2F glass band + gray panel box (3F-6F)",
        "#      + floating cap roof + 6-rib C-Arch on the South end facing Fueang Fa Rd",
        fill_p(22, 0, -4, 52, 0, 4, "minecraft:smooth_sandstone"),
        fill_p(47, 0, 1, 52, 11, 4, "minecraft:blue_concrete"),
        fill_p(52, 0, 17, 54, 31, 18, "minecraft:blue_concrete"),
        fill_p(53, 0, 3, 53, 0, 16, "minecraft:blackstone_wall"),
        *[fill(28, 0, z, 28, 9, z, "minecraft:iron_bars") for z in (-8, -6, -4)],
        setblock(28, 9, -8, "minecraft:red_wool"),
        setblock(28, 9, -6, "minecraft:white_wool"),
        setblock(28, 9, -4, "minecraft:blue_wool"),
        *[fill_p(px, 0, pz, px, 31, pz, "minecraft:quartz_pillar") for px, pz in ((46, -4), (48, -5), (50, -4), (47, -2), (49, -2), (51, -2))],
        fill_p(23, 0, -3, 23, 31, -3, "minecraft:quartz_pillar"),
        fill_p(26, 6, -3, 53, 6, 2, "minecraft:smooth_quartz"),
        fill_p(26, 6, -4, 53, 6, -4, "minecraft:white_concrete"),
        fill_p(21, 7, 2, 53, 11, 2, "minecraft:gray_stained_glass"),
        *[fill_p(px, 7, 2, px, 11, 2, "minecraft:gray_concrete") for px in range(21, 54, 4)],
        fill_p(21, 12, 1, 53, 31, 1, "minecraft:light_gray_concrete"),
        *[fill_p(21, y, 1, 53, y, 1, "minecraft:polished_andesite") for y in (16, 21, 26)],
        fill_p(21, 13, 1, 27, 30, 1, "minecraft:light_blue_stained_glass"),
        *[fill_p(px, 12, 1, px, 31, 1, "minecraft:gray_concrete") for px in (21, 24, 27)],
        *[fill_p(21, y, 1, 27, y, 1, "minecraft:gray_concrete") for y in (16, 21, 26)],
        fill_p(49, 13, 1, 52, 30, 1, "minecraft:light_blue_stained_glass"),
        fill_p(49, 21, 1, 52, 21, 1, "minecraft:gray_concrete"),
        *[fill_p(a, y, 1, b, y, 1, "minecraft:light_blue_stained_glass") for a, b, y in
          ((30, 33, 28), (37, 40, 24), (31, 34, 19), (40, 44, 17), (33, 37, 14), (43, 46, 29), (44, 46, 22))],
        *[fill_p(a, y, 1, b, y, 1, "minecraft:blue_concrete") for a, b, y in
          ((29, 34, 27), (35, 39, 29), (41, 45, 25), (30, 36, 23), (38, 42, 18), (44, 47, 15), (29, 32, 13))],
        fill_p(53, 8, 3, 53, 31, 16, "minecraft:light_gray_concrete"),
        *[fill_p(53, y, 6, 53, y + 1, 12, "minecraft:light_blue_stained_glass") for y in (14, 20, 26)],
    ]

    for px in range(20, 56):
        if px < 24:
            pz_min = -5 + (24 - px)
        elif px <= 44:
            pz_min = -5
        else:
            pz_min = round(-5 + (px - 44) * 0.5)
        cmds.append(fill_p(px, 32, pz_min, px, 32, 5, "minecraft:smooth_quartz"))
        cmds.append(fill_p(px, 33, pz_min + 1, px, 33, 5, "minecraft:smooth_quartz_slab"))
        cmds.append(set_p(px, 33, pz_min, "minecraft:white_concrete"))
    cmds.append(fill_p(47, 32, -4, 49, 33, -2, "minecraft:air"))

    rib_pzs = [-4, -2, 0, 2, 4, 6]
    seen = set()
    for t in range(0, 181, 2):
        r = math.radians(t)
        cpx = round(47 + 8.0 * math.sin(r))
        cy = round(20 + 12.0 * math.cos(r))
        for pz in rib_pzs:
            if (cpx, cy, pz) not in seen:
                seen.add((cpx, cy, pz))
                cmds.append(set_p(cpx, cy, pz, "minecraft:white_concrete"))

    cmds.append(text_p(38.0, 23.5, 0.2, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", 180.0, 1.6))
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
        *[fill_p(53, y + 1, 31, 53, y + 3, 46, "minecraft:light_blue_stained_glass") for y in (12, 17, 22, 27, 32, 37)],
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
        fill_p(19, 33, 1, 25, 41, 7, "minecraft:light_blue_stained_glass", "outline"),
        fill_p(19, 37, 1, 25, 37, 7, "minecraft:white_concrete", "outline"),
        fill_p(19, 41, 1, 25, 41, 7, "minecraft:white_concrete"),
        fill_p(11, 1, 0, 12, 41, 0, "minecraft:blue_concrete"),

        # White Projecting Floor Ledges
        *[fill_p(5, y, 5, 24, y, 5, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(24, y, 18, 54, y, 18, "minecraft:smooth_quartz") for y in (32, 37)],
        *[fill_p(5, y, 18, 51, y, 18, "minecraft:smooth_quartz") for y in (42, 47, 52)],
        *[fill_p(54, y, 18, 54, y, 49, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37)],
        *[fill_p(51, y, 18, 51, y, 49, "minecraft:smooth_quartz") for y in (42, 47, 52)],

        # Green Rooftop Terrace Gardens on 7F & 9F step-backs (matching Scale Model!)
        fill_p(24, 33, 6, 50, 33, 17, "minecraft:grass_block"),
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
