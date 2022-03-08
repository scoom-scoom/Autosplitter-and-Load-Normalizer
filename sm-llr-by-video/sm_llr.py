import numpy as np
import time
from image_scanning.screen_scanner import ScreenScanner
from image_scanning.video_scanner import VideoScanner

# is_screen_cap = False
is_screen_cap = True
fn_vid = "C:/Users/josho/Desktop/Big-Brother/vids/autosplitting/llr-test-7th-pb.mp4"

scanner = None
if is_screen_cap:
    scanner = ScreenScanner()
else:
    scanner = VideoScanner(fn_vid)

start = time.time()
scanner.start_scan_loop()
end = time.time()
print("Total program runtime:", round(end - start, 2))