import time
import configparser
from tracker import ActivityTracker
from uploader import S3Uploader
from utils import Utils
import threading


class Agent:
    def __init__(self):
        # Load configuration from config.ini
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Get configurable parameters from config
        self.screenshot_interval = int(self.config['settings']['screenshot_interval'])
        self.screenshot_blur = self.config.getboolean('settings', 'screenshot_blur')
        self.aws_access_key = self.config['aws']['aws_access_key']
        self.aws_secret_key = self.config['aws']['aws_secret_key']
        self.bucket_name = self.config['aws']['bucket_name']

        # Initialize activity tracker, S3 uploader, and utils
        self.tracker = ActivityTracker()
        self.uploader = S3Uploader(self.aws_access_key, self.aws_secret_key, self.bucket_name)
        self.utils = Utils()

        # Setup logging
        self.utils.setup_logging()

        # Handle Timezone Changes in the background
        self.timezone_thread = threading.Thread(target=self.utils.handle_timezone_changes)
        self.timezone_thread.daemon = True  # Run in the background
        self.timezone_thread.start()

    def start(self):
        """Main function to start the agent."""
        self.utils.log_event("Agent started. Tracking activity...")

        while True:
            # Track user activity (e.g., keystrokes, mouse movement)
            activity = self.tracker.track_activity()

            if activity:  # If genuine activity is detected
                # Take a screenshot based on the interval
                if self.screenshot_interval > 0:
                    self.utils.log_event("Taking screenshot...")
                    screenshot_path = self.tracker.take_screenshot(blur=self.screenshot_blur)
                    if screenshot_path:
                        compressed_screenshot = self.utils.compress_image(screenshot_path)
                        if compressed_screenshot:
                            self.uploader.upload_file(compressed_screenshot)

            # Sleep for the configured screenshot interval before next action
            time.sleep(self.screenshot_interval * 60)  # Convert minutes to seconds

    def stop(self):
        """Stop the agent gracefully."""
        self.utils.log_event("Agent stopped.")


if __name__ == "__main__":
    try:
        agent = Agent()
        agent.start()
    except KeyboardInterrupt:
        agent.stop()
