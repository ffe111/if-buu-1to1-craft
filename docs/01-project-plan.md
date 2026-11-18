# แผนการดำเนินงานโปรเจกต์อาคารคณะวิทยาการสารสนเทศ 1:1 (IF-BUU in Minecraft)

## ข้อค้นพบสำคัญจากการสำรวจข้อมูล (Phase 1 Findings)
1. **OpenStreetMap (OSM) ยังไม่มีโพลิกอนของตึก IF:** จากการยิง Overpass API รอบพิกัด `13.281348, 100.924111` พบว่าแผนที่ OSM บริเวณตึก IF และสำนักคอมพิวเตอร์ยังไม่มีข้อมูลรูปทรงอาคาร (มีเฉพาะถนนและพื้นที่ข้างเคียง) ดังนั้นหากใช้ **Arnis** เพียงอย่างเดียวจะได้เฉพาะถนนและตึกฝั่งใต้ จึงต้องใช้ภาพถ่ายดาวเทียม **ESRI World Imagery (Zoom 19)** และ **Longdo Map (`A10819315`)** เป็นฐานวัดสัดส่วน 1:1 แทน
2. **แหล่งภาพและผังอ้างอิงที่ดึงเก็บเรียบร้อยแล้ว:**
   - **Architects 110 (`project_358`):** ภาพ Perspective ภายนอก 5 มุม (`5426_View-1-1.jpg`, `View-2-1.jpg`, `View-3.jpg`, `View-Cover-1.jpg`, `View-Thumb-1.jpg`) และเอกสาร PDF (`project_358.pdf`)
   - **Informatics VR Tour (`page_6718`):** ดึงภาพ Panorama 360° ความละเอียดสูงครบ 28 ฉาก (ภายนอก + ชั้น 1–11) พร้อม Scene Graph ความเชื่อมโยงของแต่ละจุด (`references/vr-tour/scene_graph.md`)

---

## แผนการดำเนินงาน 5 เฟส (5-Phase Execution Plan)

### Phase 1: เตรียมข้อมูลและสอบเทียบสเกล *(ดำเนินการเสร็จสิ้นแล้ว)*
- [x] สร้างโครงสร้างโปรเจกต์และสคริปต์ดึงข้อมูล (`extract_vr_and_arch.py`, `download_assets.py`, `fetch_osm_footprint.py`)
- [x] ดึงภาพ Perspective จาก Architects 110 และภาพ Panorama 360° ทั้งหมด 28 จุดจาก WPVR
- [x] ระบุพิกัดจริง `(13.281348, 100.924111)` และวัดขนาดฐานอาคารจริง (~52 ม. × ~60 ม.)
- [ ] **งานภาคสนามเพิ่มเติม (แนะนำ):** ถ่ายรูปป้าย *"แผนผังเส้นทางหนีไฟ"* หน้าลิฟต์ชั้น 1–11 มาเก็บใน `references/floorplans/` เพื่อใช้กั้นห้องย่อย

### Phase 2: สร้างฐานพื้นที่และโครงสร้างแกนหลัก 1:1 *(อัปเดต v2.0 เสร็จสมบูรณ์)*
- [x] สร้าง Datapack `world/datapacks/if_buu_1to1` (`01_site_road` ถึง `06_roof_and_solar`, `09_campus_context`) ครบทั้งฐานถนนเฟื้องฟ้า, ทางม้าลาย, ทางลาดผู้พิการ, เสา Grid, แกนลิฟต์-บันได, Podium เทาอ่อน + ครีบโค้ง C-Arch 5 ซี่, Step-back ชั้น 8–11, แผงโซลาร์เซลล์ และบริบทอาคารรอบข้าง (ลานน้ำพุวงกลม, ตึกฝั่งใต้, ศูนย์คอมฯ/CL ฝั่งตรงข้าม)
- [x] ปิด `generate-structures=false` ใน `server/server.properties` เพื่อลบบ้าน NPC และสร้างโลกใหม่ที่สะอาด

### Phase 3: สร้างเปลือกอาคารภายนอก (Exterior Facade) *(อัปเดต v2.0 เสร็จสมบูรณ์)*
- [x] ก่อผนังทึบ Shear Wall สีเทาอ่อนด้านข้าง, เฟรมกระจก Curtain Wall สีเทาเข้ม, กล่องกระจกยื่นชั้น 6–8, แถบสีน้ำเงิน Cobalt และแผงระแนงกันแดดแนวตั้ง
- [x] ปั้นป้ายชื่อ `"คณะวิทยาการสารสนเทศ / FACULTY OF INFORMATICS"` ด้วย `minecraft:text_display` ทั้งบนชั้น 11 และหน้า Podium พร้อมตราทอง BUU

### Phase 4: ตกแต่งภายในแบบแบ่งกลุ่มชั้น (Modular Interior) *(อัปเดต v2.0 แล้ว)*
- [x] **ชั้น 1–2:** โต๊ะนั่งอ่านหนังสือ, ห้องสโมสรนิสิต (`SMO`) ผนังกระจก, โซฟารับรอง, ห้องคณบดี (`IF-215`), ชั้นวางหนังสือห้องสมุดดิจิทัล, ระเบียงชั้น 2 และห้องน้ำใกล้แกนกลาง
- [x] **ชั้น 3–6:** ห้องบรรยายใหญ่ Slope 210 ที่นั่ง (`IF-3M210`, `IF-5M210`), ห้องแล็บคอมพิวเตอร์ (`IF-3C01`, `IF-4C01`, `IF-6T01`), ห้องเรียน (`IF-5T03`) และห้อง Server ชั้น 4
- [x] **ชั้น 7 (BUU Open House 2026 Innovation Hub):** บูธ **Vision Lab** (AI Vision in Action + Robot Arm Controls), **DMI Lab** (AI/AR/VR Testing + Industry 5.0 Demo) และโซน FabLab / Co-Working Space
- [x] **ชั้น 8–11:** Eastern Software Park BUU (`IF-8R08`), ห้องพักอาจารย์ (`IF-908A–D`), Hall of Fame & ห้องประชุม (`IF-10M56/60`) และ Exhibition Hall (`IF-11M280`) พร้อมไฟฝ้าเพดานทุกชั้น
- [ ] กั้นผนังห้องย่อยครบทุกห้องตามป้ายแผนผังหนีไฟจริง (`references/floorplans/` เมื่อเก็บภาพหน้างานเพิ่มเติม)

### Phase 5: ระบบ Interactive และเตรียมเซิร์ฟเวอร์ Open House *(ทดสอบ v2.0 ผ่าน 10/10)*
- [x] ระบบลิฟต์เลือกชั้น B1–11F (`/trigger if_floor set 1..11` และ `99` สำหรับ B1) พร้อมปุ่มทางลัดไป 7F Innovation Hub
- [x] ทดสอบรันจริงบน PaperMC 1.21.11 + GeyserMC + Floodgate + BlueMap + FAWE (`block_tests_passed=10/10, errors=0`)
