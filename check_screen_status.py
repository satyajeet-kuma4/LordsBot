import pyautogui
import time
import pytesseract
from shield_module import shield
from check_page import identify_page

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def army_limit_check():
    identify_page()
    hasFreeArmy = True
    # for i in range(5):
    #     try:
    #         # Check if the screenshot of the screen status is present
    #         screenshot = pyautogui.locateOnScreen("utils/screen_status.png", confidence=0.8)
    #         if screenshot:
    #             x, y = pyautogui.center(screenshot)
    #             pyautogui.click(x, y)
    #             print("Screenshot found!")
    #             break
    #     except Exception as e:
    #         pyautogui.press("esc")
    #         time.sleep(0.5)

    # time.sleep(0.5)    
    # try:
    #     check = pyautogui.locateOnScreen("utils/check_army_limit.png", confidence=0.8)
    #     if check:
    #         x, y = pyautogui.center(check)
    #         pyautogui.click(x, y)
    #         print("Check army limit found and clicked.")
    # except Exception as e:
    #     time.sleep(0.5)

    # try:
    #     checker = pyautogui.locateOnScreen("utils/checker.png", confidence=0.95)
    #     if checker:
    #         x, y = pyautogui.center(checker)
    #         pyautogui.moveTo(x, y)
    # except Exception as e:
    #     hasFreeArmy = True
    #     print("Checker not found. Waiting...")
        
    # time.sleep(0.5)
    # pyautogui.press("esc")
    try:
        checker = pyautogui.locateOnScreen("utils/c1.png", confidence=0.95)
        if checker:
            print("Checker found.")
            hasFreeArmy = False
    except Exception as e:
        print("Checker1 not found. Waiting...")
    return hasFreeArmy

def recall_troops():

    time.sleep(0.5)
    try:
        tile = pyautogui.locateOnScreen("utils/army1.png", confidence=0.8)
        if tile:
            x, y = pyautogui.center(tile)
            pyautogui.click(x, y)

            print("Tile found and clicked.")
    except Exception as e:
        print("Tile not found.")

    time.sleep(1)
    for _ in range(10):
        try:
            tile = pyautogui.locateOnScreen("utils/return_to_castle.png", confidence=0.7)
            if tile:
                x, y = pyautogui.center(tile)
                pyautogui.click(x, y)
                time.sleep(0.4)
                print("return found and clicked.")
        except Exception as e:
            print("return not found.")
            pyautogui.moveTo(1500, 900)
            pyautogui.dragRel(0, -600, duration=0.4)
            time.sleep(0.5)

def fix_alert():
    # Step 1: Take a screenshot
    try:
        army_button = pyautogui.locateOnScreen("utils/arm_b.png", confidence=0.8)
        if army_button:
            x,y = pyautogui.center(army_button)
            pyautogui.click(x, y)
            time.sleep(1.5)
            recall_button = pyautogui.locateOnScreen("utils/recall_button.png", confidence=0.8)
            if recall_button:
                x,y = pyautogui.center(recall_button)
                pyautogui.click(x, y)
                time.sleep(1)
                use_button = pyautogui.locateOnScreen("utils/u1.png", confidence=0.8)
                if use_button:
                    x,y = pyautogui.center(use_button)
                    pyautogui.click(x, y)
                    time.sleep(0.5)
                    return
    except Exception as e:
        screenshot = pyautogui.screenshot()

        # Step 2: Use OCR to read the screen
        boxes = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        # Step 3: Check for specific texts
        for i in range(len(boxes['text'])):
            text = boxes['text'][i].strip().lower()
            if "camp!" in text:
                pyautogui.press("esc")
                recall_troops()
                break

            else:
                pyautogui.press("esc")
                time.sleep(0.5)
                shield()
                break
    


def being_attacked():
    try:
        attacked = pyautogui.locateOnScreen("utils/being_attacked.png", confidence=0.6)
        if attacked:
            x, y = pyautogui.center(attacked)
            pyautogui.click(x, y)
            print("Being attacked!")
            return True  # Call the fix_alert function
    except Exception as e:
        print("checking screen status continues...")
        return False  # No action taken

    return False  # No action taken
