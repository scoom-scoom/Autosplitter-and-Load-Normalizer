from image_scanning.image_scanner import ImageScanner
import cv2

# Represents scanning images form a video file.
class VideoScanner(ImageScanner):

    def __init__(self, settings):
        super(VideoScanner, self).__init__(settings)
        self.fps = self.settings["vid"]["fps"]
        self.vid = cv2.VideoCapture(self.settings["vid"]["filename_vid"])
        self.total_frames = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.frame_pos = -1
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
        # DEBUGGING
        frame_num = self.vid.get(1)

        success, frame = self.vid.read()
        return (success, frame)

    def get_frame_by_index(self, frame_index):
        frame_pos_curr = self.get_position()
        frame_pos_new = frame_index
        # -1 to convert frame index to 0-based CAP_PROP_POS_FRAMES index.
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_pos_new - 1)
        success, frame = self.vid.read()
        # Return the vid frame position to its original state.
        self.vid.set(cv2.CAP_PROP_POS_FRAMES, frame_pos_curr - 1)
        return (success, frame)

    def crop_frame(self, frame):
        return frame[self.crop_y_start:self.crop_y_end, self.crop_x_start:self.crop_x_end]

    def get_load_time_diff(self):
        return (self.frame_pos - self.load_start_frame) / self.fps

    def get_black_screen_time_diff(self):
        return (self.frame_pos - self.black_screen_start_frame) / self.fps

    def enter_black_frame(self, d_indices_enter_black, d_indices_exit_black):
        # DEBUGGING
        print("ENTERING black at frame", str(self.frame_pos))
        return super(VideoScanner, self).enter_black_frame(d_indices_enter_black, d_indices_exit_black)

    def exit_black_frame(self, d_indices_enter_black, d_indices_exit_black):
        # DEBUGGING
        print("EXITING black at frame", str(self.frame_pos))
        return super(VideoScanner, self).exit_black_frame(d_indices_enter_black, d_indices_exit_black)

    def record_load_start_position(self):
        self.load_start_frame = self.frame_pos

    def record_black_screen_start_position(self):
        self.black_screen_start_frame = self.frame_pos

    def increment_position(self):
        self.frame_pos += 1

    def get_position(self):
        return self.frame_pos

    # DEBUGGING
    def are_frames_almost_equal(self, frame_one, frame_two, threshold=0):
        return super(VideoScanner, self).are_frames_almost_equal(frame_one, frame_two, threshold)

