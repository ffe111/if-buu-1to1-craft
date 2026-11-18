# ข้อกำหนดทางสถาปัตยกรรมและ Block Palette (Verified from Photos)

## 1. มิติและสเกล (1 Block = 1 Meter)
* **การวางแนวอาคาร:** หันหน้าอาคารไปทาง **ทิศตะวันออก (`+X`)** ออกสู่ถนนเฟื้องฟ้า (แนะนำให้สร้างแบบ Axis-aligned ตามแกน `X/Z` ของ Minecraft เพื่อให้ห้องเรียน โต๊ะคอมพิวเตอร์ บันได และประตูตรงแนวบล็อก 100%)
* **ขนาดฐานรวม:** กว้าง (เหนือ–ใต้ / แกน `Z`) **52 บล็อก** × ลึก (ตะวันออก–ตก / แกน `X`) **60 บล็อก**
  * ส่วน Tower (ชั้น 1–11): `48 × 44` บล็อก
  * ส่วน Podium โค้งด้านหน้า (ชั้น 1–4): ยื่นออกไปทางทิศตะวันออก `+X` อีก `16` บล็อก
* **ความสูงแต่ละชั้น (Vertical Scale):**

| ชั้น | ช่วงระดับ `Y` (โดยประมาณ) | ความสูงรวม (บล็อก) | พื้นที่เดินภายใน (Clear Height) |
| :--- | :---: | :---: | :---: |
| **B1 (ลานจอดรถใต้ดิน)** | `-5` ถึง `0` | 5 | 4 บล็อก |
| **ชั้น 1 (โถงกิจกรรม / SMO)** | `0` ถึง `6` | 6 | 5 บล็อก |
| **ชั้น 2 (สำนักงาน / ห้องสมุด)** | `6` ถึง `12` | 6 | 5 บล็อก |
| **ชั้น 3 – 10 (เรียน / แล็บ / พักอาจารย์)** | `12` ถึง `52` | ชั้นละ 5 (รวม 40) | 4 บล็อกต่อชั้น |
| **ชั้น 11 (Exhibition Hall)** | `52` ถึง `59` | 7 | 6 บล็อก |
| **หลังคา, Parapet & โซลาร์เซลล์** | `59` ถึง `63` | 4 | — |

---

## 2. Block Palette (เทียบสีจากภาพ Architects 110 และ VR Tour จริง)

### ภายนอกอาคาร (Exterior)
* **โครงสร้างคานขาว / ขอบพื้นแต่ละชั้น:** `minecraft:smooth_quartz`, `minecraft:white_concrete`, `minecraft:smooth_quartz_slab`
* **ผนังคอนกรีตเทาอ่อน (Shear Wall & Podium Box):** `minecraft:light_gray_concrete`, `minecraft:polished_andesite`
* **ผนังและหลังคาส่วนบนเทาเข้ม / ป้ายชั้น 11:** `minecraft:gray_concrete`, `minecraft:polished_deepslate`, `minecraft:deepslate_tile_slab`
* **แถบสีน้ำเงินซิกเนเจอร์ (Vertical Core & Podium Accents):** `minecraft:blue_concrete`, `minecraft:lapis_block`
* **ระแนงกันแดดด้านข้าง (Charcoal Louvers/Screens):** `minecraft:blackstone_wall`, `minecraft:deepslate_brick_wall`, `minecraft:iron_bars` (หรือ `minecraft:tinted_glass`)
* **กระจก Curtain Wall:** `minecraft:light_blue_stained_glass` ผสม `minecraft:cyan_stained_glass` และกรอบ `minecraft:black_concrete`
* **หลังคาโค้งรูปตัว C หน้าอาคาร:** `minecraft:smooth_quartz_stairs` / `minecraft:light_gray_concrete` / `minecraft:iron_trapdoor` (ทำร่องซี่โค้งด้านข้าง)
* **แผงโซลาร์เซลล์บนดาดฟ้า:** `minecraft:daylight_detector` (mode=inverted สีน้ำเงินเข้ม) หรือ `minecraft:blue_glazed_terracotta`

### ภายในอาคาร (Interior — อ้างอิงจาก `1stFloor.jpg`, `11thFloor.jpg`)
* **พื้นกระเบื้องลายตารางสุ่ม (Signature Floor):** `minecraft:smooth_sandstone` / `minecraft:bone_block` (พื้นสีครีมอ่อน) แซมด้วย `minecraft:light_gray_concrete` และ `minecraft:gray_concrete` แบบสุ่ม 1×1 และ 2×2 บล็อก + บล็อกกระจก `minecraft:glass` เหนือโคมไฟ
* **ผนังภายในและเสา:** `minecraft:white_concrete` (ด้านล่างขอบบัวใช้ `minecraft:gray_concrete`)
* **ฝ้าเพดานและไฟ Downlight:** `minecraft:white_concrete` เจาะฝัง `minecraft:sea_lantern` หรือ `minecraft:pearlescent_froglight`
* **ตู้สายฉีดน้ำดับเพลิง:** `minecraft:red_concrete` + `minecraft:iron_trapdoor`

### พื้นที่รอบอาคาร (Site & Roads — อ้างอิงจาก `Front.jpg`)
* **ถนนเฟื้องฟ้า:** `minecraft:gray_concrete` / `minecraft:black_concrete` เส้นจราจร `minecraft:yellow_concrete` / `minecraft:white_concrete`
* **ทางเท้าลายอิฐแดง-เทา:** `minecraft:bricks` สลับ `minecraft:andesite`
* **ลานจอดรถ & ทางเข้า:** `minecraft:light_gray_concrete` คาดเส้นนำสายตาด้วย `minecraft:smooth_quartz`
