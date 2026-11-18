import json
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
ARCH_JSON = BASE_DIR / "references" / "architects110" / "assets.json"
VR_JSON = BASE_DIR / "references" / "vr-tour" / "wpvr_extracted.json"

ARCH_IMG_DIR = BASE_DIR / "references" / "architects110" / "images"
VR_IMG_DIR = BASE_DIR / "references" / "vr-tour" / "images"


def download_file(url: str, dest: Path) -> tuple[bool, str]:
    if dest.exists() and dest.stat().st_size > 0:
        return True, "already exists"
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; BUU-Openhouse-Minecraft/1.0)"})
    try:
        with urlopen(req, timeout=30) as resp:
            content = resp.read()
            dest.write_bytes(content)
            return True, f"{len(content)} bytes"
    except (HTTPError, URLError, TimeoutError) as exc:
        return False, str(exc)


def export_scene_graph(vr_data: dict) -> list[str]:
    pano_urls: set[str] = set()
    lines = ["# Informatics VR Tour - Extracted Scene Graph\n"]
    seen_scenes: set[str] = set()

    for idx, blk in enumerate(vr_data.get("scenes_data", [])):
        scenes = blk.get("scenes")
        if not isinstance(scenes, dict):
            continue
        lines.append(f"## Tour Block {idx + 1}\n")
        for scene_id, scene in scenes.items():
            pano = scene.get("panorama", "")
            if pano:
                pano_urls.add(pano)
            title = scene.get("title") or "(no title)"
            hotspots = scene.get("hotSpots", [])
            key = f"{scene_id}|{pano}"
            marker = " *(duplicate)*" if key in seen_scenes else ""
            seen_scenes.add(key)
            lines.append(f"- **Scene `{scene_id}`**{marker}: `{pano.split('/')[-1] if pano else 'N/A'}` (title: {title})")
            for hs in hotspots:
                hs_type = hs.get("type", "")
                hs_text = hs.get("text", "").replace("\n", " ").strip()
                target = hs.get("sceneId", "")
                yaw = hs.get("yaw", "")
                pitch = hs.get("pitch", "")
                if target:
                    lines.append(f"  - -> `{target}` (yaw={yaw}, pitch={pitch}) {hs_text}")
                elif hs_text:
                    lines.append(f"  - [{hs_type}] (yaw={yaw}, pitch={pitch}) {hs_text}")
        lines.append("")

    md_path = BASE_DIR / "references" / "vr-tour" / "scene_graph.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[VR Tour] Exported scene graph -> {md_path}")
    return sorted(pano_urls)


def main():
    arch = json.loads(ARCH_JSON.read_text(encoding="utf-8"))
    vr = json.loads(VR_JSON.read_text(encoding="utf-8"))

    pano_urls = export_scene_graph(vr)

    print("\n=== Downloading Architects 110 Images & PDF ===")
    for url in arch.get("project_images", []):
        name = url.split("/")[-1]
        ok, msg = download_file(url, ARCH_IMG_DIR / name)
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: {msg}")

    for url in arch.get("pdf_urls", []):
        if "download=1" in url:
            ok, msg = download_file(url, BASE_DIR / "references" / "architects110" / "project_358.pdf")
            print(f"  [{'OK' if ok else 'FAIL'}] project_358.pdf: {msg}")

    # Combine pano_urls from scenes + vr_related_urls (.jpg files)
    vr_jpgs = sorted(
        set(pano_urls)
        | {u for u in vr.get("vr_related_urls", []) if u.lower().endswith((".jpg", ".jpeg", ".png"))}
    )
    print(f"\n=== Downloading Informatics VR Tour Assets ({len(vr_jpgs)} files) ===")
    for url in vr_jpgs:
        name = url.split("/")[-1]
        ok, msg = download_file(url, VR_IMG_DIR / name)
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: {msg}")


if __name__ == "__main__":
    main()
