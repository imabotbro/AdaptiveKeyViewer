import winreg
import ctypes

default_cursors = {
    "Arrow": "arrow",
    "Help": "help",
    "AppStarting": "wait",
    "Wait": "busy",
    "Crosshair": "cross",
    "IBeam": "ibeam",
    "NWPen": "pen",
    "No": "no",
    "SizeNS": "sizens",
    "SizeWE": "sizewe",
    "SizeNWSE": "sizenwse",
    "SizeNESW": "sizenesw",
    "SizeAll": "sizeall",
    "UpArrow": "uparrow",
    "Hand": "hand",
}

def set_default_cursor(cursor_name, default_value):
    reg_path = r"Control Panel\Cursors"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, cursor_name, 0, winreg.REG_SZ, default_value)
    except Exception as e:
        print(f"Error resetting {cursor_name}:", e)

def apply_changes():
    ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0)  # SPI_SETCURSORS

if __name__ == "__main__":
    for name, default in default_cursors.items():
        set_default_cursor(name, default)
    apply_changes()
    print("Cursors restored to Windows defaults.")
