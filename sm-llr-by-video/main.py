import time
from enum import Enum
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

fn_vid = "C:/Users/josho/Desktop/Big-Brother/vids/autosplitting/llr-test-7th-pb.mp4"
class ImageScanType(Enum):
    SCREEN = 1
    VIDEO = 2

# scan_type = ImageScanType.SCREEN
scan_type = ImageScanType.VIDEO
if scan_type == ImageScanType.SCREEN:
    scanner = ScreenScanner()
elif scan_type == ImageScanType.VIDEO:
    scanner = VideoScanner(fn_vid)

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))