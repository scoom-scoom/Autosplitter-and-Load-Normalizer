from image_scanning.image_scanner import ImageScanner
import cv2

# Represents scanning images form a video file.
class VideoScanner(ImageScanner):

    def __init__(self, fn_vid="", fps=30):
        self.fps = fps
        super(VideoScanner, self).__init__(fn_vid)
        self.vid = cv2.VideoCapture(fn_vid)

        # Threshold for how much difference there needs to be between a frame and
        # the black frame to consider the frame as being almost black.
        black_threshold_ryllus = 500
        self.threshold = 0
        # self.threshold = black_threshold_ryllus
        self.frame_count = 1
        self.load_start_frame = 0
        self.load_frames_total = 0

    def get_image_res(self, fn_vid=""):
        # Detect video resolution from scanning the first frame.
        self.vid = cv2.VideoCapture(fn_vid)
        success, frame = self.vid.read()
        if not success:
            raise RuntimeError("Could not read the first frame of the video file.")
        return (len(frame[0]), len(frame))

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

    def reset_load_vars(self):
        super(VideoScanner, self).reset_load_vars()
        self.load_start_frame = self.frame_count

    def increment_position(self):
        self.frame_count += 1

    def get_position(self):
        return self.frame_count

    def print_final_load_time(self):
        print("Total load time is:", round(self.load_frames_total / self.fps, 2), "seconds")
