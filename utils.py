import os
import logging
import pytz
from datetime import datetime
from PIL import Image
import zipfile

class Utils:
    def setup_logging(self):
        logging.basicConfig(filename='agent.log', level=logging.INFO)

    def log_event(self, message):
        logging.info(f"{datetime.now()}: {message}")

    def handle_timezone_changes(self):
        # Logic to detect and handle timezone changes
        pass

    def compress_image(self, image_path):
        """Compress the image using PIL."""
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")  # Ensure it's in RGB mode
                compressed_path = f"compressed_{os.path.basename(image_path)}"
                img.save(compressed_path, "JPEG", optimize=True, quality=50)
                return compressed_path
        except Exception as e:
            self.log_event(f"Error compressing image: {e}")
            return None

    def compress_file(self, file_path):
        """Compress files into a zip file."""
        zip_file = f"{file_path}.zip"
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.write(file_path, arcname=os.path.basename(file_path))
        return zip_file
