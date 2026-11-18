function if_buu:elevator_menu
tellraw @s [{"text":"[หน้าตึก] ","color":"green","bold":true,"click_event":{"action":"run_command","command":"/trigger if_floor set 1"},"clickEvent":{"action":"run_command","command":"/trigger if_floor set 1"}},{"text":"ใช้คำสั่ง /function if_buu:elevator_menu เพื่อเปิดเมนูลิฟต์ได้ตลอดเวลา","color":"gray"}]
