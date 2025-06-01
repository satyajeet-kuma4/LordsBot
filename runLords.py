import os
import pyautogui
import time
import psutil
from shield_module import shield
from check_page import identify_page
from detectTiles import scan_map
from send_resources import read_screen

game_path = r"C:\Users\Satyajeet kumar\AppData\Roaming\IGG\Lords Mobile PC\Lords Mobile Updater.exe"
confirm_button_path = os.path.join("utils", "cancel_button.png")

def is_game_running(process_name="Lords Mobile PC.exe"):
    for process in psutil.process_iter(attrs=["name"]):
        if process.info["name"] == process_name:
            return True
    return False

if not is_game_running():
    print("Lords Mobile is not running. Starting it now...")
    os.startfile(game_path)
    time.sleep(15)
else:
    print("Lords Mobile is already running. Skipping startup.")

try:
    lords_icon = pyautogui.locateOnScreen(os.path.join("utils", "lords_icon.png"), confidence=0.8)
    if lords_icon:
        x, y = pyautogui.center(lords_icon)
        pyautogui.click(x, y)
        print("Lords icon found and clicked.")
except Exception as e:
    print(f"Error locating Lords icon: {e}")

time.sleep(3)

try:
    max_attempts = 20
    attempts = 0
    while attempts < max_attempts:
        pyautogui.press("esc")
        time.sleep(0.5)
        cancel_button = pyautogui.locateOnScreen(confirm_button_path, confidence=0.8)
        if cancel_button:
            x, y = pyautogui.center(cancel_button)
            pyautogui.click(x, y)
            print("Cancel button found and clicked.")
            break
        else:
            print("Cancel button not found. Waiting...")
        attempts += 1

except KeyboardInterrupt:
    print("Script interrupted by user with Ctrl+C.")
except Exception as e:
    print(f"An error occurred: {e}")

# current_page = identify_page()
# print(f"Current page: {current_page}")
# scan_map()
read_screen("Ganjeri2")