from image_scanning.image_scanner import ImageScanner
import cv2

# Represents scanning images form a video file.
class VideoScanner(ImageScanner):

    def __init__(self, settings):
        super(VideoScanner, self).__init__(settings)
        self.fps = self.settings["vid"]["fps"]
        self.vid = cv2.VideoCapture(self.settings["vid"]["filename_vid"])
        self.frame_count = 1
        self.load_start_frame = 0
        self.black_screen_start_frame = 0

    def get_image_res(self):
        # Detect video resolution from scanning the first frame.
        self.vid = cv2.VideoCapture(self.settings["vid"]["filename_vid"])
        success, frame = self.vid.read()
        if not success:
            raise RuntimeError("Could not read the first frame of the video file.")
        return (len(frame[0]), len(frame))

    def get_next_frame(self):
        success, frame = self.vid.read()
        return (success, frame)

    def crop_frame(self, frame):
        return frame[self.crop_y_start:self.crop_y_end, self.crop_x_start:self.crop_x_end]

    def get_load_time_diff(self):
        return (self.frame_count - self.load_start_frame) / self.fps

    def get_black_screen_time_diff(self):
        return (self.frame_count - self.black_screen_start_frame) / self.fps

    def enter_black_frame(self, debug_frame_before_black):
        # DEBUGGING
        print("ENTERING black at frame", str(self.frame_count))
        super(VideoScanner, self).enter_black_frame(debug_frame_before_black)

    def exit_black_frame(self,):
        # DEBUGGING
        print("EXITING black at frame", str(self.frame_count))
        super(VideoScanner, self).exit_black_frame()

    def record_load_start_position(self):
        self.load_start_frame = self.frame_count

    def record_black_screen_start_position(self):
        self.black_screen_start_frame = self.frame_count

    def increment_position(self):
        self.frame_count += 1

    def get_position(self):
        return self.frame_count

