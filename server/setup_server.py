"""
Download PaperMC + Open-Source Open House Plugins (GeyserMC, Floodgate, BlueMap, FAWE)
and sync the 1:1 Faculty of Informatics Datapack into server/world/datapacks/.
"""

import argparse
import json
import shutil
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

SERVER_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SERVER_DIR.parent
DATAPACK_SRC = PROJECT_DIR / "world" / "datapacks" / "if_buu_1to1"
PLUGINS_DIR = SERVER_DIR / "plugins"
DATAPACK_DST = SERVER_DIR / "world" / "datapacks" / "if_buu_1to1"

UA = "BUU-Openhouse-Minecraft/1.0"


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=120) as resp:
        data = resp.read()
    dest.write_bytes(data)
    print(f"  [OK] {dest.name} ({len(data) / (1024 * 1024):.2f} MB)")


def get_paper_url(mc_version: str) -> tuple[str, str]:
    builds = fetch_json(f"https://fill.papermc.io/v3/projects/paper/versions/{mc_version}/builds")
    stable = [b for b in builds if b.get("channel") == "STABLE"] or builds
    latest = stable[0]
    dl = latest["downloads"]["server:default"]
    return dl["url"], dl["name"]


def get_modrinth_plugin(slug: str, mc_version: str) -> tuple[str, str] | None:
    loaders = quote('["paper","spigot","bukkit"]')
    versions = fetch_json(f"https://api.modrinth.com/v2/project/{slug}/version?loaders={loaders}")
    for v in versions:
        if mc_version in v.get("game_versions", []):
            f = v["files"][0]
            return f["url"], f["filename"]
    # Fallback to latest paper build if exact game_version tag isn't listed
    if versions:
        f = versions[0]["files"][0]
        return f["url"], f["filename"]
    return None


def main():
    parser = argparse.ArgumentParser(description="Setup PaperMC + GeyserMC + BlueMap + FAWE server")
    parser.add_argument("--mc-version", default="1.21.11", help="Minecraft Paper version (default: 1.21.11)")
    args = parser.parse_args()
    mc_ver = args.mc_version

    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"1. Fetching PaperMC {mc_ver} from Fill v3 API...")
    paper_url, paper_name = get_paper_url(mc_ver)
    download_file(paper_url, SERVER_DIR / "paper.jar")
    print(f"   (Downloaded {paper_name})")

    print("2. Fetching Open-Source Plugins...")
    download_file(
        "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
        PLUGINS_DIR / "Geyser-Spigot.jar",
    )
    download_file(
        "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot",
        PLUGINS_DIR / "floodgate-spigot.jar",
    )

    for slug in ("bluemap", "fastasyncworldedit"):
        res = get_modrinth_plugin(slug, mc_ver)
        if res:
            url, fname = res
            download_file(url, PLUGINS_DIR / fname)
        else:
            print(f"  [WARN] Could not find Modrinth release for {slug}")

    print("3. Syncing 1:1 Datapack -> server/world/datapacks/if_buu_1to1 ...")
    if DATAPACK_SRC.exists():
        if DATAPACK_DST.exists():
            shutil.rmtree(DATAPACK_DST)
        DATAPACK_DST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(DATAPACK_SRC, DATAPACK_DST)
        print("  [OK] Datapack synced.")
    else:
        print("  [WARN] Datapack not found. Run scripts/generate_datapack.py first.")

    print("\nSetup complete! Next steps:")
    print("  1) Accept the Minecraft EULA by creating server/eula.txt with: eula=true")
    print("  2) Run start_server.bat")
    print("  3) In server console, run: execute positioned 0 0 0 run function if_buu:build_all")
    print("  4) Open BlueMap 3D Web Viewer at http://localhost:8100")


if __name__ == "__main__":
    main()
