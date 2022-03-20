import time
from enum import Enum
import yaml
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

settings = read_yaml("settings.yaml")
# print(settings["parameters"])

crop_scale = (settings["crop_scale"]["width"], settings["crop_scale"]["height"])
scan_type = settings["image_scan_type"]
if scan_type == settings["IMAGE_SCAN_TYPE_VIDEO"]:
    scanner = VideoScanner(crop_scale, settings["vid"]["filename_vid"], settings["vid"]["fps"])
elif scan_type == settings["IMAGE_SCAN_TYPE_SCREEN"]:
    scanner = ScreenScanner(crop_scale)

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))