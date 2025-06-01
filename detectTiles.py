import pyautogui
import cv2
import numpy as np
import time
import os
import torch
from ultralytics import YOLO
import pytesseract
from check_page import identify_page
from state import seen_coords  # Shared global list

# Load YOLOv8 model for resource detection
model = YOLO("runs/detect/train/weights/best.pt")  # Replace with your model path

# Global flag to track if a resource has been found
found_resources = False  

# Region where coordinate text appears (left, top, width, height)
coord_region = (1131, 1014, 301, 49)
search_region = (0, 130, 2559, 1309)  # Full screen
def go_to_kingdom_map():
    currenPage = identify_page()
    if currenPage == "kingdom_map":
        pass
    else:
        try:
            map_icon = pyautogui.locateOnScreen("utils/map.png", confidence=0.8)
            if map_icon:
                x, y = pyautogui.center(map_icon)
                pyautogui.click(x, y)
                print("Map icon found and clicked.")
        except pyautogui.ImageNotFoundException:
            print("Map icon not found. Please check the image path or the game state.")

def capture_screen():
    screenshot = pyautogui.screenshot(region=search_region)
    frame = np.array(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def read_coordinates_text():
    screenshot = pyautogui.screenshot(region=coord_region)
    gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray)
    cleaned = text.strip().replace("\n", " ")
    return cleaned

def detect_resources(frame, target_class="gold"):
    global found_resources
    results = model(frame)

    best_detection = None
    highest_conf = 0

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls)
            cls_name = result.names[cls_id]
            conf = box.conf.item()
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if cls_name == target_class and conf > highest_conf:
                highest_conf = conf
                best_detection = (cls_name, conf, (x1, y1, x2, y2))

    if best_detection and highest_conf >= 0.7:
        x1, y1, x2, y2 = best_detection[2]
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        center_y += 130
        pyautogui.click(center_x, center_y)
        found_resources = True
        print(f"{target_class.capitalize()} found at ({center_x}, {center_y}) with confidence {highest_conf:.3f}")

        time.sleep(1.5)  # Wait for coordinate text to appear
        coord_text = read_coordinates_text()

        if coord_text in seen_coords:
            print(f"Already sent troops to {coord_text}. Skipping...")
            pyautogui.press('esc')
            return False
        else:
            seen_coords.append(coord_text)
            print(f"New tile detected at {coord_text}. Adding to seen list.")
            return True
    else:
        print(f"No {target_class} detected.")
        return False

def deploy(): 
    time.sleep(0.5)
    buttons = ["gather.png", "g1.png", "g2.png", "deploy.png"]
    for button in buttons:
        try:
            button_path = os.path.join("utils", button)
            btn = pyautogui.locateOnScreen(button_path, confidence=0.8)
            if btn:
                x, y = pyautogui.center(btn)
                pyautogui.click(x, y)
                time.sleep(0.5)
        except pyautogui.ImageNotFoundException:
            pyautogui.moveTo(1500, 200)
            pyautogui.dragRel(-200, 200, duration=0.3)
            break
            print(f"{button} not found.")

def scan_map(target_class="gold", pause_event=None):
    for _ in range(3):
        try:
            c111 = pyautogui.locateOnScreen("utils/exit_1.png", confidence=0.8)
            if c111:
                x,y = pyautogui.center(c111)
                pyautogui.click(x,y)
                break
        except Exception:
            time.sleep(0.5)
            pass
    global found_resources
    found_resources = False  # Reset at the start
    go_to_kingdom_map()

    frame = capture_screen()
    if detect_resources(frame, target_class=target_class):
        deploy()
        return 

    count = 0
    c1 = 0
    max_attempts = 20

    while count < max_attempts and not found_resources:
        if pause_event and pause_event.is_set():
            print("🔴 Scan paused due to attack detected.")
            return

        print(f"--- Scan iteration {count + 1} ---")

        for i in range(1 + c1):
            if pause_event and pause_event.is_set():
                return
            pyautogui.moveTo(1500, 500)
            pyautogui.dragRel(0, 500, duration=0.3)
            time.sleep(0.8)
            frame = capture_screen()
            if detect_resources(frame, target_class=target_class):
                deploy()
                return  # detection already handles deploy or skip

        for i in range(1 + c1):
            if pause_event and pause_event.is_set():
                return
            pyautogui.moveTo(600, 600)
            pyautogui.dragRel(500, 0, duration=0.3)
            time.sleep(0.8)
            frame = capture_screen()
            if detect_resources(frame, target_class=target_class):
                deploy()
                return

        c1 += 1

        for i in range(1 + c1):
            if pause_event and pause_event.is_set():
                return
            pyautogui.moveTo(400, 1300)
            pyautogui.dragRel(0, -500, duration=0.3)
            time.sleep(0.8)
            frame = capture_screen()
            if detect_resources(frame, target_class=target_class):
                deploy()
                return

        for i in range(1 + c1):
            if pause_event and pause_event.is_set():
                return
            pyautogui.moveTo(1700, 1000)
            pyautogui.dragRel(-500, 0, duration=0.3)
            time.sleep(0.8)
            frame = capture_screen()
            if detect_resources(frame, target_class=target_class):
                deploy()
                return

        c1 += 1
        count += 1

    print("Scan complete.")