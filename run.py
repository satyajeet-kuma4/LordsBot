import os
import pyautogui
import time
import threading
from check_page import identify_page
from shield_module import shield
from check_screen_status import being_attacked, fix_alert, army_limit_check
from detectTiles import scan_map, go_to_kingdom_map

pause_scan_event = threading.Event()  # Renamed for clarity
scan_map_thread = None
is_fix_alert_running = False


# -- Game startup --
def start_game():
    game_path = r"C:\Users\Satyajeet kumar\AppData\Roaming\IGG\Lords Mobile PC\Lords Mobile Updater.exe"
    game_started_manually = False

    try:
        lords_icon = pyautogui.locateOnScreen("utils/lords_icon.png", confidence=0.8)
        if lords_icon:
            x, y = pyautogui.center(lords_icon)
            pyautogui.click(x, y)
            print("Game icon clicked.")
        else:
            raise Exception("Game icon not found.")
    except Exception:
        os.startfile(game_path)
        print("Starting game manually...")
        game_started_manually = True
        time.sleep(15)

    if game_started_manually:
        for _ in range(10):
            try:
                cross_button = pyautogui.locateOnScreen("utils/cross_button1.png", confidence=0.70)
                if cross_button:
                    x, y = pyautogui.center(cross_button)
                    pyautogui.click(x, y)
                    time.sleep(1)
                    print("Cross button found and clicked.")
                    break
            except Exception:
                print("Cross button not found. Waiting...")
                time.sleep(3)
        
        try:
            cross_button = pyautogui.locateOnScreen("utils/cross_button1.png", confidence=0.70)
            if cross_button:
                x, y = pyautogui.center(cross_button)
                pyautogui.click(x, y)
                print("Cross button found and clicked.")
        except Exception:
            print("Cross button not found. Waiting...")

    

# -- Thread Wrappers --
def scan_map_wrapper():
    global scan_map_thread
    scan_map(pause_event=pause_scan_event)
    for _ in range(5):  # Retry up to 5 times
        try:
            cr = pyautogui.locateOnScreen("utils/gather_esc.png", confidence=0.8)
            if cr:
                x, y = pyautogui.center(cr)
                pyautogui.click(x,y)
                time.sleep(0.5)
                break
        except Exception as e:
            print("cross did not clicked")
            time.sleep(1)  # Pass the pause event
    scan_map_thread = None

def fix_alert_wrapper():
    global is_fix_alert_running  
    # Check if shield is already active
    is_fix_alert_running = True 
    print("[⚠️] No shield detected. Executing fix_alert routine.")

    pause_scan_event.set()  # Pause map scanning
    fix_alert()
    pause_scan_event.clear()  # Resume map scanning

    is_fix_alert_running = False



# -- Monitor Loop --
def monitor_game():
    global scan_map_thread, is_fix_alert_running

    print("🔍 Starting Lords Mobile monitor...")

    while True:
        # PRIORITY: Being Attacked
        # try:
        #     c11 = pyautogui.locateOnScreen("utils/exit_0.png", confidence=0.8)
        #     if c11:
        #         time.sleep(2)
        #         print("nothing to do..")
        # except Exception:
        #     try:
        #         cross = pyautogui.locateOnScreen("utils/exit_1.png", confidence=0.8)
        #         if cross:
        #             x,y = pyautogui.center(cross)
        #             pyautogui.click(x,y)
        #             time.sleep(0.5)
        #     except Exception:
        #         time.sleep(0.5)
        #         pass
        # try:
        #     is_shield_active = pyautogui.locateOnScreen("utils/turfBoost0.png", confidence=0.8)
        #     if is_shield_active:
        #         print("Shield is active.")  
        # except Exception:
        #     print("No shield.")
        #     shield()
        #     continue
        if not is_fix_alert_running and being_attacked():
            threading.Thread(target=fix_alert_wrapper).start()

        # Only scan if not being attacked or paused
        if not is_fix_alert_running and not pause_scan_event.is_set():
            if scan_map_thread is None or not scan_map_thread.is_alive():
                if army_limit_check():
                    scan_map_thread = threading.Thread(target=scan_map_wrapper)
                    scan_map_thread.start()

        time.sleep(2)

# -- Main --
if __name__ == "__main__":
    start_game()
    monitor_game()
