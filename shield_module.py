import pyautogui
import time

def shield():
    print("Activating shield...")
    
    # List of turfBoost options
    turf_boosts = ["utils/turfBoost0.png", "utils/turfBoost1.png", "utils/turfBoost2.png", "utils/turfBoost3.png",]
    for boost_img in turf_boosts:
        try:
            found = pyautogui.locateOnScreen(boost_img, confidence=0.8)
            if found:
                pyautogui.click(pyautogui.center(found))
                print(f"{boost_img} found and clicked.")
                break
        except Exception as e:
            print(f"Error locating {boost_img}: {e}")
    else:
        print("No turf boost image found.")
        return

    time.sleep(0.5)

    # Try to open shield menu
    shield_menu_found = False
    for _ in range(5):
        try:
            found = pyautogui.locateOnScreen("utils/shield1.png", confidence=0.8)
            if found:
                pyautogui.click(pyautogui.center(found))
                print("Shield menu found and clicked.")
                shield_menu_found = True
                break
                
        except Exception as e:
            print(f"Error finding shield menu: {e}")
            pyautogui.moveTo(1500, 900)
            pyautogui.dragRel(0, 450, duration=0.4)
            time.sleep(0.5)
    
    if not shield_menu_found:
        print("Failed to open shield menu.")
        return

    time.sleep(0.5)

    # Use 8hr shield
    try:
        is_8 = pyautogui.locateOnScreen("utils/eight.png", confidence=0.8)
        is_use = pyautogui.locateOnScreen("utils/use.png", confidence=0.8)
        if is_8 and is_use:
            y1 = is_8.top
            x2, y2 = pyautogui.center(is_use)
            pyautogui.click(x2, y1)
            print("8-hour shield used.")
        else:
            print("8-hour shield or use button not found.")
    except Exception as e:
        print(f"Error clicking use shield: {e}")

    time.sleep(0.5)

    # Confirm with OK
    try:
        ok_found = pyautogui.locateOnScreen("utils/ok.png", confidence=0.8)
        if ok_found:
            pyautogui.click(pyautogui.center(ok_found))
            print("OK clicked. Shield active.")
        else:
            print("OK button not found.")
    except Exception as e:
        print(f"Error confirming shield: {e}")

    time.sleep(1)
    pyautogui.press("esc")
