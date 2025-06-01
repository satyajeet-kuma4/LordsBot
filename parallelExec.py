import threading
import time
from check_screen_status import being_attacked, fix_alert, army_limit_check
from detectTiles import scan_map

# Control flags to prevent multiple threads
is_fix_alert_running = False
is_scan_map_running = False

def monitor_game():
    global is_fix_alert_running, is_scan_map_running

    print("🔍 Starting Lords Mobile monitor...")
    while True:
        # Check for attack
        if being_attacked() and not is_fix_alert_running:
            is_fix_alert_running = True
            threading.Thread(target=fix_alert_wrapper).start()

        # Check for army availability
        if army_limit_check() and not is_scan_map_running:
            is_scan_map_running = True
            threading.Thread(target=scan_map_wrapper).start()

        time.sleep(2)  # Adjust for performance or frequency

def fix_alert_wrapper():
    global is_fix_alert_running
    try:
        fix_alert()
    finally:
        is_fix_alert_running = False

def scan_map_wrapper():
    global is_scan_map_running
    try:
        print("🧭 Starting map scan...")
        scan_map()
    finally:
        is_scan_map_running = False

if __name__ == "__main__":
    monitor_game()
