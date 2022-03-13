import numpy as np

# Represents the process of scanning frames.
class ImageScanner:

    # The thresholds below are used because of the fact that a load is defined as a series of image
    # frames between two black screens. This leads to problems if not delt with properly.

    # All loads must be higher than this time to be considered a load. This stops other image frames
    # between black screens throughout the run from accidentally being counted as a load.
    # Example:
    # - A black screen between gameplay and a cutscene, and skipping the cutscene sends you
    # back to a black screen, but you do not want the cutscene to be accidentally counted as a load).
    CONST_LOAD_THRESH_LOW_SECONDS = 5

    # All loads must be lower than this time to be considered a load. This stops ship proxies from
    # counting gameplay as a load, as ship proxies give a black screen.
    CONST_LOAD_THRESH_HIGH_SECONDS = 25

    # fn_vid is the video file name, if using video scanning.
    def __init__(self, fn_vid=""):
        # Probably not the best way to code this, as this line is only used for video scanning,
        # but I couldn't figure out a nicer way to have the video scanner set the image resolution.
        self.image_res_x, self.image_res_y = self.get_image_res(fn_vid)
        self.x_centre = int(self.image_res_x / 2)
        self.y_centre = int(self.image_res_y / 2)

        # Choose the crop width and height. Greater values give more reliable results when
        # matching images, as you are using more pixels.
        # self.crop_width = 4
        # self.crop_height = 4
        (self.crop_width, self.crop_height) = self.get_crop_width_and_height(fn_vid)
        if (self.crop_width % 2) != 0:
            raise RuntimeError("Crop width not divisible by 2.")
        if (self.crop_height % 2) != 0:
            raise RuntimeError("Crop height not divisible by 2.")
        self.crop_half_width = int(self.crop_width / 2)
        self.crop_half_height = int(self.crop_height / 2)
        self.crop_x_start = self.x_centre - self.crop_half_width
        self.crop_x_end = self.x_centre + self.crop_half_width
        self.crop_y_start = self.y_centre - self.crop_half_height
        self.crop_y_end = self.y_centre + self.crop_half_height

        self.black_cropped = self.get_black_cropped()
        self.is_finished = False
        # Threshold for how much difference there needs to be between a frame and
        # the black frame to consider the frame as being almost black.
        self.threshold = 0
        # The number of times we have entered a black screen. Useful for checking when to start the load timing.
        self.enter_black_count = 0

    def get_crop_width_and_height(self, fn_vid=""):
        raise NotImplementedError

    # Gets the image resolution in pixels (width, height) to be used in the cropping
    # process. fn_vid is the video file name, if using video scanning.
    def get_image_res(self, fn_vid=""):
        raise NotImplementedError

    # Returns the cropped black frame to compare frames against for the start and end of the load.
    def get_black_cropped(self):
        return np.zeros((self.crop_y_end - self.crop_y_start, self.crop_x_end - self.crop_x_start, 3), np.uint8)

    # Returns whether getting the frame was successful, and the frame data as a numpy array of pixels.
    def get_next_frame_cropped(self):
        raise NotImplementedError

    # Functionality performed when going from a non-black frame to a black frame (entering).
    # This functionality is important for timing the loads.
    def enter_black_frame(self):
        raise NotImplementedError

    # Functionality performed when going from a black frame to a non-black frame (exiting).
    # This functionality is important for timing the loads.
    def exit_black_frame(self):
        raise NotImplementedError

    def is_load_valid(self, load_time):
        return (load_time > self.CONST_LOAD_THRESH_LOW_SECONDS) and (load_time < self.CONST_LOAD_THRESH_HIGH_SECONDS)

    # Increments the position, which is either the frame number for the video scanning,
    # or the total time for the screen scanning.
    def increment_position(self):
        raise NotImplementedError

    # Get the current position, which is either the frame number for the video scanning,
    # or the current time for the screen scanning.
    def get_position(self):
        raise NotImplementedError

    # Resets variables after a load is timed, to prepare the variables for the next load.
    def reset_load_vars(self):
        self.enter_black_count = 0

    # Given two frames, returns true if the euclidean (pixel) distance between them is less than the threshold.
    # You can also supply the frame for debugging purposes.
    def are_frames_almost_equal(self, frame_one, frame_two, threshold=0):
        str_debug = "Position: "
        str_debug += str(self.get_position())
        if threshold == 0:
            almost_equal = np.array_equal(frame_one, frame_two)
            # str_debug += " Is Frame equal? " + str(almost_equal)
        else:
            # Perform more expensive norm calculation only if necessary.
            norm = np.linalg.norm(frame_one - frame_two)
            almost_equal = norm < threshold
            str_debug += " Norm: " + str(norm)
        # print(str_debug)
        return almost_equal

    def print_final_load_time(self):
        raise NotImplementedError

    def start_scan_loop(self):
        success, frame = self.get_next_frame_cropped()
        if not success:
            raise RuntimeError("Failed to read first frame.")

        is_prev_frame_black = False
        while success:
            if self.is_finished:
                break

            is_curr_frame_black = self.are_frames_almost_equal(frame, self.black_cropped, self.threshold)
            if (not is_prev_frame_black) and is_curr_frame_black:
                self.enter_black_frame()
            elif is_prev_frame_black and (not is_curr_frame_black):
                self.exit_black_frame()
            # Read the next frame.
            success, frame = self.get_next_frame_cropped()
            if success:
                # Update the is_prev_frame_black variable for the next loop iteration.
                is_prev_frame_black = is_curr_frame_black
                self.increment_position()

            # DEBUGGING
            # break

        self.print_final_load_time()
