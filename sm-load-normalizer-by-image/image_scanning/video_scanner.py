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
        self.debug_load_number = 0

    # TODO implement this for screen scanner
    def get_crop_width_and_height(self, fn_vid=""):
        # Determine crop size depending on image resolution
        (res_width, res_height) = self.get_image_res(fn_vid)
        # Make sure that we always have an even number of pixels, so that the image comparison
        # returns a difference of 0 for black screens.

        # Check what aspect ratio we are using.
        if (res_width / res_height) == (16/9):
            test = 1
        elif (res_width / res_height) == (4/3):

        # Assume minimum video resolution of 144p so that there is more control over the
        # crop patch size.
        CONST_MINIMUM_HEIGHT_RES = 144
        # Use widescreen settings (16:9). For any widescreen image, this calculation will always give us the
        # same looking crop in the image, just a different sized patch. This helps debugging as the crop
        # will not vary for different videos.
        percentage_width = (1/16)
        percentage_height = (1/9)
        # Make sure these scales are ints to keep the pixel numbers even.
        width_scale = 1
        height_scale = 1
        # * 2 first so that the number is guaranteed to be even.
        crop_width = (res_width * percentage_width) * 2
        crop_height = (res_height * percentage_height) * 2 / CONST_MINIMUM_HEIGHT_RES
        crop_width *= width_scale
        crop_height *= height_scale
        return (crop_width, crop_height)

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
        # DEBUGGING
        print("Entering black at frame", str(self.frame_count))
        if self.enter_black_count == 1:
            # We are at the end of the load.
            # TODO add this code for image scanner too
            load_frames = self.frame_count - self.load_start_frame
            # Only add the load if it is valid.
            if self.is_load_valid(load_frames / self.fps):
                self.load_frames_total += load_frames
                self.debug_load_number += 1
                print("Load number", str(self.debug_load_number), "added.")
                # Don't add one to enter_black_count, or it will carry over and interfere with the next load screen.
            else:
                # Count this scenario as a regular entering into a black frame.
                self.enter_black_count += 1
            self.reset_load_vars()
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
