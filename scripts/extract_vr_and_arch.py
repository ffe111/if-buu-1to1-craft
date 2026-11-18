import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
VR_HTML = BASE_DIR / "references" / "vr-tour" / "page_6718.html"
ARCH_HTML = BASE_DIR / "references" / "architects110" / "project_358.html"


def parse_architects110():
    html = ARCH_HTML.read_text(encoding="utf-8", errors="ignore")
    urls = sorted(
        set(
            re.findall(
                r"https?://www\.architects110\.com/wp-content/uploads/2017/04/[^\"'\s<>()]+",
                html,
            )
        )
    )
    pdf_urls = sorted(
        set(
            re.findall(
                r"https?://www\.architects110\.com/property_pdf/\?id=358[^\"'\s<>()]*",
                html,
            )
        )
    )
    result = {
        "project_images": urls,
        "pdf_urls": pdf_urls,
    }
    out_file = BASE_DIR / "references" / "architects110" / "assets.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Architects110] Found {len(urls)} images, {len(pdf_urls)} PDF links -> {out_file}")
    return result


def parse_vr_tour():
    html = VR_HTML.read_text(encoding="utf-8", errors="ignore")
    normalized = html.replace("\\/", "/")
    upload_urls = sorted(
        set(
            re.findall(
                r"https?://www\.informatics\.buu\.ac\.th/wp-content/uploads/[^\"'\s<>\\]+",
                normalized,
            )
        )
    )
    vr_2021_urls = [u for u in upload_urls if "/2021/" in u or "Floor" in u or "1st" in u]

    # Try to extract pannellum / wpvr scene JSON blocks
    pannellum_matches = []
    for m in re.finditer(r"pannellum\.viewer\(", normalized):
        snippet = normalized[m.start() : m.start() + 4000]
        pannellum_matches.append(snippet[:600])

    # Extract wpvr scene definitions ("scenes": { ... })
    scenes_data = []
    for m in re.finditer(r'"scenes"\s*:\s*\{', normalized):
        brace_start = normalized.find("{", m.start())
        if brace_start != -1:
            depth = 0
            in_str = False
            esc = False
            end = None
            for idx in range(brace_start, min(len(normalized), brace_start + 300000)):
                ch = normalized[idx]
                if esc:
                    esc = False
                    continue
                if ch == "\\":
                    esc = True
                    continue
                if ch == '"':
                    in_str = not in_str
                    continue
                if not in_str:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            end = idx + 1
                            break
            if end:
                raw_json = normalized[brace_start:end]
                try:
                    parsed = json.loads(raw_json)
                    scenes_data.append({"scenes": parsed})
                except json.JSONDecodeError:
                    scenes_data.append({"raw_preview": raw_json[:1000]})

    out = {
        "total_upload_urls": len(upload_urls),
        "vr_related_urls": vr_2021_urls,
        "all_upload_urls": upload_urls,
        "scenes_blocks_found": len(scenes_data),
        "scenes_data": scenes_data,
        "pannellum_snippets": pannellum_matches[:5],
    }
    out_file = BASE_DIR / "references" / "vr-tour" / "wpvr_extracted.json"
    out_file.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[VR Tour] Found {len(vr_2021_urls)} VR-related upload URLs, {len(scenes_data)} scene blocks -> {out_file}")
    return out


if __name__ == "__main__":
    arch = parse_architects110()
    vr = parse_vr_tour()
    print("\nArchitects 110 Images:")
    for u in arch["project_images"]:
        print(" -", u)
    print("\nVR Tour 2021/Floor URLs:")
    for u in vr["vr_related_urls"]:
        print(" -", u)
