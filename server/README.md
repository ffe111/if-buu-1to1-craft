# เซิร์ฟเวอร์ Open House (PaperMC + GeyserMC + BlueMap + FAWE)

ชุดไฟล์สำหรับรันเซิร์ฟเวอร์ Minecraft แบบ Cross-Platform (เข้าได้ทั้ง PC Java Edition, มือถือ/iPad Bedrock Edition และดูโมเดล 3D ผ่านเว็บเบราว์เซอร์ด้วย BlueMap)

## วิธีติดตั้งและเปิดเซิร์ฟเวอร์
1. **ติดตั้งไฟล์เซิร์ฟเวอร์และปลั๊กอินอัตโนมัติ** (ใช้ Python ดาวน์โหลด PaperMC 1.21.11, GeyserMC, Floodgate, BlueMap และ FastAsyncWorldEdit พร้อมซิงก์ Datapack 1:1):
   ```bash
   python setup_server.py
   ```
2. **ยอมรับ Minecraft EULA:**
   สร้างไฟล์ `server/eula.txt` แล้วใส่ข้อความ:
   ```text
   eula=true
   ```
3. **เปิดเซิร์ฟเวอร์:**
   รันไฟล์ `start_server.bat` (เครื่องมี Java 26 พร้อมใช้งานแล้ว)
4. **สร้างอาคารคณะ 1:1 ลงในโลกเซิร์ฟเวอร์:**
   พิมพ์คำสั่งนี้ในหน้าต่าง Console ของเซิร์ฟเวอร์ (เพื่อสร้างที่พิกัด `X=0, Y=0, Z=0` บนโลก Flat):
   ```mcfunction
   execute positioned 0 0 0 run function if_buu:build_all
   setworldspawn 1 0 -1
   ```
5. **ตั้งค่าเพิ่มเติมหลังรันครั้งแรก:**
   - **BlueMap (ดูตึก 3D บนเว็บ):** เปิดเบราว์เซอร์ไปที่ `http://localhost:8100` (หาก BlueMap แจ้งให้ยอมรับ `accept-download: true` ใน `plugins/BlueMap/core.conf` ให้แก้เป็น `true` แล้วพิมพ์ `bluemap reload`)
   - **GeyserMC (เข้าจากมือถือ/iPad):** พอร์ตเริ่มต้น `19132/UDP` (สามารถให้ผู้ร่วมงาน Open House ใช้ชื่อเล่นเข้าได้โดยไม่ต้องมีไอดีแท้เมื่อเปิดคู่กับ Floodgate)
   - **ลิฟต์สำหรับผู้เยี่ยมชม (ไม่ต้องมีสิทธิ์ OP):** ผู้เล่นทุกคนสามารถพิมพ์ `/trigger if_floor set 1` ถึง `11` (หรือ `99` สำหรับชั้นใต้ดิน B1) หรือให้แอดมินรัน `/execute as @a run function if_buu:elevator_menu` เพื่อส่งเมนูลิฟต์ให้ผู้ชมกดเลือกชั้นได้ทันที
