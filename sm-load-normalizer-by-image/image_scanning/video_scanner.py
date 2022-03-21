from image_scanning.image_scanner import ImageScanner
import cv2

# Represents scanning images form a video file.
class VideoScanner(ImageScanner):

    def __init__(self, settings):
        super(VideoScanner, self).__init__(settings)
        self.fps = self.settings["vid"]["fps"]
        self.vid = cv2.VideoCapture(self.settings["vid"]["filename_vid"])

        # Threshold for how much difference there needs to be between a frame and
        # the black frame to consider the frame as being almost black.
        black_threshold_ryllus = 500
        self.threshold = 0
        # self.threshold = black_threshold_ryllus
        self.frame_count = 1
        self.load_start_frame = 0

    def get_image_res(self):
        # Detect video resolution from scanning the first frame.
        self.vid = cv2.VideoCapture(self.settings["vid"]["filename_vid"])
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

    def get_time_diff(self):
        return (self.frame_count - self.load_start_frame) / self.fps

    def enter_black_frame(self):
        # DEBUGGING
        print("Entering black at frame", str(self.frame_count))
        super(VideoScanner, self).enter_black_frame()

    def record_position(self):
        self.load_start_frame = self.frame_count

    def increment_position(self):
        self.frame_count += 1

    def get_position(self):
        return self.frame_count

