"""
Generate a Minecraft Java 1.21+ Datapack (world/datapacks/if_buu_1to1) — v2.0
Builds the 1:1 Faculty of Informatics building, Burapha University (BUU):
  01_site_road            - Fueang Fa Rd, crosswalk, brick sidewalk, front plaza, moto parking, trees
  02_basement_and_grid    - Basement car park (B1) & structural white concrete column grid
  03_slabs_and_core       - 11 floor slabs, signature floor tiles, walkable main/fire stairs,
                            corridor ceiling downlights, toilets, and glass-walled elevator lobbies
  04_podium_and_arch      - Light-gray stone Podium (1F-4F), curved front canopy overhang,
                            5 ribbed sweeping C-arch fins, wheelchair ramp, 6 slender pillars,
                            cobalt blue entrance wall, 2F terrace
  05_facade_shell         - Accurate tower shear walls, dark window mullions, white projecting ledges,
                            charcoal side louvers, 8F-11F step-back wing, 6F-8F protruding glass box
  06_roof_and_solar       - Double-tiered roof overhang, attic band, 3D Faculty sign + gold emblem,
                            and 3 solar panel arrays
  07_interiors            - 1F SMO/study tables, 2F Digital Library/Dean Office, 3F/5F 210-seat
                            Sloped Lecture Halls & Comp Labs, 4F Server Room, 7F BUU Open House 2026
                            Innovation Hub (Vision Lab + DMI Lab + FabLab), 8F Software Park,
                            9F Offices, 10F Hall of Fame, 11F Exhibition Hall
  08_interactive_openhouse - /trigger if_floor elevator system (non-OP) + clickable menu + 7F shortcut
  09_campus_context       - Surrounding BUU landmarks: NW circular fountain plaza, South 5F building,
                            and East Computer Center / Science CL frontage across Fueang Fa Rd.

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
    msgs = [
        json.dumps(line1, ensure_ascii=False),
        json.dumps(line2, ensure_ascii=False),
        json.dumps(line3, ensure_ascii=False),
        json.dumps(line4, ensure_ascii=False),
    ]
    nbt = "{front_text:{messages:[" + ",".join(f'\'{{"text":{m}}}\'' for m in msgs) + "]}}"
    return f"setblock ~{x} ~{y} ~{z} minecraft:oak_wall_sign[facing={facing}]{nbt}"


def text_display(x: float, y: float, z: float, text: str, yaw: float, scale: float = 1.5, tag: str = "if_buu_label") -> str:
    escaped = json.dumps(text, ensure_ascii=False)
    return (
        f'summon minecraft:text_display ~{x} ~{y} ~{z} '
        f'{{Tags:["{tag}"],text:{{text:{escaped},color:"white",bold:true}},'
        f'Rotation:[{yaw}f,0f],billboard:"fixed",background:0,'
        f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
        f'translation:[0f,0f,0f],scale:[{scale}f,{scale}f,{scale}f]}}}}'
    )


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
        # Trees along sidewalk & plaza planters
        *[fill(4, 0, z, 4, 2, z, "minecraft:oak_log") for z in (-22, -14, 16, 22)],
        *[fill(3, 3, z - 1, 5, 4, z + 1, "minecraft:oak_leaves[persistent=true]") for z in (-22, -14, 16, 22)],
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
        *[fill(-56, -6, z, -48, -6, z, "minecraft:yellow_concrete") for z in range(-20, 20, 6)],
        *[fill(-34, -6, z, -24, -6, z, "minecraft:yellow_concrete") for z in range(-20, 20, 6)],
        fill(-60, -5, -24, -16, -1, -24, "minecraft:stone_bricks"),
        fill(-60, -5, 23, -16, -1, 23, "minecraft:stone_bricks"),
        fill(-60, -5, -24, -60, -1, 23, "minecraft:stone_bricks"),
        fill(-16, -5, -24, -16, -1, 23, "minecraft:stone_bricks"),
    ]
    xs = [-60, -49, -38, -27, -16]
    zs = [-24, -12, 0, 12, 23]
    for x in xs:
        for z in zs:
            top_y = 36 if (x == -16 and z <= -12) else 58
            cmds.append(fill(x, -5, z, x, top_y, z, "minecraft:white_concrete"))
    return cmds


def gen_slabs_and_core(spec: dict) -> list[str]:
    cmds = ["# 03 - 11 Floor Slabs, Signature Tile Pattern, Walkable Stairs, Toilets & Glass Elevator Lobbies"]
    floors = spec["floors"]

    for fl in floors:
        fid = fl["id"]
        yf = fl["y_floor"]
        yc = fl["y_ceiling"]
        if fid in ("B1", "RF"):
            continue

        # Step-back on North-East wing for 8F-11F (seen in 5426_View-3.jpg)
        if fid in ("8F", "9F", "10F", "11F"):
            cmds.append(fill(-60, yf, -24, -26, yf, 23, "minecraft:smooth_sandstone" if fid == "11F" else "minecraft:smooth_quartz"))
            cmds.append(fill(-25, yf, -8, -16, yf, 23, "minecraft:smooth_sandstone" if fid == "11F" else "minecraft:smooth_quartz"))
        else:
            base_mat = "minecraft:smooth_sandstone" if fid in ("1F", "2F") else "minecraft:smooth_quartz"
            cmds.append(fill(-60, yf, -24, -16, yf, 23, base_mat))

        # Exterior crisp white horizontal floor ledge projecting 1 block outward
        cmds.append(fill(-61, yf, -25, -15 if fid not in ("8F", "9F", "10F", "11F") else -26, yf, -25, "minecraft:smooth_quartz"))
        cmds.append(fill(-61, yf, 24, -15, yf, 24, "minecraft:smooth_quartz"))
        cmds.append(fill(-61, yf, -25, -61, yf, 24, "minecraft:smooth_quartz"))

        # Random/checker accent tiles on 1F, 2F, 7F, 11F matching VR Tour panoramas
        if fid in ("1F", "2F", "7F", "11F"):
            for x in range(-58, -18, 5):
                for z in range(-22, 22, 5):
                    if fid == "7F" and x > -26 and z < -8:
                        continue
                    mat = "minecraft:gray_concrete" if (x + z) % 2 == 0 else "minecraft:light_gray_concrete"
                    cmds.append(setblock(x, yf, z, mat))

        # Corridor ceiling downlights (warm interior glow in BlueMap & in-game!)
        for x in (-34, -28, -22):
            for z in (-16, -6, 4, 14):
                if fid in ("8F", "9F", "10F", "11F") and x >= -25 and z < -8:
                    continue
                cmds.append(setblock(x, yc - 1, z, "minecraft:sea_lantern"))

    # Central Elevator Core (-48..-42, Z=-6..5) & Restrooms Core (-58..-50, Z=-6..5)
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

        if fid != "B1":
            # Elevator Lobby enclosure (matching Lift.jpg & 7thFloor.jpg)
            cmds.append(fill(-41, yf + 1, -7, -36, yc - 1, -7, "minecraft:light_blue_terracotta"))
            cmds.append(fill(-41, yf + 1, 6, -36, yc - 1, 6, "minecraft:light_blue_terracotta"))
            cmds.append(fill(-41, yc - 1, -6, -36, yc - 1, 5, "minecraft:blue_terracotta"))
            cmds.append(fill(-37, yc - 1, -6, -36, yc - 1, 5, "minecraft:stripped_oak_wood"))
            cmds.append(fill(-35, yf + 1, -6, -35, yc - 1, 5, "minecraft:white_stained_glass"))
            cmds.append(fill(-35, yf + 1, -2, -35, yf + 3, 1, "minecraft:air"))
            cmds.append(setblock(-39, yc - 1, -2, "minecraft:sea_lantern"))
            cmds.append(setblock(-39, yc - 1, 2, "minecraft:sea_lantern"))
            # 4-color recycling bins outside elevator lobby
            cmds.append(setblock(-34, yf + 1, 3, "minecraft:yellow_concrete"))
            cmds.append(setblock(-34, yf + 1, 4, "minecraft:blue_concrete"))
            cmds.append(setblock(-34, yf + 1, 5, "minecraft:green_concrete"))
            cmds.append(setblock(-34, yf + 1, 6, "minecraft:red_concrete"))

            # Restrooms block behind elevator core (-58..-50, Z=-5..4) on 1F-10F
            if fid != "11F":
                cmds.append(fill(-58, yf + 1, -5, -50, yc - 1, 4, "minecraft:white_concrete", "hollow"))
                cmds.append(fill(-50, yf + 1, -2, -50, yf + 3, -1, "minecraft:air"))
                cmds.append(fill(-50, yf + 1, 2, -50, yf + 3, 2, "minecraft:air"))
                cmds.append(setblock(-54, yc - 1, 0, "minecraft:sea_lantern"))

        cmds.append(wall_sign(-41, yf + 2, -1, "east", f"[ {fid} ]", fl["name"][:15], "Use /trigger", "if_floor set 1..11"))

        # Walkable Main Staircase (-48..-42, Z=8..14) connecting B1 -> 11F
        if idx < len(floors) - 2:
            next_yf = floors[idx + 1]["y_floor"]
            height = next_yf - yf
            cmds.append(fill(-48, next_yf, 9, -42, next_yf, 13, "minecraft:air"))
            cmds.append(fill(-49, yf + 1, 8, -42, next_yf, 8, "minecraft:white_concrete"))
            cmds.append(fill(-49, yf + 1, 14, -42, next_yf, 14, "minecraft:white_concrete"))
            for s in range(height):
                sx = -43 - min(s, 5)
                sy = yf + 1 + s
                cmds.append(fill(sx, sy, 9, sx, sy, 13, "minecraft:smooth_quartz_stairs[facing=west]"))
            cmds.append(fill(-48, next_yf + 1, 8, -42, next_yf + 1, 8, "minecraft:glass_pane"))

        # South-West Fire Staircase Core (-58..-53, Z=17..22)
        if idx < len(floors) - 2:
            next_yf = floors[idx + 1]["y_floor"]
            cmds.append(fill(-57, next_yf, 18, -54, next_yf, 21, "minecraft:air"))
            for s in range(next_yf - yf):
                sx = -54 - (s % 4)
                cmds.append(fill(sx, yf + 1 + s, 18, sx, yf + 1 + s, 21, "minecraft:stone_brick_stairs[facing=west]"))

    cmds.append(fill(-58, -5, 17, -53, 58, 17, "minecraft:light_gray_concrete"))
    cmds.append(fill(-58, -5, 22, -53, 58, 22, "minecraft:light_gray_concrete"))
    cmds.append(fill(-58, -5, 17, -58, 58, 22, "minecraft:light_gray_concrete"))
    return cmds


def gen_podium_and_arch() -> list[str]:
    cmds = [
        "# 04 - v2.0 Refined Light-Gray Podium (1F-4F) & 5-Ribbed Sweeping C-Shaped Canopy Arch",
        fill(-15, 0, -16, -2, 0, 14, "minecraft:smooth_sandstone"),
        fill(-15, 6, -14, -3, 6, 12, "minecraft:light_gray_concrete"),
        fill(-15, 12, -14, -3, 12, 12, "minecraft:light_gray_concrete"),
        fill(-15, 17, -14, -3, 17, 12, "minecraft:light_gray_concrete"),

        # 2F Outdoor Terrace with glass railings (Z=-14..-8, X=-15..-3)
        fill(-15, 7, -14, -3, 7, -14, "minecraft:light_blue_stained_glass_pane"),
        fill(-3, 7, -14, -3, 7, -8, "minecraft:light_blue_stained_glass_pane"),

        # Podium Upper Facade Box (Light-Gray stone cladding matching 5426_View-3.jpg!)
        fill(-3, 12, -13, -3, 20, 11, "minecraft:light_gray_concrete"),
        # Subtle horizontal stone panel grooves
        fill(-3, 14, -13, -3, 14, 11, "minecraft:polished_andesite"),
        fill(-3, 17, -13, -3, 17, 11, "minecraft:polished_andesite"),
        # Angled/stepped bottom edge on North side of Podium box (Y=12..13 carved open above 2F)
        fill(-3, 12, -13, -3, 13, -6, "minecraft:air"),
        fill(-3, 12, -5, -3, 12, 0, "minecraft:air"),
        # Scattered cobalt blue accent bands
        fill(-3, 15, -11, -3, 15, -7, "minecraft:blue_concrete"),
        fill(-3, 16, 4, -3, 16, 9, "minecraft:blue_concrete"),
        fill(-3, 18, -3, -3, 18, 2, "minecraft:blue_concrete"),
        # Scattered framed horizontal windows on Podium
        fill(-3, 16, -10, -3, 16, -6, "minecraft:light_blue_stained_glass"),
        fill(-3, 15, 1, -3, 15, 6, "minecraft:light_blue_stained_glass"),
        fill(-3, 19, -11, -3, 19, -7, "minecraft:light_blue_stained_glass"),
        # Side glass curtain on North & South faces of Podium (2F-4F)
        fill(-14, 7, -14, -4, 20, -14, "minecraft:cyan_stained_glass", "keep"),
        fill(-14, 12, 12, -4, 20, 12, "minecraft:cyan_stained_glass", "keep"),

        # Podium recessed dark-framed glass curtain wall (2F Y=7..11)
        fill(-5, 7, -12, -5, 11, 10, "minecraft:cyan_stained_glass"),
        fill(-5, 9, -12, -5, 9, 10, "minecraft:gray_concrete"),  # horizontal mullion

        # Left (South) cluster of 6 slender white columns under circular oculus skylight (Front.jpg)
        fill(-1, 0, 11, -1, 21, 11, "minecraft:quartz_pillar"),
        fill(1, 0, 13, 1, 21, 13, "minecraft:quartz_pillar"),
        fill(-3, 0, 13, -3, 21, 13, "minecraft:quartz_pillar"),
        fill(0, 0, 15, 0, 21, 15, "minecraft:quartz_pillar"),
        fill(-2, 0, 15, -2, 21, 15, "minecraft:quartz_pillar"),
        fill(-1, 0, 16, -1, 21, 16, "minecraft:quartz_pillar"),
        # Right (North) tall white pillar
        fill(-1, 0, -13, -1, 21, -13, "minecraft:quartz_pillar"),

        # Left-side Cobalt Blue Entrance Core Wall
        fill(-12, 0, 14, -6, 11, 15, "minecraft:blue_concrete"),
    ]

    # v2.0 Curved Canopy Roof (smooth rounded front-east & north-east overhang at Y=22..23)
    for x in range(-15, 5):
        # Curve the North-East edge smoothly inward as x goes East
        z_min = -16 if x <= -2 else round(-16 + (x + 2) * 1.1)
        z_max = 16
        cmds.append(fill(x, 22, z_min, x, 22, z_max, "minecraft:smooth_quartz"))
        cmds.append(fill(x, 23, z_min, x, 23, z_max, "minecraft:light_gray_concrete"))

    # Cut crisp circular oculus skylight above the 6 columns
    cmds.append(fill(-2, 22, 12, 0, 23, 14, "minecraft:air"))

    # v2.0 5 Parallel Ribbed Silver C-Arch Fins sweeping down on South (+Z) side
    fin_xs = [-12, -9, -6, -3, 0]
    seen_fin_pts = set()
    for deg in range(-70, 195, 2):
        rad = math.radians(deg)
        cz = round(11 + 8.5 * math.sin(rad))
        cy = round(14.5 + 8.0 * math.cos(rad))
        for cx in fin_xs:
            for dx in (0, 1):
                pt = (cx + dx, cy, cz)
                if pt not in seen_fin_pts:
                    seen_fin_pts.add(pt)
                    mat = "minecraft:smooth_quartz" if dx == 0 else "minecraft:light_gray_concrete"
                    cmds.append(setblock(cx + dx, cy, cz, mat))

    # Podium Front Faculty Signage (text_display)
    cmds.append(text_display(-2.4, 18.2, 4.0, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", -90.0, 1.35))
    return cmds


def gen_facade_shell() -> list[str]:
    cmds = [
        "# 05 - v2.0 Accurate Tower Facade: Flanking Shear Walls, Dark Mullions, Louvers & Step-Back",
        # --- Solid Flanking Light-Gray Concrete Shear Walls & Cobalt Blue Vertical Cores ---
        # South-East solid corner (Z=19..23, X=-20..-16, Y=0..58)
        fill(-20, 0, 19, -16, 58, 23, "minecraft:light_gray_concrete"),
        fill(-16, 0, 22, -15, 58, 23, "minecraft:blue_concrete"),
        # North-East solid corner (1F-7F at X=-20..-16, Z=-24..-20; 8F-11F stepped back to X=-26)
        fill(-20, 0, -24, -16, 36, -20, "minecraft:light_gray_concrete"),
        fill(-16, 0, -24, -15, 36, -23, "minecraft:blue_concrete"),
        fill(-26, 37, -24, -25, 58, -20, "minecraft:light_gray_concrete"),
        fill(-26, 37, -24, -25, 58, -23, "minecraft:blue_concrete"),

        # --- Dark Charcoal Louver Screen Panels Flanking Curtain Wall ---
        # South-East louver screen bay (Z=14..18, X=-16, Y=12..58)
        fill(-16, 12, 14, -16, 58, 18, "minecraft:gray_concrete"),
        *[fill(-15, y, 15, -15, y, 17, "minecraft:deepslate_tile_wall") for y in range(13, 58, 2)],
        # North-East louver bay (Z=-19..-16, X=-16, Y=12..36)
        fill(-16, 12, -19, -16, 36, -16, "minecraft:gray_concrete"),

        # --- Main East Curtain Wall Glass (X=-16) ---
        fill(-16, 22, -15, -16, 36, 13, "minecraft:light_blue_stained_glass", "keep"),
        fill(-16, 37, -8, -16, 51, 13, "minecraft:light_blue_stained_glass", "keep"),
        fill(-26, 37, -19, -26, 51, -9, "minecraft:light_blue_stained_glass", "keep"),
        # Step-back cross wall along Z=-8 (X=-26..-16, Y=37..58)
        fill(-26, 37, -8, -16, 58, -8, "minecraft:light_blue_stained_glass", "keep"),

        # Dark vertical window mullions every 5 blocks across East curtain wall
        *[fill(-16, 22, z, -16, 36, z, "minecraft:gray_concrete") for z in (-15, -10, -5, 0, 5, 10, 13)],
        *[fill(-16, 37, z, -16, 51, z, "minecraft:gray_concrete") for z in (-5, 0, 5, 10, 13)],
        *[fill(-26, 37, z, -26, 51, z, "minecraft:gray_concrete") for z in (-19, -14, -9)],

        # Protruding 3-storey glass corner box at 6F-8F on North-East (seen in 5426_View-3.jpg!)
        fill(-20, 27, -14, -13, 41, -7, "minecraft:light_blue_stained_glass", "hollow"),
        fill(-20, 32, -14, -13, 32, -7, "minecraft:white_concrete"),
        fill(-20, 37, -14, -13, 37, -7, "minecraft:white_concrete"),

        # Crisp Projecting White Horizontal Floor Ledges (at X=-15 / -25)
        *[fill(-16, y, -24, -15, y, 23, "minecraft:smooth_quartz") for y in (12, 17, 22, 27, 32, 37)],
        *[fill(-16, y, -8, -15, y, 23, "minecraft:smooth_quartz") for y in (42, 47, 52)],
        *[fill(-26, y, -24, -25, y, -8, "minecraft:smooth_quartz") for y in (42, 47, 52)],

        # Dark charcoal vertical louver bands on North & South side elevations
        fill(-36, 13, -24, -21, 36, -24, "minecraft:gray_concrete"),
        fill(-36, 37, -24, -27, 51, -24, "minecraft:gray_concrete"),
        fill(-36, 13, 23, -21, 51, 23, "minecraft:gray_concrete"),
        # Ribbed vertical louver walls on North & South sides
        *[fill(x, 13, -25, x, 36, -25, "minecraft:deepslate_brick_wall") for x in range(-35, -21, 3)],
        *[fill(x, 13, 24, x, 51, 24, "minecraft:deepslate_brick_wall") for x in range(-35, -21, 3)],

        # Side windows & West rear facade
        fill(-58, 13, -24, -37, 51, -24, "minecraft:cyan_stained_glass", "keep"),
        fill(-58, 13, 23, -37, 51, 23, "minecraft:cyan_stained_glass", "keep"),
        fill(-60, 1, -23, -60, 58, 22, "minecraft:light_gray_concrete", "keep"),
        *[fill(-60, y + 1, -20, -60, y + 2, 19, "minecraft:cyan_stained_glass") for y in (12, 17, 22, 27, 32, 37, 42, 47, 52)],

        # 11F Exhibition Hall wrap-around curtain wall (Y=53..58)
        fill(-16, 53, -8, -16, 58, 18, "minecraft:light_blue_stained_glass"),
        fill(-26, 53, -19, -26, 58, -9, "minecraft:light_blue_stained_glass"),
        fill(-59, 53, -24, -27, 58, -24, "minecraft:light_blue_stained_glass", "keep"),
        fill(-59, 53, 23, -21, 58, 23, "minecraft:light_blue_stained_glass", "keep"),
    ]
    return cmds


def gen_roof_and_solar() -> list[str]:
    cmds = [
        "# 06 - v2.0 Roof Crown, Corrugated Attic Band, 3D Faculty Sign & 3 Solar Panel Arrays",
        fill(-60, 59, -24, -26, 59, 23, "minecraft:gray_concrete"),
        fill(-25, 59, -8, -16, 59, 23, "minecraft:gray_concrete"),
        # Light-gray attic facade band above 11F glass (Y=59..61) matching 5426_View-3.jpg
        fill(-15, 59, -8, -15, 61, 23, "minecraft:light_gray_concrete"),
        fill(-15, 60, -8, -15, 60, 23, "minecraft:smooth_stone"),
        fill(-25, 59, -24, -25, 61, -9, "minecraft:light_gray_concrete"),
        # Recessed dark louver groove below roof overhang
        fill(-15, 62, -8, -15, 62, 23, "minecraft:gray_concrete"),
        # Double-tiered overhanging flat roof canopy (Y=62..64)
        fill(-62, 63, -26, -24, 63, 25, "minecraft:light_gray_concrete"),
        fill(-24, 63, -10, -13, 63, 25, "minecraft:light_gray_concrete"),
        fill(-62, 64, -26, -24, 64, 25, "minecraft:polished_deepslate"),
        fill(-24, 64, -10, -13, 64, 25, "minecraft:polished_deepslate"),
        # Gold BUU seal & crisp 3D text_display Faculty Sign on top crown
        fill(-14, 60, -2, -14, 61, -1, "minecraft:gold_block"),
        text_display(-13.8, 60.6, 8.5, "คณะวิทยาการสารสนเทศ\nFACULTY OF INFORMATICS", -90.0, 2.1),
        # 3 Rows of Solar Panels on West roof (matching ESRI z19 satellite image!)
        fill(-54, 65, -18, -50, 65, 16, "minecraft:daylight_detector"),
        fill(-44, 65, -18, -40, 65, 16, "minecraft:daylight_detector"),
        fill(-34, 65, -18, -30, 65, 16, "minecraft:daylight_detector"),
    ]
    return cmds


def gen_interiors() -> list[str]:
    cmds = [
        "# 07 - v2.0 Full Floor Zoning, Classrooms & 7F BUU Open House 2026 Innovation Hub",

        # --- 1F (Y=0): Study Tables, Glass-Walled SMO, Lounge Sofas ---
        fill(-32, 1, 12, -24, 5, 21, "minecraft:glass", "hollow"),
        fill(-24, 1, 15, -24, 3, 17, "minecraft:air"),
        setblock(-28, 1, 16, "minecraft:oak_planks"),
        wall_sign(-23, 2, 16, "east", "SMO", "Student Union", "Informatics BUU"),
        *[fill(-34, 1, z, -24, 1, z, "minecraft:quartz_slab") for z in (-18, -14, -10)],
        *[fill(-34, 1, z - 1, -24, 1, z - 1, "minecraft:light_blue_carpet") for z in (-18, -14, -10)],
        fill(-22, 1, -6, -22, 1, -3, "minecraft:dark_oak_stairs[facing=east]"),
        fill(-19, 1, -7, -17, 1, -7, "minecraft:dark_oak_stairs[facing=south]"),
        fill(-34, 1, 8, -34, 3, 10, "minecraft:orange_concrete"),

        # --- 2F (Y=6): Dean Office (IF-215), Admin Office, Digital Library ---
        fill(-58, 7, -22, -49, 10, -10, "minecraft:white_concrete", "hollow"),
        fill(-49, 7, -17, -49, 9, -15, "minecraft:air"),
        fill(-56, 7, -18, -54, 7, -14, "minecraft:dark_oak_slab"),
        wall_sign(-48, 8, -16, "east", "IF-215", "Dean Office", "Admin & Edu"),
        *[fill(-30, 7, z, -20, 9, z, "minecraft:bookshelf") for z in (-21, -17, -13)],
        wall_sign(-31, 8, -17, "west", "2F Digital", "Library"),

        # --- 3F (Y=12) & 5F (Y=22): 210-Seat Sloped Lecture Hall (IF-3M210 / IF-5M210) ---
        *[
            cmd
            for y_base, room_name in [(12, "IF-3M210"), (22, "IF-5M210")]
            for cmd in [
                fill(-58, y_base + 1, -22, -38, y_base + 4, -9, "minecraft:white_terracotta", "hollow"),
                fill(-38, y_base + 1, -17, -38, y_base + 3, -14, "minecraft:air"),
                fill(-57, y_base + 2, -19, -57, y_base + 4, -12, "minecraft:white_concrete"),
                fill(-54, y_base + 1, -17, -54, y_base + 1, -14, "minecraft:dark_oak_planks"),
                fill(-50, y_base + 1, -20, -49, y_base + 1, -11, "minecraft:warped_stairs[facing=west]"),
                fill(-47, y_base + 1, -20, -45, y_base + 1, -11, "minecraft:smooth_quartz"),
                fill(-47, y_base + 2, -20, -46, y_base + 2, -11, "minecraft:warped_stairs[facing=west]"),
                fill(-44, y_base + 1, -20, -41, y_base + 2, -11, "minecraft:smooth_quartz"),
                fill(-44, y_base + 3, -20, -42, y_base + 3, -11, "minecraft:warped_stairs[facing=west]"),
                wall_sign(-37, y_base + 2, -16, "east", room_name, "Lecture Hall", "210 Seats"),
            ]
        ],

        # --- 3F, 4F, 6F Computer Labs & Classrooms (IF-3C01, IF-4C01, IF-6T01) ---
        *[
            cmd
            for y_base, lab_name in [(12, "IF-3C01"), (17, "IF-4C01"), (27, "IF-6T01")]
            for cmd in [
                fill(-34, y_base + 1, 10, -18, y_base + 4, 21, "minecraft:light_blue_terracotta", "hollow"),
                fill(-34, y_base + 1, 14, -34, y_base + 3, 16, "minecraft:air"),
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

        # --- 5F (Y=22) & 6F (Y=27): 60-Seat Lecture Rooms (IF-5T03 / IF-6T02) ---
        fill(-34, 23, -22, -18, 26, -10, "minecraft:white_concrete", "hollow"),
        fill(-34, 23, -17, -34, 25, -15, "minecraft:air"),
        wall_sign(-35, 24, -16, "west", "IF-5T03", "Lecture 60 Seats"),

        # --- 7F (Y=32): BUU Open House & Innovation Hub 2026 Showcase Floor! ---
        # 1) Vision Lab Booth (North-East, X=-32..-18, Z=-22..-10)
        fill(-32, 33, -22, -18, 33, -10, "minecraft:light_blue_carpet"),
        # AI Vision Display Wall + Camera
        fill(-20, 33, -21, -20, 35, -16, "minecraft:black_concrete"),
        fill(-21, 34, -20, -21, 34, -17, "minecraft:sea_lantern"),
        setblock(-23, 33, -18, "minecraft:quartz_pillar"),
        setblock(-23, 34, -18, "minecraft:observer[facing=east]"),
        # Robot Arm Controls Prop
        setblock(-28, 33, -14, "minecraft:iron_block"),
        setblock(-28, 34, -14, "minecraft:oxidized_copper"),
        setblock(-28, 35, -14, "minecraft:lightning_rod[facing=up]"),
        setblock(-27, 35, -14, "minecraft:end_rod[facing=east]"),
        setblock(-26, 33, -12, "minecraft:lever[face=floor,facing=north]"),
        text_display(-25.0, 35.8, -16.0, "Vision Lab: AI Vision & Robot Arm Controls", -90.0, 0.9),

        # 2) DMI Lab Booth (South-East, X=-32..-18, Z=10..21)
        fill(-32, 33, 10, -18, 33, 21, "minecraft:cyan_carpet"),
        # AI/AR/VR Application Testing Station
        fill(-22, 33, 12, -20, 33, 14, "minecraft:quartz_slab"),
        setblock(-21, 34, 13, "minecraft:tinted_glass"),
        # Automation & Industry 5.0 Conveyor Line
        fill(-30, 33, 18, -22, 33, 18, "minecraft:smooth_stone_slab"),
        setblock(-28, 34, 18, "minecraft:crafter"),
        setblock(-25, 34, 18, "minecraft:redstone_lamp[lit=true]"),
        setblock(-23, 34, 18, "minecraft:iron_bars"),
        text_display(-25.0, 35.8, 15.5, "DMI Lab: AI/AR/VR & Industry 5.0 Demo", -90.0, 0.9),

        # 3) FabLab & Co-Working (North-West, X=-56..-38, Z=-22..-10)
        *[fill(-54, 33, z, -42, 33, z, "minecraft:oak_slab") for z in (-18, -13)],
        setblock(-48, 33, -15, "minecraft:crafting_table"),
        setblock(-46, 33, -15, "minecraft:crafter"),
        wall_sign(-34, 34, -10, "east", "7F Innovation", "Hub & FabLab", "Open House 2026"),

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
        fill(-56, 48, -18, -51, 48, -14, "minecraft:dark_oak_planks"),
        *[setblock(x, 48, -6, "minecraft:quartz_pillar") for x in (-32, -28, -24)],
        *[setblock(x, 49, -6, "minecraft:gold_block") for x in (-32, -28, -24)],

        # --- 11F (Y=52): Exhibition Hall (IF-11M280) + Red Fire Hose Cabinets ---
        setblock(-58, 53, -22, "minecraft:red_concrete"),
        setblock(-58, 54, -22, "minecraft:red_concrete"),
        *[fill(x, 53, 10, x + 2, 53, 12, "minecraft:blue_concrete") for x in (-54, -46, -30, -22)],
        *[setblock(x + 1, 54, 11, "minecraft:sea_lantern") for x in (-54, -46, -30, -22)],
        wall_sign(-34, 54, 0, "east", "11F Exhibition", "Hall IF-11M280", "Open House 2026"),
    ]
    return cmds


def gen_campus_context() -> list[str]:
    cmds = [
        "# 09 - v2.0 Surrounding BUU Campus Landmarks (Fountain Plaza, South Bldg, East Computer Center)",
        # 1) North-West Circular Fountain Plaza (seen in 5426_View-2-1.jpg & satellite tile!)
        fill(-98, -1, -56, -72, -1, -30, "minecraft:light_gray_concrete"),
    ]
    # Circular water pool centered at (-85, 0, -43) radius 9
    for dx in range(-10, 11):
        for dz in range(-10, 11):
            r = math.hypot(dx, dz)
            px, pz = -85 + dx, -43 + dz
            if r <= 6.5:
                cmds.append(setblock(px, -1, pz, "minecraft:water"))
            elif r <= 8.5:
                cmds.append(setblock(px, 0, pz, "minecraft:smooth_quartz_slab"))
                cmds.append(setblock(px, -1, pz, "minecraft:smooth_quartz"))

    # 2) Adjacent 5-Storey Gray/Blue Building to the South (Z = 38 .. 58, X = -56 .. -12, Y=0..24)
    # (Matches 5426_View-1-1.jpg & 5426_View-2-1.jpg on the left of IF!)
    cmds.extend([
        fill(-56, -1, 38, -12, -1, 58, "minecraft:light_gray_concrete"),
        fill(-56, 0, 38, -12, 24, 58, "minecraft:light_gray_concrete", "hollow"),
        # Blue vertical accent & windows on its North face (Z=38)
        fill(-30, 1, 38, -22, 23, 38, "minecraft:light_blue_concrete"),
        *[fill(x, y, 38, x + 2, y + 1, 38, "minecraft:black_stained_glass") for y in (4, 9, 14, 19) for x in range(-52, -15, 8)],
        fill(-57, 25, 37, -11, 25, 59, "minecraft:gray_concrete"),
    ])

    # 3) Across Fueang Fa Rd (East, X = 22 .. 42, Z = -28 .. 24): Computer Center / Science CL Frontage
    # (Matches the curved teal-roof white building in Front.jpg & yellow building in 5426_View-3.jpg!)
    cmds.extend([
        fill(18, -1, -32, 44, -1, 28, "minecraft:grass_block"),
        fill(18, -1, -26, 22, -1, 24, "minecraft:light_gray_concrete"),
        # White & teal curved-roof building
        fill(24, 0, -2, 42, 18, 22, "minecraft:white_concrete", "hollow"),
        *[fill(24, y, 0, 24, y, 20, "minecraft:cyan_stained_glass") for y in (3, 7, 11, 15)],
        fill(22, 19, -4, 43, 19, 23, "minecraft:cyan_concrete"),
        # Yellow adjacent wing to the North-East
        fill(24, 0, -28, 42, 16, -6, "minecraft:smooth_sandstone", "hollow"),
        *[fill(24, y, -25, 24, y, -9, "minecraft:black_stained_glass") for y in (3, 8, 13)],
        fill(23, 17, -29, 43, 17, -5, "minecraft:gray_concrete"),
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
        'tellraw @s [{"text":"\\n=== ลิฟต์อาคารคณะวิทยาการสารสนเทศ (IF-BUU 1:1 v2.0) ===","color":"aqua","bold":true}]',
        'tellraw @s [{"text":"พิมพ์ /trigger if_floor set <เลขชั้น> หรือคลิกชั้นที่ต้องการ (แนะนำ 7F Innovation Hub!):","color":"gray"}]',
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
        (7, "7F", 32, "★ BUU Open House Innovation Hub (Vision/DMI/FabLab)"),
        (8, "8F", 37, "ห้องปฏิบัติการวิจัย / Eastern Software Park BUU"),
        (9, "9F", 42, "ห้องพักอาจารย์ IF-908A..D"),
        (10, "10F", 47, "ห้องเกียรติยศ (Hall of Fame) / ห้องประชุม"),
        (11, "11F", 52, "ห้องนิทรรศการ Exhibition Hall (IF-11M280)"),
    ]

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
            f"run tp @s ~-39 ~{tp_y} ~-1 -90 0"
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
            "description": "IF-BUU 1:1 Craft v2.0 — Faculty of Informatics BUU (Open House 2026)",
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

    # Clear area helper (chunked safely <= 32,768 blocks per /fill)
    clear_cmds = ["# Clear 1:1 building + surrounding campus context before rebuilding"]
    for y_start, y_end in [(-6, 4), (5, 15), (16, 26), (27, 37), (38, 48), (49, 59), (60, 68)]:
        for x_start, x_end in [(-100, -70), (-69, -40), (-39, -10), (-9, 20), (21, 46)]:
            for z_start, z_end in [(-58, -20), (-19, 20), (21, 60)]:
                clear_cmds.append(fill(x_start, y_start, z_start, x_end, y_end, z_end, "minecraft:air"))
    clear_cmds.append("kill @e[type=minecraft:marker,tag=if_buu_origin]")
    clear_cmds.append("kill @e[type=minecraft:text_display,tag=if_buu_label]")
    clear_cmds.append('tellraw @a {"text":"[IF-BUU 1:1 v2.0] Cleared building & campus zone.","color":"yellow"}')
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
            'tellraw @a {"text":"[IF-BUU 1:1 v2.0] Built Faculty of Informatics 1:1 + Innovation Hub + Campus Context!","color":"aqua"}',
        ],
    )

    print(f"Generated v2.0 Minecraft 1:1 Datapack -> {DP_ROOT}")
    for f in sorted(FUNC_DIR.glob("*.mcfunction")):
        line_count = len(f.read_text(encoding="utf-8").splitlines())
        print(f"  - if_buu:{f.stem} ({line_count} lines)")


if __name__ == "__main__":
    main()
