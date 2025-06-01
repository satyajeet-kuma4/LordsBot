import pyautogui
import time

# Define the page names and associated image paths
PAGE_IMAGES = {
    "home": "utils/map.png",
    "kingdom_map": "utils/return_castle.png",
    "kvk_map": "utils/kvk_map.png",
}

EXIT_CONFIRM_IMAGE = "utils/cancel_button.png"
# Define the path to the images

def get_current_page():
    for page_name, image_path in PAGE_IMAGES.items():
        print(f"Checking for {page_name} page...")
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if location:
                print(f"> You are on the {page_name} page.")
                return page_name
        except Exception as e:
            print(f"Error locating {page_name} image: {e}")
    return None

def escape_to_valid_page():
    """Presses ESC until the confirmation appears, then clicks Cancel to reset the page."""
    print("Page not identified. Escaping to a known state...")
    while True:
        pyautogui.press("esc")
        time.sleep(0.5)
        try:
            cancel_button = pyautogui.locateOnScreen(EXIT_CONFIRM_IMAGE, confidence=0.8)
            if cancel_button:
                x, y = pyautogui.center(cancel_button)
                pyautogui.click(x, y)
                print("Cancel clicked. You should now be on a known page.")
                break
        except Exception as e:
            print(f"Error locating cancel button: {e}")

        print("Still not at confirmation dialog. Pressing ESC again...")

    time.sleep(1)
    return get_current_page()


def identify_page():
    page = get_current_page()
    if page:
        return page
    else:
        return escape_to_valid_page()

