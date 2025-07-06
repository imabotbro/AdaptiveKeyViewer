from pynput import keyboard
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import threading
import time

class KeyDetector:
    def __init__(self):
        # Setup main window
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.transparent_color = "#123456"
        self.root.config(bg=self.transparent_color)
        self.root.wm_attributes("-transparentcolor", self.transparent_color)
        
        # Size & position: bottom center
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_width = 600
        self.window_height = 100
        self.x_position = (self.screen_width - self.window_width) // 2
        self.y_position = self.screen_height - self.window_height - 50
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Initialize text with default color
        self.text_color = "black"
        self.text_id = self.canvas.create_text(
            self.window_width // 2,
            self.window_height // 2,
            text="Key Detector Running",
            font=("Helvetica", 36, "bold"),
            fill=self.text_color
        )
        
        # Key tracking
        self.pressed_keys = set()
        
        # Common key mappings
        self.key_map = {
            keyboard.Key.ctrl_l: "Ctrl",
            keyboard.Key.ctrl_r: "Ctrl",
            keyboard.Key.alt_l: "Alt",
            keyboard.Key.alt_r: "Alt",
            keyboard.Key.shift_l: "Shift",
            keyboard.Key.shift_r: "Shift",
            keyboard.Key.cmd: "Win",
            keyboard.Key.cmd_r: "Win",
            keyboard.Key.space: "Space",
            keyboard.Key.enter: "Enter",
            keyboard.Key.backspace: "Backspace",
            keyboard.Key.tab: "Tab",
            keyboard.Key.caps_lock: "Caps",
            keyboard.Key.esc: "Esc",
            keyboard.Key.delete: "Del",
            keyboard.Key.up: "↑",
            keyboard.Key.down: "↓",
            keyboard.Key.left: "←",
            keyboard.Key.right: "→",
            keyboard.Key.f1: "F1",
            keyboard.Key.f2: "F2",
            keyboard.Key.f3: "F3",
            keyboard.Key.f4: "F4",
            keyboard.Key.f5: "F5",
            keyboard.Key.f6: "F6",
            keyboard.Key.f7: "F7",
            keyboard.Key.f8: "F8",
            keyboard.Key.f9: "F9",
            keyboard.Key.f10: "F10",
            keyboard.Key.f11: "F11",
            keyboard.Key.f12: "F12"
        }
        
        # Start background color detection thread
        self.running = True
        self.color_thread = threading.Thread(target=self.background_color_monitor)
        self.color_thread.daemon = True
        self.color_thread.start()
        
        # Start key listener
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()
        
        # Add exit mechanism (press Esc + F12 to exit)
        self.exit_combo = {keyboard.Key.esc, keyboard.Key.f12}
        self.exit_keys_pressed = set()
    
    def update_text(self):
        """Update the displayed text with current pressed keys"""
        if not self.pressed_keys:
            combo = ""
        else:
            combo = " + ".join(sorted(self.pressed_keys))
        
        self.canvas.itemconfig(self.text_id, text=combo)
    
    def on_press(self, key):
        """Handle key press events"""
        # Check for exit combination
        if key in self.exit_combo:
            self.exit_keys_pressed.add(key)
            if self.exit_keys_pressed == self.exit_combo:
                self.running = False
                self.root.quit()
                return False
        
        # Convert key to readable format
        try:
            if key in self.key_map:
                key_name = self.key_map[key]
            elif hasattr(key, 'char') and key.char:
                key_name = key.char.upper()
            else:
                key_name = str(key).replace("'", "")
        except:
            key_name = str(key).replace("'", "")
        
        # Add to pressed keys and update display
        self.pressed_keys.add(key_name)
        self.update_text()
    
    def on_release(self, key):
        """Handle key release events"""
        # Remove from exit keys if applicable
        if key in self.exit_keys_pressed:
            self.exit_keys_pressed.remove(key)
        
        # Convert key to readable format
        try:
            if key in self.key_map:
                key_name = self.key_map[key]
            elif hasattr(key, 'char') and key.char:
                key_name = key.char.upper()
            else:
                key_name = str(key).replace("'", "")
        except:
            key_name = str(key).replace("'", "")
        
        # Remove from pressed keys and update display
        if key_name in self.pressed_keys:
            self.pressed_keys.remove(key_name)
        self.update_text()
    
    def get_background_brightness(self):
        """Capture and analyze screen area under the text to determine brightness"""
        try:
            # Calculate position of text center
            text_center_x = self.x_position + self.window_width // 2
            text_center_y = self.y_position + self.window_height // 2
            
            # Capture a small area around the text
            sample_size = 20
            sample_area = (
                text_center_x - sample_size, 
                text_center_y - sample_size,
                text_center_x + sample_size, 
                text_center_y + sample_size
            )
            img = ImageGrab.grab(bbox=sample_area)
            
            # Convert to numpy array and calculate brightness
            img_array = np.array(img)
            avg_color = img_array.mean(axis=(0, 1))
            
            # Simple brightness formula
            brightness = (0.299 * avg_color[0] + 0.587 * avg_color[1] + 0.114 * avg_color[2]) / 255
            return brightness
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return 0.5  # Default to middle brightness
    
    def background_color_monitor(self):
        """Thread that monitors background color and updates text color"""
        while self.running:
            try:
                brightness = self.get_background_brightness()
                
                # Determine appropriate text color based on background brightness
                new_color = "black" if brightness > 0.5 else "white"
                
                # Update text color if needed
                if new_color != self.text_color:
                    self.text_color = new_color
                    self.canvas.itemconfig(self.text_id, fill=self.text_color)
            except Exception as e:
                print(f"Error in background monitor: {e}")
            
            # Check every 0.5 seconds
            time.sleep(0.5)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
        # Clean up
        self.running = False
        self.listener.stop()

if __name__ == "__main__":
    # Make sure you have the required packages:
    # pip install pynput pillow numpy
    detector = KeyDetector()
    detector.run()