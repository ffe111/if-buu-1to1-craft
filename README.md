<div align="center">

# 🏛️ IF-BUU 1:1 Craft

**A 1:1 Scale Interactive Digital Twin of the Faculty of Informatics, Burapha University (BUU) — Built for BUU Open House & Innovation Hub 2026**

[English](README.md) | [ภาษาไทย](README.th.md)

[![Minecraft](https://img.shields.io/badge/Minecraft-1.21.11%20Java%20%26%20Bedrock-4E9A06?style=for-the-badge&logo=minecraft&logoColor=white)](https://www.minecraft.net/)
[![PaperMC](https://img.shields.io/badge/Server-PaperMC%20%2B%20GeyserMC-2B7DE9?style=for-the-badge)](https://papermc.io/)
[![BlueMap](https://img.shields.io/badge/3D%20Web%20Map-BlueMap-00B4D8?style=for-the-badge)](https://bluemap.bluecolored.io/)
[![Scale](https://img.shields.io/badge/Scale-1%3A1%20(1%20Block%20%3D%201%20Meter)-F59E0B?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0.0-7C3AED?style=for-the-badge)](#roadmap--v20-improvements)

<br/>

<img src="docs/images/v1-bluemap-preview.png" alt="IF-BUU 1:1 Craft v1.0.0 3D BlueMap Render" width="760"/>

*3D BlueMap render of **v1.0.0** — featuring the 11-storey tower, iconic curved front podium, 8F–11F step-back wing, rooftop solar arrays, and Fueang Fa Road.*

</div>

---

## 🎉 BUU Open House & Innovation Hub 2026 (`@InformaticsBUU`)

> *"Informatics – A Place Fostering Your Creative Innovations"*

This project is built as a virtual showcase companion for **BUU Open House & Innovation Hub 2026 (BUU69)**:

* 📅 **Date & Time:** **20 – 21 November 2026** | `09:00 – 16:30` (GMT+7)
* 📍 **Venues:** Thamrong Buasri Hall & **7th Floor, Faculty of Informatics Building, BUU**
* 🔬 **7th Floor Innovation Hub & Technology Showcase Highlights:**
  * **AI Vision in Action** — Live Lab Experiment *(Vision Lab)*
  * **Robot Arm Controls** *(Vision Lab)*
  * **AI / AR / VR Application Testing** *(DMI Lab)*
  * **Automation and Industry 5.0 Demo** *(DMI Lab)*
* 🌐 **Official Channels:** [informatics.buu.ac.th](https://informatics.buu.ac.th) | Facebook: *คณะวิทยาการสารสนเทศ มหาวิทยาลัยบูรพา* | YouTube: *Informatics BUU*

---

## ✨ About the Project

**IF-BUU 1:1 Craft** transforms the **11-storey Faculty of Informatics Building (Lecture Center & Administrative Office)** at **BUU (Chonburi, Thailand)** into an explorable **1:1 scale virtual campus** (`1 block = 1 meter`).

Whether visitors explore from **PC (Java Edition)**, **Mobile / iPad (Bedrock Edition)**, or directly in a **Web Browser (3D BlueMap)**, anyone can walk under the iconic curved entrance canopy, ride the working 12-level elevator from **B1 to 11F**, and visit lecture halls, computer labs, the 7th-floor Innovation Hub / FabLab, and the 11th-floor Exhibition Hall.

### 🎯 Why Build This?
* **Cross-Platform Open House Experience:** Welcomes visitors on PC, smartphones, tablets, and web browsers simultaneously.
* **Data-Driven 1:1 Accuracy:** Built using real architectural photography, 28 high-resolution 360° VR Tour panoramas, and Zoom-19 satellite measurements (`0.2906 m/px`).
* **Infrastructure-as-Blocks:** The entire 11-storey structure, staircases, elevator lobbies, and sample interiors are procedurally generated from Python into a pure vanilla **Minecraft Datapack** (`if_buu_1to1`).

---

## 📊 Verified Building Specifications

| Parameter | Real-World Data | Minecraft 1:1 Representation |
| :--- | :--- | :--- |
| **Building Name** | Faculty of Informatics, BUU (Architects 110, 2017) | `if_buu_1to1` Datapack |
| **Coordinates** | `13.281348° N, 100.924111° E` (Fueang Fa Rd.) | Origin `(0, 0, 0)` at front drop-off stairs |
| **Footprint** | ~52 m (N–S) × ~60 m (E–W incl. podium) | `52 × 60` blocks (`48 × 44` tower + `16` podium) |
| **Floors & Area** | 11 storeys + 1 basement (~18,309 sq.m. GFA) | `B1` (`Y=-5`) up to `11F` (`Y=52`) + Roof (`Y=63`) |
| **Rooftop** | 3 solar panel arrays | `minecraft:daylight_detector` arrays |

---

## 🚀 Key Features (v1.0.0)

* **Procedural 1:1 Datapack Builder (`world/datapacks/if_buu_1to1/`):**
  * **Site & Surroundings (`01_site_road`):** Fueang Fa Road, pedestrian crosswalk, brick sidewalk, wheelchair ramp, front plaza, and west motorcycle parking.
  * **11-Storey Core & Stairs (`02_basement_and_grid`, `03_slabs_and_core`):** Basement car park (`B1`), structural white-concrete grid, walkable main & fire staircases across all 12 levels, and glass-walled elevator lobbies with 4-color recycling bins.
  * **Signature Massing (`04_podium_and_arch`, `05_facade_shell`, `06_roof_and_solar`):** Sweeping C-arch front canopy with 6 slender columns & oculus skylight, 8F–11F step-back wing, 6F–8F protruding glass corner box, cobalt-blue vertical accents, and rooftop solar arrays.
  * **Representative Interiors (`07_interiors`):**
    * **1F:** Undercroft study tables, glass-walled Student Union (`SMO`), lounge sofas.
    * **2F:** Dean's Office (`IF-215`), Digital Library bookshelves, outdoor terrace.
    * **3F–6F:** 210-seat sloped Lecture Halls (`IF-3M210`, `IF-5M210`) with cyan/teal tiered seating, Computer Labs (`IF-3C01`, `IF-4C01`), and 4F Server Room.
    * **7F–10F:** Co-Working Space & FabLab / Innovation Hub zone (7F), Eastern Software Park BUU `IF-8R08` (8F), Lecturer Offices (9F), Hall of Fame & Conference Rooms (10F).
    * **11F:** Open House Exhibition Hall (`IF-11M280`) with showcase booths & fire-hose cabinets.
* **Non-OP Open House Elevator (`08_interactive_openhouse`):**
  * Works for every guest in Adventure Mode via `/trigger if_floor set <1..11>` (or `99` for `B1`) and clickable chat directory `/function if_buu:elevator_menu`.
* **Cross-Platform Open-Source Server Stack (`server/`):**
  * Powered by **PaperMC 1.21.11**, **GeyserMC + Floodgate** (Bedrock mobile/iPad support), **FastAsyncWorldEdit (FAWE)**, and **BlueMap** (3D web viewer at port `8100`).

---

## 🛠️ Quick Start

### Option A: Use the 1:1 Datapack in Any Minecraft Java World (1.21+)
1. Clone this repository:
   ```bash
   git clone https://github.com/ffe111/if-buu-1to1-craft.git
   cd if-buu-1to1-craft
   ```
2. *(Optional)* Regenerate the datapack from Python:
   ```bash
   python scripts/generate_datapack.py
   ```
3. Copy `world/datapacks/if_buu_1to1/` into your save's `datapacks/` folder, run `/reload`, stand at ground level (`Y=0`), and execute:
   ```mcfunction
   /function if_buu:build_all
   ```

### Option B: Launch the Full Cross-Platform Open House Server
1. Download **PaperMC 1.21.11**, **GeyserMC**, **Floodgate**, **BlueMap**, and **FAWE** automatically:
   ```bash
   python server/setup_server.py
   ```
2. Create `server/eula.txt` with `eula=true`.
3. Start the server (`server/start_server.bat` on Windows) and run in the server console:
   ```mcfunction
   execute positioned 0 0 0 run function if_buu:build_all
   setworldspawn 1 0 -1
   ```
4. Connect & explore:
   * **Java Edition:** `localhost:25565`
   * **Bedrock (Mobile/iPad):** `<server-ip>:19132`
   * **3D Web Browser:** `http://localhost:8100`

---

## 📁 Repository Structure

```text
if-buu-1to1-craft/
├── LICENSE                      # MIT License
├── README.md                    # English documentation (primary)
├── README.th.md                 # Thai documentation (ภาษาไทย)
├── docs/
│   ├── 01-project-plan.md       # 5-phase execution plan & progress
│   ├── 02-architectural-spec.md # Vertical scale & verified block palette
│   ├── 03-floor-directory.md    # Room inventory & VR Tour mapping (B1–11F)
│   └── images/                  # Build previews & renders
├── data/
│   ├── building_spec.json       # Machine-readable 1:1 building dimensions
│   └── osm/                     # Overpass API campus query & footprint notes
├── scripts/
│   ├── extract_vr_and_arch.py   # Extracts WPVR scene graph & asset URLs
│   ├── download_assets.py       # Downloads reference photos & 360° panoramas
│   ├── fetch_osm_footprint.py   # Queries OpenStreetMap building data
│   └── generate_datapack.py     # Procedural 1:1 Minecraft Datapack generator
├── world/datapacks/if_buu_1to1/ # Ready-to-use Minecraft 1.21+ Datapack
└── server/                      # PaperMC + GeyserMC + BlueMap setup & test suite
```

---

## 🗺️ Roadmap & v2.0 Improvements

While **v1.0.0** establishes the complete 1:1 structure, interactive elevator, and server stack, the following visual upgrades are planned for **v2.0**:
- [ ] **Refined Podium & C-Arch Geometry:** Switch dark `gray_concrete` podium cladding to lighter stone/concrete tones matching real-world daylight photos, and smooth out the sloped curved canopy ribbon.
- [ ] **Accurate Tower Facade Framing:** Add solid flanking concrete shear walls, dark horizontal window mullions, and vertical charcoal louvers on side corridors.
- [ ] **3D Faculty Signage & Surroundings:** Add `"คณะวิทยาการสารสนเทศ / FACULTY OF INFORMATICS"` via Block Display / Map Art, disable vanilla structures (`generate-structures=false`), and add neighboring buildings (Computer Center, Science CL, circular plaza).
- [ ] **Full 7th-Floor Innovation Hub & Room Partitions:** Detail the Vision Lab & DMI Lab showcases on 7F and map every room wall using on-site fire-escape floorplans (`references/floorplans/`).

---

## 🙏 Data Sources & Open-Source Credits

* **Architectural Design & Imagery:** [Architects 110 — Lecture Center & Administrative Office, Faculty of Informatics, BUU](https://www.architects110.com/project/lecture-center-administrative-office-faculty-informatics-burapha-university/)
* **Interior & Campus 360° Reference:** [Informatics 360 VR Tour — Faculty of Informatics, BUU](https://www.informatics.buu.ac.th/?page_id=6718)
* **Open-Source Ecosystem:** [PaperMC](https://papermc.io/), [GeyserMC](https://geysermc.org/), [BlueMap](https://github.com/BlueMap-Minecraft/BlueMap), [FastAsyncWorldEdit](https://github.com/IntellectualSites/FastAsyncWorldEdit)
