import os
import time
from datetime import datetime
import pyautogui
import psutil
from pynput import mouse, keyboard
from PIL import Image, ImageFilter

class ActivityTracker:
    def __init__(self):
        self.last_activity_time = time.time()
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        # Start the listeners for activity tracking
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_move(self, x, y):
        """Mouse movement event handler"""
        self.last_activity_time = time.time()

    def on_click(self, x, y, button, pressed):
        """Mouse click event handler"""
        self.last_activity_time = time.time()

    def on_press(self, key):
        """Keyboard press event handler"""
        self.last_activity_time = time.time()

    def track_activity(self):
        """Returns True if genuine user activity is detected"""
        current_time = time.time()
        # If there was any activity in the last minute, return True
        if current_time - self.last_activity_time < 60:
            return True
        return False

    def take_screenshot(self, blur=False):
        """Capture a screenshot and save it to a file, optionally apply a blur effect"""
        try:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            screenshot_path = f'screenshots/screenshot_{timestamp}.png'

            # Ensure the screenshot folder exists
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')

            # Apply blur if required
            if blur:
                screenshot = screenshot.convert('RGB')  # Convert to an editable image format
                screenshot = screenshot.filter(ImageFilter.GaussianBlur(10))

            # Save the screenshot
            screenshot.save(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None

    def detect_irregular_activity(self):
        """Placeholder for detecting irregular or scripted activity like unnatural mouse movement"""
        # Logic to detect irregular mouse movement patterns or script-based automation
        # Example: detecting sudden jumps in mouse positions or repeating keystroke patterns
        pass
