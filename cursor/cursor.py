import winreg
import ctypes
import os

# Path to your custom cursor
cursor_path = r"./car_cursor.cur"

# Which system cursor to change (e.g., "Arrow", "Hand", "Wait", etc.)
cursor_type = "Arrow"

def set_cursor(cursor_name, cursor_file):
    reg_path = r"Control Panel\Cursors"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, cursor_name, 0, winreg.REG_SZ, cursor_file)
        print(f"Cursor for '{cursor_name}' set to '{cursor_file}'")
    except Exception as e:
        print("Failed to set cursor:", e)

# Apply changes
def apply_cursor_change():
    ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0)  # SPI_SETCURSORS
    print("Cursor changes applied.")

if __name__ == "__main__":
    if os.path.exists(cursor_path):
        set_cursor(cursor_type, cursor_path)
        apply_cursor_change()
    else:
        print("Cursor file not found.")
