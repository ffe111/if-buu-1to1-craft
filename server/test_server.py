import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.request import urlopen

SERVER_DIR = Path(__file__).resolve().parent


def reader_thread(pipe, q: queue.Queue):
    for line in iter(pipe.readline, ""):
        q.put(line.rstrip("\r\n"))
    pipe.close()


def main():
    cmd = ["java", "-Xms1G", "-Xmx3G", "-XX:+UseG1GC", "-jar", "paper.jar", "--nogui"]
    print("Starting PaperMC 1.21.11 headless test...")
    proc = subprocess.Popen(
        cmd,
        cwd=str(SERVER_DIR),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    q: queue.Queue[str] = queue.Queue()
    t = threading.Thread(target=reader_thread, args=(proc.stdout, q), daemon=True)
    t.start()

    lines = []
    ready = False
    commands_sent = False
    bluemap_checked = False
    stop_sent = False
    start = time.time()
    ready_time = 0.0
    timeout = 120

    def send(c: str):
        print(f">>> {c}")
        proc.stdin.write(c + "\n")
        proc.stdin.flush()

    while True:
        if time.time() - start > timeout:
            print("TIMEOUT waiting for server!")
            send("stop")
            break
        try:
            s = q.get(timeout=0.5)
            lines.append(s)
            print(s)
        except queue.Empty:
            if proc.poll() is not None:
                break
            s = ""

        if not ready and "Done (" in s and "For help, type" in s:
            ready = True
            ready_time = time.time()
            print("\n=== Server Ready! Running integration checks ===")
            send("plugins")
            send("datapack list")
            send("setworldspawn 30 0 5")
            send("forceload add -64 -56 84 60")
            send("execute positioned 0 0 0 run function if_buu:build_all")
            send("execute if block 38 -1 0 minecraft:yellow_concrete")
            send("execute if block -3 65 -17 minecraft:daylight_detector")
            send("execute if block -24 30 27 minecraft:blue_concrete")
            send("execute if block 14 6 -17 minecraft:green_wool")
            send("execute if block 5 7 -16 minecraft:bookshelf")
            send("execute if block 16 13 4 minecraft:warped_stairs")
            send("execute if block -2 35 16 minecraft:lightning_rod")
            send("execute if block 12 38 -17 minecraft:quartz_slab")
            send("execute if block 0 53 -5 minecraft:red_concrete")
            send("execute if block 52 -1 14 minecraft:water")
            send("execute if entity @e[type=minecraft:text_display,tag=if_buu_label]")
            send("scoreboard objectives list")
            send("save-all")
            commands_sent = True

        if commands_sent and not bluemap_checked and ("WebServer started" in s or "Loaded!" in s or time.time() - ready_time > 15):
            bluemap_checked = True
            try:
                with urlopen("http://127.0.0.1:8100/", timeout=5) as r:
                    print(f"[HTTP CHECK] BlueMap Web UI http://127.0.0.1:8100/ -> HTTP {r.status}")
            except Exception as exc:
                print(f"[HTTP CHECK] BlueMap Web UI check: {exc}")
            send("bluemap")

        if bluemap_checked and not stop_sent and (time.time() - ready_time > 25):
            stop_sent = True
            send("save-all")
            send("stop")

    rc = proc.wait(timeout=30)
    print(f"\nServer exited with code {rc}")

    errors = [l for l in lines if "ERROR" in l]
    passed = sum(1 for l in lines if "Test passed" in l)
    print(f"Summary: block_tests_passed={passed}/11, errors={len(errors)}")
    for e in errors[:10]:
        print("  ERR:", e)
    sys.exit(0 if (rc == 0 and passed == 11 and len(errors) == 0) else 1)


if __name__ == "__main__":
    main()
