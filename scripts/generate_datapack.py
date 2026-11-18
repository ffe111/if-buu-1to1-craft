"""
Generate a Minecraft Java 1.21+ Datapack (world/datapacks/if_buu_1to1)
that builds the 1:1 Faculty of Informatics building, Burapha University:
  01_site_road            - Fueang Fa Rd, crosswalk, brick sidewalk, front plaza, moto parking, trees
  02_basement_and_grid    - Basement car park (B1) & structural white concrete column grid
  03_slabs_and_core       - 11 floor slabs, signature floor tiles, walkable main/fire stairs,
                            and authentic glass-walled elevator lobbies (matching Lift.jpg & 7thFloor.jpg)
  04_podium_and_arch      - Front podium (1F-4F), C-shaped sweeping canopy arch, wheelchair ramp,
                            6 slender pillars, cobalt blue wall, 2F terrace
  05_facade_shell         - Main 11-storey tower curtain wall, step-back wing (8F-11F),
                            protruding 6F-8F glass corner box, cobalt blue cores, dark louvers
  06_roof_and_solar       - Roof overhang, Faculty sign parapet, 3 solar panel arrays
  07_interiors            - Representative rooms across all floors: 1F SMO/study tables,
                            2F Digital Library/Offices, 3F/5F 210-seat Sloped Lecture Hall & Comp Labs,
                            4F/6F Server Room & Labs, 7F Co-Working/FabLab, 8F Research/Software Park,
                            9F Faculty Offices, 10F Hall of Fame/Conference, 11F Exhibition Hall
  08_interactive_openhouse - /trigger if_floor elevator system (works for non-OP guests!) +
                            clickable tellraw directory menu + lobby floor signs

Origin (~0 ~0 ~0) = Center of front drop-off stairs on the East plaza,
just west of Fueang Fa Road.
  +X = East (Fueang Fa Road)
  -X = West (into the building)
  -Z = North (toward Computer Center)
  +Z = South (toward adjacent building / C-arch base)
"""

import json
import math
from pathlib import Path

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


def wall_sign(x: int, y: int, z: int, facing: str, line1: str, line2: str = "", line3: str = "", line4: str = "") -> str:
    msgs = [json.dumps(line1, ensure_ascii=False), json.dumps(line2, ensure_ascii=False),
            json.dumps(line3, ensure_ascii=False), json.dumps(line4, ensure_ascii=False)]
    nbt = (
        '{front_text:{messages:['
        + ",".join(f'\'{{"text":{m}}}\'' for m in msgs)
        + "]}}"
    )
    return f"setblock ~{x} ~{y} ~{z} minecraft:oak_wall_sign[facing={facing}]{nbt}"


def write_func(name: str, lines: list[str]) -> Path:
    FUNC_DIR.mkdir(parents=True, exist_ok=True)
    path = FUNC_DIR / f"{name}.mcfunction"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def gen_site_and_road() -> list[str]:
    cmds = [
        "# 01 - Site Plaza, Brick Sidewalk, Fueang Fa Road, Crosswalk & West Moto Parking",
        fill(-74, -1, -34, 22, -1, 34, "minecraft:grass_block"),
        # Fueang Fa Road (+X = 6 .. 16)
        fill(6, -1, -34, 16, -1, 34, "minecraft:gray_concrete"),
        fill(11, -1, -34, 11, -1, 34, "minecraft:yellow_concrete"),
        # Pedestrian Crosswalk North of entrance (seen in ESRI z19 tile!)
        *[fill(7, -1, z, 15, -1, z + 1, "minecraft:white_concrete") for z in range(-28, -21, 3)],
        # Brick sidewalk (+X = 3 .. 5)
        fill(3, -1, -34, 5, -1, 34, "minecraft:bricks"),
        # Front Plaza (-16 .. +2)
        fill(-16, -1, -30, 2, -1, 30, "minecraft:light_gray_concrete"),
        # Decorative cream concrete strips on plaza (from Front.jpg)
        fill(-14, -1, -12, 2, -1, -11, "minecraft:smooth_quartz"),
        fill(-14, -1, 10, 2, -1, 11, "minecraft:smooth_quartz"),
        # Front granite entrance steps (-3 .. -1, Z = -8 .. +6)
        fill(-2, 0, -8, -1, 0, 6, "minecraft:smooth_quartz_slab"),
        fill(-3, 0, -8, -3, 0, 6, "minecraft:smooth_quartz"),
        # Wheelchair Ramp along South-East entrance (Z = +7 .. +12)
        fill(0, 0, 8, -2, 0, 10, "minecraft:smooth_quartz_slab"),
        fill(-3, 0, 8, -5, 0, 10, "minecraft:smooth_quartz"),
        # West Motorcycle Parking lot (-73 .. -62) + shade bays
        fill(-73, -1, -26, -61, -1, 26, "minecraft:gray_concrete"),
        *[fill(-72, -1, z, -63, -1, z, "minecraft:white_concrete") for z in range(-22, 24, 6)],
        # Trees along North/South sides & plaza planters
        *[setblock(4, 0, z, "minecraft:oak_leaves[persistent=true]") for z in (-20, -14, 16, 22)],
        *[fill(4, 0, z, 4, 2, z, "minecraft:oak_log") for z in (-22, 18)],
        *[fill(3, 3, z - 1, 5, 4, z + 1, "minecraft:oak_leaves[persistent=true]") for z in (-22, 18)],
        # Spawn marker pad for Open House guests
        setblock(1, -1, -1, "minecraft:sea_lantern"),
        setblock(1, 0, -1, "minecraft:light_gray_carpet"),
    ]
    return cmds


def gen_basement_and_grid() -> list[str]:
    cmds = [
        "# 02 - Basement Car Park (B1) & Structural Column Grid",
        fill(-60, -5, -24, -16, -1, 23, "minecraft:air"),
        fill(-60, -6, -24, -16, -6, 23, "minecraft:gray_concrete"),
        # B1 parking bay stripes
        *[fill(-56, -6, z, -48, -6, z, "minecraft:yellow_concrete") for z in range(-20, 20, 6)],
        *[fill(-34, -6, z, -24, -6, z, "minecraft:yellow_concrete") for z in range(-20, 20, 6)],
        # B1 perimeter retaining walls
        fill(-60, -5, -24, -16, -1, -24, "minecraft:stone_bricks"),
        fill(-60, -5, 23, -16, -1, 23, "minecraft:stone_bricks"),
        fill(-60, -5, -24, -60, -1, 23, "minecraft:stone_bricks"),
        fill(-16, -5, -24, -16, -1, 23, "minecraft:stone_bricks"),
    ]
    # Structural columns (8F-11F step back on North-East corner, so East-North columns stop at 7F/52)
    xs = [-60, -49, -38, -27, -16]
    zs = [-24, -12, 0, 12, 23]
    for x in xs:
        for z in zs:
            top_y = 36 if (x == -16 and z <= -12) else 58
            cmds.append(fill(x, -5, z, x, top_y, z, "minecraft:white_concrete"))
    return cmds


def gen_slabs_and_core(spec: dict) -> list[str]:
    cmds = ["# 03 - 11 Floor Slabs, Signature Tile Pattern, Walkable Stairs & Glass Elevator Lobbies"]
    floors = spec["floors"]

    for fl in floors:
        fid = fl["id"]
        yf = fl["y_floor"]
        if fid in ("B1", "RF"):
            continue

        # Step-back on North-East wing for 8F-11F (seen in 5426_View-3.jpg)
        if fid in ("8F", "9F", "10F", "11F"):
            # Main west block full width (-60..-26, Z=-24..23), east-south wing (-25..-16, Z=-8..23)
            cmds.append(fill(-60, yf, -24, -26, yf, 23, "minecraft:smooth_sandstone" if fid == "11F" else "minecraft:smooth_quartz"))
            cmds.append(fill(-25, yf, -8, -16, yf, 23, "minecraft:smooth_sandstone" if fid == "11F" else "minecraft:smooth_quartz"))
        else:
            base_mat = "minecraft:smooth_sandstone" if fid in ("1F", "2F") else "minecraft:smooth_quartz"
            cmds.append(fill(-60, yf, -24, -16, yf, 23, base_mat))

        # Exterior white horizontal floor ledge around tower
        cmds.append(fill(-61, yf, -25, -15 if fid not in ("8F", "9F", "10F", "11F") else -26, yf, -25, "minecraft:smooth_quartz"))
        cmds.append(fill(-61, yf, 24, -15, yf, 24, "minecraft:smooth_quartz"))
        cmds.append(fill(-61, yf, -25, -61, yf, 24, "minecraft:smooth_quartz"))

        # Random/checker accent tiles on 1F, 2F, 7F, 11F matching VR Tour panoramas
        if fid in ("1F", "2F", "7F", "11F"):
            for x in range(-58, -18, 5):
                for z in range(-22, 22, 5):
                    if fid in ("7F",) and x > -26 and z < -8:
                        continue
                    mat = "minecraft:gray_concrete" if (x + z) % 2 == 0 else "minecraft:light_gray_concrete"
                    cmds.append(setblock(x, yf, z, mat))

    # Central Elevator Core (-48..-42, Z=-6..5) & Glass-Walled Elevator Lobby (-41..-35, Z=-7..6)
    cmds.append(fill(-48, -5, -6, -42, 58, 5, "minecraft:light_gray_concrete", "hollow"))

    for idx, fl in enumerate(floors):
        if fl["id"] == "RF":
            continue
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        fid = fl["id"]

        # Elevator doors & iron frames
        cmds.append(fill(-42, yf + 1, -4, -42, yf + 3, -3, "minecraft:air"))
        cmds.append(fill(-42, yf + 1, 1, -42, yf + 3, 2, "minecraft:air"))
        cmds.append(fill(-43, yf + 1, -4, -43, yf + 3, -3, "minecraft:iron_block"))
        cmds.append(fill(-43, yf + 1, 1, -43, yf + 3, 2, "minecraft:iron_block"))

        # Elevator Lobby enclosure (matching Lift.jpg & 7thFloor.jpg!)
        if fid != "B1":
            # Light-blue side accent walls (Z=-7 and Z=+6)
            cmds.append(fill(-41, yf + 1, -7, -36, yc - 1, -7, "minecraft:light_blue_terracotta"))
            cmds.append(fill(-41, yf + 1, 6, -36, yc - 1, 6, "minecraft:light_blue_terracotta"))
            # Dark blue-gray ceiling & warm oak trim inside elevator lobby
            cmds.append(fill(-41, yc - 1, -6, -36, yc - 1, 5, "minecraft:blue_terracotta"))
            cmds.append(fill(-37, yc - 1, -6, -36, yc - 1, 5, "minecraft:stripped_oak_wood"))
            # Glass front wall with open double doorway (-35, Z=-6..5)
            cmds.append(fill(-35, yf + 1, -6, -35, yc - 1, 5, "minecraft:white_stained_glass"))
            cmds.append(fill(-35, yf + 1, -2, -35, yf + 3, 1, "minecraft:air"))
            # Lobby ceiling lights
            cmds.append(setblock(-39, yc - 1, -2, "minecraft:sea_lantern"))
            cmds.append(setblock(-39, yc - 1, 2, "minecraft:sea_lantern"))
            # 4-color recycling bins outside elevator lobby (seen in 7thFloor.jpg)
            cmds.append(setblock(-34, yf + 1, 3, "minecraft:yellow_concrete"))
            cmds.append(setblock(-34, yf + 1, 4, "minecraft:blue_concrete"))
            cmds.append(setblock(-34, yf + 1, 5, "minecraft:green_concrete"))
            cmds.append(setblock(-34, yf + 1, 6, "minecraft:red_concrete"))

        # Floor Indicator Sign right next to elevator doors
        cmds.append(wall_sign(-41, yf + 2, -1, "east", f"[ {fid} ]", fl["name"][:15], "Use /trigger", "if_floor set 1..11"))

        # Walkable Main Staircase (-48..-42, Z=8..14) connecting B1 -> 11F
        if idx < len(floors) - 2:  # up to 11F
            next_yf = floors[idx + 1]["y_floor"]
            height = next_yf - yf
            # Cut stairwell opening in upper slab
            cmds.append(fill(-48, next_yf, 9, -42, next_yf, 13, "minecraft:air"))
            # Staircase side walls
            cmds.append(fill(-49, yf + 1, 8, -42, next_yf, 8, "minecraft:white_concrete"))
            cmds.append(fill(-49, yf + 1, 14, -42, next_yf, 14, "minecraft:white_concrete"))
            # Build steps ascending West (-43 -> -48)
            for s in range(height):
                sx = -43 - min(s, 5)
                sy = yf + 1 + s
                cmds.append(fill(sx, sy, 9, sx, sy, 13, "minecraft:smooth_quartz_stairs[facing=west]"))
            # Guardrail around upper stairwell
            cmds.append(fill(-48, next_yf + 1, 8, -42, next_yf + 1, 8, "minecraft:glass_pane"))

        # South-West Fire Staircase Core (-58..-53, Z=17..22)
        if idx < len(floors) - 2:
            next_yf = floors[idx + 1]["y_floor"]
            cmds.append(fill(-57, next_yf, 18, -54, next_yf, 21, "minecraft:air"))
            for s in range(next_yf - yf):
                sx = -54 - (s % 4)
                cmds.append(fill(sx, yf + 1 + s, 18, sx, yf + 1 + s, 21, "minecraft:stone_brick_stairs[facing=west]"))

    # Seal stairwell walls at -58..-53, Z=17..22 exterior
    cmds.append(fill(-58, -5, 17, -53, 58, 17, "minecraft:gray_concrete"))
    cmds.append(fill(-58, -5, 22, -53, 58, 22, "minecraft:gray_concrete"))
    cmds.append(fill(-58, -5, 17, -58, 58, 22, "minecraft:gray_concrete"))
    return cmds


def gen_podium_and_arch() -> list[str]:
    cmds = [
        "# 04 - Front Podium (1F-4F) & Iconic C-Shaped Sweeping Canopy Arch",
        fill(-15, 0, -16, -2, 0, 14, "minecraft:smooth_sandstone"),
        fill(-15, 6, -14, -3, 6, 12, "minecraft:light_gray_concrete"),
        fill(-15, 12, -14, -3, 12, 12, "minecraft:light_gray_concrete"),
        fill(-15, 17, -14, -3, 17, 12, "minecraft:light_gray_concrete"),

        # 2F Outdoor Terrace with glass railings (Z=-14..-8, X=-15..-3)
        fill(-15, 7, -14, -3, 7, -14, "minecraft:light_blue_stained_glass_pane"),
        fill(-3, 7, -14, -3, 7, -8, "minecraft:light_blue_stained_glass_pane"),

        # Podium upper facade box (Y=12..21, X=-3, Z=-13..11) in gray concrete + blue stripe accents
        fill(-3, 12, -13, -3, 20, 11, "minecraft:gray_concrete"),
        fill(-3, 14, -9, -3, 14, -4, "minecraft:blue_concrete"),
        fill(-3, 16, 2, -3, 16, 7, "minecraft:blue_concrete"),
        fill(-3, 18, -5, -3, 18, 0, "minecraft:blue_concrete"),
        fill(-3, 15, -8, -3, 15, -5, "minecraft:light_blue_stained_glass"),
        fill(-3, 15, 1, -3, 15, 6, "minecraft:light_blue_stained_glass"),
        fill(-3, 19, -10, -3, 19, -7, "minecraft:light_blue_stained_glass"),

        # Podium recessed glass curtain wall (2F Y=7..11)
        fill(-5, 7, -12, -5, 11, 10, "minecraft:cyan_stained_glass"),

        # Left (South) cluster of 6 slender white columns + circular skylight ring (Front.jpg)
        fill(-1, 0, 11, -1, 21, 11, "minecraft:quartz_pillar"),
        fill(1, 0, 13, 1, 21, 13, "minecraft:quartz_pillar"),
        fill(-3, 0, 13, -3, 21, 13, "minecraft:quartz_pillar"),
        fill(0, 0, 15, 0, 21, 15, "minecraft:quartz_pillar"),
        fill(-2, 0, 15, -2, 21, 15, "minecraft:quartz_pillar"),
        fill(-1, 0, 16, -1, 21, 16, "minecraft:quartz_pillar"),
        # Right (North) tall white pillar
        fill(-1, 0, -13, -1, 21, -13, "minecraft:quartz_pillar"),

        # Left-side Cobalt Blue Entrance Core Wall (seen in Front.jpg & 1stFloor.jpg)
        fill(-12, 0, 14, -6, 11, 15, "minecraft:blue_concrete"),

        # Sweeping C-Shaped Canopy Arch Roof (Y=22..23)
        fill(-14, 22, -16, 2, 22, 15, "minecraft:smooth_quartz"),
        fill(-14, 23, -16, 2, 23, 15, "minecraft:light_gray_concrete"),
        # Circular skylight oculus cutout above the 6 pillars
        fill(-2, 22, 12, 0, 23, 14, "minecraft:air"),
    ]

    seen_pts = set()
    for deg in range(-75, 195, 3):
        rad = math.radians(deg)
        cz = round(10 + 9.0 * math.sin(rad))
        cy = round(14.5 + 8.0 * math.cos(rad))
        for cx in range(-12, 1):
            pt = (cx, cy, cz)
            if pt not in seen_pts:
                seen_pts.add(pt)
                mat = "minecraft:smooth_quartz" if cx % 2 == 0 else "minecraft:light_gray_concrete"
                cmds.append(setblock(cx, cy, cz, mat))
    return cmds


def gen_facade_shell() -> list[str]:
    cmds = [
        "# 05 - Main Tower Exterior Facade, Step-Back Wing (8F-11F) & Protruding Glass Box (6F-8F)",
        # East face lower tower (Y=22..36 full width Z=-23..22)
        fill(-16, 22, -23, -16, 36, 22, "minecraft:light_blue_stained_glass", "keep"),
        # East face upper tower step-back (Y=37..51): South-East wing at X=-16 (Z=-8..22), North-East steps back to X=-26 (Z=-23..-9)
        fill(-16, 37, -8, -16, 51, 22, "minecraft:light_blue_stained_glass", "keep"),
        fill(-26, 37, -23, -26, 51, -9, "minecraft:light_blue_stained_glass", "keep"),
        # Step-back cross wall along Z=-8 (X=-26..-16, Y=37..58)
        fill(-26, 37, -8, -16, 58, -8, "minecraft:light_blue_stained_glass", "keep"),

        # Protruding 3-storey glass corner box at 6F-8F on North-East (seen in 5426_View-3.jpg!)
        fill(-20, 27, -14, -13, 41, -7, "minecraft:light_blue_stained_glass", "hollow"),
        fill(-20, 32, -14, -13, 32, -7, "minecraft:white_concrete"),
        fill(-20, 37, -14, -13, 37, -7, "minecraft:white_concrete"),

        # White horizontal floor bands on East facade
        *[fill(-16, y, -24, -16, y, 23, "minecraft:white_concrete") for y in (12, 17, 22, 27, 32, 37)],
        *[fill(-16, y, -8, -16, y, 23, "minecraft:white_concrete") for y in (42, 47, 52)],
        *[fill(-26, y, -24, -26, y, -8, "minecraft:white_concrete") for y in (42, 47, 52)],

        # Iconic Cobalt Blue vertical stripes
        fill(-16, 0, -24, -15, 36, -23, "minecraft:blue_concrete"),
        fill(-26, 37, -24, -25, 58, -23, "minecraft:blue_concrete"),
        fill(-16, 0, 22, -15, 58, 23, "minecraft:blue_concrete"),

        # Gray concrete shear walls
        fill(-22, 0, -24, -17, 36, -24, "minecraft:light_gray_concrete"),
        fill(-22, 0, 23, -17, 58, 23, "minecraft:light_gray_concrete"),

        # Dark charcoal vertical louver bands on North & South elevations
        fill(-36, 13, -24, -23, 36, -24, "minecraft:gray_concrete"),
        fill(-36, 37, -24, -27, 51, -24, "minecraft:gray_concrete"),
        fill(-36, 13, 23, -23, 51, 23, "minecraft:gray_concrete"),

        # Side windows & West rear facade
        fill(-58, 13, -24, -37, 51, -24, "minecraft:cyan_stained_glass", "keep"),
        fill(-58, 13, 23, -37, 51, 23, "minecraft:cyan_stained_glass", "keep"),
        fill(-60, 1, -23, -60, 58, 22, "minecraft:light_gray_concrete", "keep"),
        *[fill(-60, y + 1, -20, -60, y + 2, 19, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],

        # 11F Exhibition Hall wrap-around curtain wall (Y=53..58)
        fill(-16, 53, -8, -16, 58, 22, "minecraft:light_blue_stained_glass"),
        fill(-26, 53, -23, -26, 58, -9, "minecraft:light_blue_stained_glass"),
        fill(-59, 53, -24, -27, 58, -24, "minecraft:light_blue_stained_glass", "keep"),
        fill(-59, 53, 23, -17, 58, 23, "minecraft:light_blue_stained_glass", "keep"),
    ]
    return cmds


def gen_roof_and_solar() -> list[str]:
    cmds = [
        "# 06 - Roof Overhang, Parapet Sign Band & 3 Rows of Solar Panels",
        fill(-60, 59, -24, -26, 59, 23, "minecraft:gray_concrete"),
        fill(-25, 59, -8, -16, 59, 23, "minecraft:gray_concrete"),
        # Overhanging flat roof canopy (Y=62..63)
        fill(-62, 62, -26, -24, 62, 25, "minecraft:gray_concrete"),
        fill(-24, 62, -10, -14, 62, 25, "minecraft:gray_concrete"),
        fill(-62, 63, -26, -24, 63, 25, "minecraft:polished_deepslate"),
        fill(-24, 63, -10, -14, 63, 25, "minecraft:polished_deepslate"),
        # East parapet facade band for Faculty Sign (Y=60..61)
        fill(-15, 60, -8, -15, 61, 23, "minecraft:gray_concrete"),
        fill(-14, 61, 0, -14, 61, 0, "minecraft:gold_block"),
        fill(-14, 61, 2, -14, 61, 16, "minecraft:white_concrete"),
        # 3 Rows of Solar Panels on West roof (matching ESRI z19 satellite image!)
        fill(-54, 64, -18, -50, 64, 16, "minecraft:daylight_detector"),
        fill(-44, 64, -18, -40, 64, 16, "minecraft:daylight_detector"),
        fill(-34, 64, -18, -30, 64, 16, "minecraft:daylight_detector"),
    ]
    return cmds


def gen_interiors() -> list[str]:
    cmds = [
        "# 07 - Representative Interior Zoning & Furniture (1F to 11F, matched to VR Tour Panoramas)",

        # --- 1F (Y=0): Study Tables/Benches, Glass-Walled SMO, Lounge Sofas ---
        # Glass-walled SMO (Student Union) box on South-East 1F (-32..-24, Y=1..5, Z=12..21)
        fill(-32, 1, 12, -24, 5, 21, "minecraft:glass", "hollow"),
        fill(-24, 1, 15, -24, 3, 17, "minecraft:air"),  # doorway
        setblock(-28, 1, 16, "minecraft:oak_planks"),
        # 1F Student Study Tables & Benches (seen in Stairs.jpg!)
        *[fill(-34, 1, z, -24, 1, z, "minecraft:quartz_slab") for z in (-18, -14, -10)],
        *[fill(-34, 1, z - 1, -24, 1, z - 1, "minecraft:light_blue_carpet") for z in (-18, -14, -10)],
        # Dark brown leather sofas in 1F lounge (1stFloor.jpg)
        fill(-22, 1, -6, -22, 1, -3, "minecraft:dark_oak_stairs[facing=east]"),
        fill(-19, 1, -7, -17, 1, -7, "minecraft:dark_oak_stairs[facing=south]"),
        # Welcome Stand / Banner
        fill(-34, 1, 8, -34, 3, 10, "minecraft:orange_concrete"),

        # --- 2F (Y=6): Dean Office (IF-215), Digital Library Bookshelves ---
        fill(-58, 7, -22, -49, 10, -10, "minecraft:white_concrete", "hollow"),  # Dean Office wing
        fill(-49, 7, -17, -49, 9, -15, "minecraft:air"),
        fill(-56, 7, -18, -54, 7, -14, "minecraft:dark_oak_slab"),
        # Digital Library Bookshelves on 2F North-East (-32..-18, Z=-22..-12)
        *[fill(-30, 7, z, -20, 9, z, "minecraft:bookshelf") for z in (-21, -17, -13)],

        # --- 3F (Y=12) & 5F (Y=22): 210-Seat Sloped Lecture Hall (IF-3M210 / IF-5M210) & Computer Lab ---
        # Lecture Hall occupies North-West zone (-58..-38, Z=-22..-9)
        *[
            cmd
            for y_base, room_name in [(12, "IF-3M210"), (22, "IF-5M210")]
            for cmd in [
                # Beige/tan acoustic walls (LectureHall1.jpg)
                fill(-58, y_base + 1, -22, -38, y_base + 4, -9, "minecraft:white_terracotta", "hollow"),
                fill(-38, y_base + 1, -17, -38, y_base + 3, -14, "minecraft:air"),  # Double doors
                # Giant Projector Screen on West wall (-57)
                fill(-57, y_base + 2, -19, -57, y_base + 4, -12, "minecraft:white_concrete"),
                # Lecturer Desk & Low Curved Podium Wall
                fill(-54, y_base + 1, -17, -54, y_base + 1, -14, "minecraft:dark_oak_planks"),
                # Tiered Cyan/Teal Theater Seating rising Eastward (-50 -> -41)
                fill(-50, y_base + 1, -20, -49, y_base + 1, -11, "minecraft:warped_stairs[facing=west]"),
                fill(-47, y_base + 1, -20, -45, y_base + 1, -11, "minecraft:smooth_quartz"),
                fill(-47, y_base + 2, -20, -46, y_base + 2, -11, "minecraft:warped_stairs[facing=west]"),
                fill(-44, y_base + 1, -20, -41, y_base + 2, -11, "minecraft:smooth_quartz"),
                fill(-44, y_base + 3, -20, -42, y_base + 3, -11, "minecraft:warped_stairs[facing=west]"),
                wall_sign(-37, y_base + 2, -16, "east", room_name, "Lecture Hall", "210 Seats"),
            ]
        ],

        # Computer Labs on 3F & 4F South Wing (-34..-18, Z=10..21) matching CompRoom1.jpg
        *[
            cmd
            for y_base, lab_name in [(12, "IF-3C01"), (17, "IF-4C01")]
            for cmd in [
                fill(-34, y_base + 1, 10, -18, y_base + 4, 21, "minecraft:light_blue_terracotta", "hollow"),
                fill(-34, y_base + 1, 14, -34, y_base + 3, 16, "minecraft:air"),
                # 2 Long Rows of White Computer Desks + Black Monitors + Cyan Chairs
                fill(-31, y_base + 1, 13, -21, y_base + 1, 13, "minecraft:quartz_slab"),
                fill(-31, y_base + 1, 18, -21, y_base + 1, 18, "minecraft:quartz_slab"),
                *[setblock(x, y_base + 2, 13, "minecraft:black_concrete") for x in range(-30, -21, 2)],
                *[setblock(x, y_base + 2, 18, "minecraft:black_concrete") for x in range(-30, -21, 2)],
                *[setblock(x, y_base + 1, 14, "minecraft:warped_stairs[facing=north]") for x in range(-30, -21, 2)],
                *[setblock(x, y_base + 1, 17, "minecraft:warped_stairs[facing=south]") for x in range(-30, -21, 2)],
                wall_sign(-35, y_base + 2, 15, "west", lab_name, "Computer Lab"),
            ]
        ],

        # --- 4F (Y=17): Server Room (-58..-50, Z=8..15) ---
        fill(-58, 18, 8, -50, 21, 15, "minecraft:gray_concrete", "hollow"),
        *[fill(-56, 18, z, -52, 20, z, "minecraft:black_concrete") for z in (10, 13)],
        *[setblock(x, 19, 10, "minecraft:redstone_lamp[lit=true]") for x in (-55, -53)],
        wall_sign(-49, 19, 11, "east", "4F Server Room", "BUU Informatics"),

        # --- 7F (Y=32): Student Creative Co-Working Space & FabLab / Maker Space ---
        *[fill(-32, 33, z, -22, 33, z, "minecraft:oak_slab") for z in (-18, -12, 12)],
        setblock(-28, 33, -15, "minecraft:crafting_table"),
        setblock(-26, 33, -15, "minecraft:crafter"),
        setblock(-24, 33, -15, "minecraft:iron_block"),
        wall_sign(-34, 34, -10, "east", "7F FabLab", "Maker Space &", "Co-Working"),

        # --- 8F (Y=37): Research Labs & Eastern Software Park BUU (IF-8R08) ---
        fill(-32, 38, 10, -18, 41, 21, "minecraft:white_concrete", "hollow"),
        fill(-32, 38, 14, -32, 40, 16, "minecraft:air"),
        wall_sign(-33, 39, 15, "west", "IF-8R08", "Eastern Software", "Park BUU"),

        # --- 9F (Y=42): Lecturer Offices (IF-908A..D) ---
        *[fill(-32, 43, z, -18, 46, z, "minecraft:white_concrete") for z in (8, 13, 18)],
        wall_sign(-33, 44, 10, "west", "9F Offices", "IF-908A - D"),

        # --- 10F (Y=47): Hall of Fame & Conference Room (IF-10M56 / IF-10M60) ---
        fill(-58, 48, -22, -48, 51, -10, "minecraft:white_concrete", "hollow"),
        fill(-48, 48, -17, -48, 50, -14, "minecraft:air"),
        fill(-56, 48, -18, -51, 48, -14, "minecraft:dark_oak_planks"),  # Conference table
        # Hall of Fame trophy pedestals
        *[setblock(x, 48, -6, "minecraft:quartz_pillar") for x in (-32, -28, -24)],
        *[setblock(x, 49, -6, "minecraft:gold_block") for x in (-32, -28, -24)],

        # --- 11F (Y=52): Exhibition Hall (IF-11M280) + Red Fire Hose Cabinets ---
        setblock(-58, 53, -22, "minecraft:red_concrete"),
        setblock(-58, 54, -22, "minecraft:red_concrete"),
        # Open House Exhibition Booths
        *[fill(x, 53, 10, x + 2, 53, 12, "minecraft:blue_concrete") for x in (-54, -46, -30, -22)],
        *[setblock(x + 1, 54, 11, "minecraft:sea_lantern") for x in (-54, -46, -30, -22)],
        wall_sign(-34, 54, 0, "east", "11F Exhibition", "Hall IF-11M280", "Open House Showcase"),
    ]
    return cmds


def gen_interactive_openhouse(spec: dict) -> dict[str, list[str]]:
    # Remember: ~0 ~0 ~0 is front stairs; elevator lobby inside building is at X=-39, Z=-1
    # We store anchor coordinates in scoreboard or use a marker entity named 'if_buu_origin'
    # spawned at the origin when build_all runs! That makes /trigger if_floor teleport accurately
    # from ANYWHERE in the world!
    init_cmds = [
        "# Setup Open House /trigger elevator scoreboard and spawn origin marker",
        "scoreboard objectives add if_floor trigger",
        "kill @e[type=minecraft:marker,tag=if_buu_origin]",
        "summon minecraft:marker ~0 ~0 ~0 {Tags:[\"if_buu_origin\"]}",
        "scoreboard players enable @a if_floor",
    ]

    menu_lines = [
        'tellraw @s [{"text":"\\n=== ลิฟต์อาคารคณะวิทยาการสารสนเทศ (IF-BUU 1:1) ===","color":"aqua","bold":true}]',
        'tellraw @s [{"text":"พิมพ์คำสั่ง /trigger if_floor set <เลขชั้น> หรือคลิกชั้นที่ต้องการ:","color":"gray"}]',
    ]

    tick_cmds = [
        "scoreboard players enable @a if_floor",
    ]

    floor_num_map = [
        (0, "B1", -5, "ลานจอดรถใต้ดิน (Basement Car Park)"),
        (1, "1F", 0, "โถงกิจกรรม / สโมสรนิสิต (SMO) / จุดคัดกรอง"),
        (2, "2F", 6, "สำนักงานคณบดี / ห้องสมุดดิจิทัล / ระเบียง"),
        (3, "3F", 12, "ห้องปฏิบัติการคอมฯ / ห้องบรรยาย IF-3M210"),
        (4, "4F", 17, "ห้องแล็บคอมฯ / ห้องบริการเครื่องแม่ข่าย (Server)"),
        (5, "5F", 22, "ห้องเรียนรวม IF-5T03 / ห้องบรรยาย IF-5M210"),
        (6, "6F", 27, "ห้องเรียนและห้องคอมพิวเตอร์ IF-6T01..05"),
        (7, "7F", 32, "Co-Working Space / FabLab & Maker Space"),
        (8, "8F", 37, "ห้องปฏิบัติการวิจัย / Eastern Software Park BUU"),
        (9, "9F", 42, "ห้องพักอาจารย์ IF-908A..D"),
        (10, "10F", 47, "ห้องเกียรติยศ (Hall of Fame) / ห้องประชุม"),
        (11, "11F", 52, "ห้องนิทรรศการ Exhibition Hall (IF-11M280)"),
    ]

    for num, code, y_fl, desc in floor_num_map:
        tp_y = y_fl + 1
        menu_lines.append(
            f'tellraw @s [{{"text":"[{code}] ","color":"gold","bold":true,'
            f'"click_event":{{"action":"run_command","command":"/trigger if_floor set {num}"}},'
            f'"clickEvent":{{"action":"run_command","command":"/trigger if_floor set {num}"}}}},'
            f'{{"text":"{desc}","color":"white"}}]'
        )
        # Note: in tick_cmds, when a player triggers if_floor == num (use 99 for B1 because 0 is default unset! Let's map B1 -> 99 or 100, and 1..11 -> 1..11!)
        score_val = 99 if num == 0 else num
        if num == 0:
            # replace 0 with 99 in menu command too
            menu_lines[-1] = menu_lines[-1].replace("if_floor set 0", "if_floor set 99")
        tick_cmds.append(
            f"execute as @a[scores={{if_floor={score_val}}}] at @e[type=minecraft:marker,tag=if_buu_origin,limit=1] "
            f"run tp @s ~-39 ~{tp_y} ~-1 -90 0"
        )
        tick_cmds.append(
            f'execute as @a[scores={{if_floor={score_val}}}] run title @s actionbar '
            f'{{"text":"ชั้น {code} — {desc}","color":"aqua"}}'
        )
        tick_cmds.append(f"scoreboard players reset @a[scores={{if_floor={score_val}}}] if_floor")

    guide_cmds = [
        "function if_buu:elevator_menu",
        'tellraw @s [{"text":"[หน้าตึก] ","color":"green","bold":true,'
        '"click_event":{"action":"run_command","command":"/trigger if_floor set 1"},'
        '"clickEvent":{"action":"run_command","command":"/trigger if_floor set 1"}},'
        '{"text":"ใช้คำสั่ง /function if_buu:elevator_menu เพื่อเปิดเมนูลิฟต์ได้ตลอดเวลา","color":"gray"}]',
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
            "description": "Faculty of Informatics, Burapha University (1:1 Scale Builder + Open House Elevator)",
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

    interactive = gen_interactive_openhouse(spec)
    for fname, flines in interactive.items():
        write_func(fname, flines)

    # Register tick & load function tags so /trigger if_floor works automatically every tick!
    (TAGS_FUNC_DIR / "tick.json").write_text(json.dumps({"values": ["if_buu:elevator_tick"]}, indent=2), encoding="utf-8")
    (TAGS_FUNC_DIR / "load.json").write_text(json.dumps({"values": ["if_buu:init_openhouse"]}, indent=2), encoding="utf-8")

    # Clear area helper (chunked so every /fill stays <= 32,768 blocks)
    clear_cmds = ["# Clear 1:1 building bounding volume before rebuilding"]
    for y_start, y_end in [(-6, 4), (5, 15), (16, 26), (27, 37), (38, 48), (49, 59), (60, 66)]:
        for x_start, x_end in [(-74, -44), (-43, -12), (-11, 22)]:
            clear_cmds.append(fill(x_start, y_start, -34, x_end, y_end, 34, "minecraft:air"))
    clear_cmds.append("kill @e[type=minecraft:marker,tag=if_buu_origin]")
    clear_cmds.append('tellraw @a {"text":"[IF-BUU 1:1] Cleared building zone.","color":"yellow"}')
    write_func("clear_area", clear_cmds)

    # Master build function
    write_func(
        "build_all",
        [
            "function if_buu:01_site_road",
            "function if_buu:02_basement_and_grid",
            "function if_buu:03_slabs_and_core",
            "function if_buu:04_podium_and_arch",
            "function if_buu:05_facade_shell",
            "function if_buu:06_roof_and_solar",
            "function if_buu:07_interiors",
            "function if_buu:init_openhouse",
            'tellraw @a {"text":"[IF-BUU 1:1] Built Faculty of Informatics 11-storey 1:1 building + interiors + elevator!","color":"aqua"}',
        ],
    )

    print(f"Generated Enhanced Minecraft 1:1 Datapack -> {DP_ROOT}")
    for f in sorted(FUNC_DIR.glob("*.mcfunction")):
        line_count = len(f.read_text(encoding="utf-8").splitlines())
        print(f"  - if_buu:{f.stem} ({line_count} lines)")


if __name__ == "__main__":
    main()
