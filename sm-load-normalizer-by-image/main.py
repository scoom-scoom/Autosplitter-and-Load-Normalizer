import time
from enum import Enum
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

# Change these variables here according to your video.
fn_vid = "C:/Users/josho/Desktop/Big-Brother/vids/autosplitting/any-Alemussy-ryllus-and-kalidon.mp4"
fps = 30

class ImageScanType(Enum):
    SCREEN = 1
    VIDEO = 2

# scan_type = ImageScanType.SCREEN
scan_type = ImageScanType.VIDEO
if scan_type == ImageScanType.SCREEN:
    scanner = ScreenScanner()
elif scan_type == ImageScanType.VIDEO:
    scanner = VideoScanner(fn_vid, fps)

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))