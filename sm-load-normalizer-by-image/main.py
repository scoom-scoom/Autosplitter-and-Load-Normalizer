import time
from enum import Enum
import yaml
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

settings = read_yaml("settings.yaml")

class ImageScanType(Enum):
    SCREEN = 1
    VIDEO = 2

# scan_type = ImageScanType.SCREEN
scan_type = ImageScanType.VIDEO
crop_scale = (settings["crop_scale"]["width"], settings["crop_scale"]["height"])
if scan_type == ImageScanType.SCREEN:
    scanner = ScreenScanner(crop_scale)
elif scan_type == ImageScanType.VIDEO:
    scanner = VideoScanner(crop_scale, settings["filename_vid"], settings["fps"])

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))