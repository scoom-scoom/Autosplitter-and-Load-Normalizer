from image_scanning.image_scanner import ImageScanner
import cv2
import numpy as np

# Represents scanning images form a video file.
class VideoScanner(ImageScanner):

    vid_res_x = 852
    vid_res_y = 480
    x_mid = (vid_res_x / 2)
    y_mid = (vid_res_y / 2)
    crop_width = 100
    crop_height = 100
    crop_x_start = int(x_mid - crop_width)
    crop_x_end = int(x_mid + crop_width)
    crop_y_start = int(y_mid - crop_height)
    crop_y_end = int(y_mid + crop_height)

    def __init__(self, fn_vid):
        super(VideoScanner, self).__init__()
        self.vid = cv2.VideoCapture(fn_vid)

        # Threshold for how much difference there needs to be between a frame and the black frame to consider the frame as being almost black.
        black_threshold_ryllus = 500
        self.threshold = black_threshold_ryllus
        self.frame_count = 1
        self.load_start_frame = 0
        self.load_frames_total = 0
        self.fps = 30

    def get_black_cropped(self):
        return np.zeros((self.crop_y_end - self.crop_y_start, self.crop_x_end - self.crop_x_start, 3), np.uint8)

    def get_next_frame_cropped(self):
        success, frame = self.vid.read()
        frame_cropped = None
        if success:
            frame_cropped = frame[self.crop_y_start:self.crop_y_end, self.crop_x_start:self.crop_x_end]
        return (success, frame_cropped)

    def enter_black_frame(self):
        if self.enter_black_count == 1:
            # We are at the end of the load.
            self.load_frames_total += (self.frame_count - self.load_start_frame)
            self.reset_load_vars()
            # Don't add one to enter_black_count, or it will carry over and interfere with the next load screen.
            return
        self.enter_black_count += 1

    def exit_black_frame(self):
        if self.enter_black_count == 1:
            self.load_start_frame = self.frame_count

    def increment_position(self):
        self.frame_count += 1

    def get_position(self):
        return self.frame_count

    def print_final_load_time(self):
        print("Total load time is:", round(self.load_frames_total / self.fps, 2), "seconds")
