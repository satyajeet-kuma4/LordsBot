import tkinter as tk
import threading
import os
import sys

import pyautogui

# Make sure this script knows where to find your modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)


def click_lords_icon():
    try:
        lords_icon = pyautogui.locateOnScreen(os.path.join("utils", "lords_icon.png"), confidence=0.8)
        if lords_icon:
            x, y = pyautogui.center(lords_icon)
            pyautogui.click(x, y)
            print("Lords icon found and clicked.")
    except pyautogui.ImageNotFoundException:
        print("Lords icon not found. Please check the image path or the game state.")
# Import your functions from local bot files
from detectTiles import scan_map
from shield_module import shield as apply_shield

# Wrap threaded bot tasks
def start_gathering():
    click_lords_icon()
    print("Starting gathering task...")
    threading.Thread(target=scan_map).start()

def start_shielding():
    click_lords_icon()
    print("Starting shield task...")
    threading.Thread(target=apply_shield).start()

# Exit
def close_bot():
    click_lords_icon()
    print("Bot control window closed.")
    root.destroy()

# Floating always-on-top window
root = tk.Tk()
root.title("LordsBot Control")
root.geometry("200x150+100+100")
root.attributes("-topmost", True)
root.overrideredirect(True)

# Drag functions
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

frame = tk.Frame(root, bg="#222", bd=2)
frame.pack(expand=True, fill="both")
frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)

# Buttons
tk.Button(frame, text="Gather", command=start_gathering, bg="green", fg="white").pack(padx=10, pady=5, fill="x")
tk.Button(frame, text="Apply Shield", command=start_shielding, bg="blue", fg="white").pack(padx=10, pady=5, fill="x")
tk.Button(frame, text="Exit", command=close_bot, bg="red", fg="white").pack(padx=10, pady=5, fill="x")



root.mainloop()
