import time
from enum import Enum
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

# fn_vid = "C:/Users/josho/Desktop/Big-Brother/vids/autosplitting/any-Alemussy.mp4"
fn_vid = "C:/Users/josho/Desktop/Big-Brother/vids/autosplitting/any-Alemussy-ryllus-and-kalidon.mp4"
fps = 30

# The parameter crop_scale determines how large the cropped image in the centre should be.
# If it's too small, there is a chance that images with some black in the middle
# will be falsely counted as a black screen. If it is too large, there is a chance
# that the cropped image also includes pixels outside of the game video (e.g.
# twitch layout), which would most likely not be black.

# crop_scale_width = 1
# crop_scale_height = 1
crop_scale_width = 3
crop_scale_height = 3
crop_scale = (crop_scale_width, crop_scale_height)

class ImageScanType(Enum):
    SCREEN = 1
    VIDEO = 2

# scan_type = ImageScanType.SCREEN
scan_type = ImageScanType.VIDEO
if scan_type == ImageScanType.SCREEN:
    scanner = ScreenScanner(crop_scale)
elif scan_type == ImageScanType.VIDEO:
    scanner = VideoScanner(crop_scale, fn_vid, fps)

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))