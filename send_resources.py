from pynput import keyboard
import subprocess
import os

def on_press(key):
    try:
        if key.char == 'q':
            print("You pressed Q! Launching script...")
            script_path = os.path.join(os.path.dirname(__file__), "runLords.py")
            subprocess.Popen(["python", script_path])  # or "python3" on some systems
    except AttributeError:
        pass  # This is for keys like shift, ctrl, etc.

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting listener.")
        return False  # Stops the listener

# Start listening
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
