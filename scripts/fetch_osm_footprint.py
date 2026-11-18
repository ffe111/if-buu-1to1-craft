import json
import math
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
OSM_DIR = BASE_DIR / "data" / "osm"

# Bounding box around Burapha University Faculty of Informatics (Bangsaen, Chonburi)
# Lat: 13.278 to 13.286, Lon: 100.919 to 100.928
BBOX = (13.2775, 100.9190, 13.2865, 100.9285)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def latlon_to_local_xz(lat: float, lon: float, origin_lat: float, origin_lon: float) -> tuple[float, float]:
    # In Minecraft: +X is East, +Z is South
    meters_per_deg_lat = 111132.92 - 559.82 * math.cos(2 * math.radians(origin_lat))
    meters_per_deg_lon = 111412.84 * math.cos(math.radians(origin_lat))
    dx = (lon - origin_lon) * meters_per_deg_lon
    dz = (origin_lat - lat) * meters_per_deg_lat
    return dx, dz


def fetch_overpass() -> dict:
    OSM_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = OSM_DIR / "buu_campus_raw.json"
    query = f"""
    [out:json][timeout:30];
    (
      way["building"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      relation["building"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      way["highway"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
      node["name"~"สารสนเทศ|Informatics|คอมพิวเตอร์",i]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});
    );
    out body;
    >;
    out skel qt;
    """
    data = urlencode({"data": query}).encode("utf-8")
    req = Request(OVERPASS_URL, data=data, headers={"User-Agent": "BUU-Openhouse-Minecraft/1.0"})
    with urlopen(req, timeout=45) as resp:
        raw = resp.read().decode("utf-8")
    raw_path.write_text(raw, encoding="utf-8")
    return json.loads(raw)


def analyze_buildings(osm_data: dict):
    nodes = {}
    ways = []
    named_nodes = []
    for el in osm_data.get("elements", []):
        if el["type"] == "node":
            nodes[el["id"]] = (el["lat"], el["lon"])
            if "tags" in el and "name" in el["tags"]:
                named_nodes.append(el)
        elif el["type"] == "way" and "tags" in el and "building" in el["tags"]:
            ways.append(el)

    buildings = []
    for w in ways:
        tags = w.get("tags", {})
        name = tags.get("name") or tags.get("name:th") or tags.get("name:en") or ""
        pts = [nodes[nid] for nid in w.get("nodes", []) if nid in nodes]
        if len(pts) < 3:
            continue
        centroid_lat = sum(p[0] for p in pts[:-1]) / max(1, len(pts) - 1)
        centroid_lon = sum(p[1] for p in pts[:-1]) / max(1, len(pts) - 1)

        local_pts = [latlon_to_local_xz(p[0], p[1], centroid_lat, centroid_lon) for p in pts]
        edge_lengths = []
        for i in range(len(local_pts) - 1):
            x1, z1 = local_pts[i]
            x2, z2 = local_pts[i + 1]
            edge_lengths.append(round(math.hypot(x2 - x1, z2 - z1), 2))

        xs = [p[0] for p in local_pts]
        zs = [p[1] for p in local_pts]
        width_ew = round(max(xs) - min(xs), 2)
        depth_ns = round(max(zs) - min(zs), 2)

        # Shoelace area in m^2
        area = 0.0
        for i in range(len(local_pts) - 1):
            x1, z1 = local_pts[i]
            x2, z2 = local_pts[i + 1]
            area += x1 * z2 - x2 * z1
        area = round(abs(area) / 2.0, 2)

        buildings.append(
            {
                "osm_id": w["id"],
                "name": name,
                "tags": tags,
                "centroid": {"lat": round(centroid_lat, 7), "lon": round(centroid_lon, 7)},
                "bbox_meters": {"east_west_x": width_ew, "north_south_z": depth_ns},
                "footprint_area_sqm": area,
                "edge_lengths_m": edge_lengths,
                "local_xz_blocks": [[round(x, 2), round(z, 2)] for x, z in local_pts],
                "latlon_points": [[round(p[0], 7), round(p[1], 7)] for p in pts],
            }
        )

    # Sort or highlight Informatics-related buildings
    keywords = ["สารสนเทศ", "informatics", "if", "คอมพิวเตอร์", "วิทยาศาสตร์", "cl"]
    highlighted = []
    for b in buildings:
        n_low = (b["name"] + " " + json.dumps(b["tags"], ensure_ascii=False)).lower()
        if any(k in n_low for k in keywords):
            highlighted.append(b)

    summary = {
        "total_buildings_in_bbox": len(buildings),
        "named_nodes": named_nodes,
        "highlighted_buildings": highlighted,
        "all_named_buildings": [
            {
                "osm_id": b["osm_id"],
                "name": b["name"],
                "centroid": b["centroid"],
                "bbox_meters": b["bbox_meters"],
                "footprint_area_sqm": b["footprint_area_sqm"],
            }
            for b in buildings
            if b["name"]
        ],
    }

    out_path = OSM_DIR / "buildings_analysis.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Found {len(buildings)} buildings in bbox, {len(highlighted)} matched keywords.")
    print(f"Saved analysis -> {out_path}")
    for b in highlighted:
        print(
            f"  * [{b['osm_id']}] {b['name'] or '(unnamed)'} | "
            f"center=({b['centroid']['lat']}, {b['centroid']['lon']}) | "
            f"size={b['bbox_meters']['east_west_x']}m x {b['bbox_meters']['north_south_z']}m | "
            f"area={b['footprint_area_sqm']} sqm | edges={b['edge_lengths_m']}"
        )
    if named_nodes:
        print("Named POIs:")
        for nd in named_nodes:
            print(f"  - {nd['tags'].get('name')} @ ({nd['lat']}, {nd['lon']})")


if __name__ == "__main__":
    osm_data = fetch_overpass()
    analyze_buildings(osm_data)
