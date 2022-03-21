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

    # Crop scale is the scaling of the size of the cropped patch in the centre of the image,
    # in the form (crop_scale_width, crop_scale_height). fn_vid is the video file name, if using video scanning.
    def __init__(self, settings):
        self.settings = settings

        self.crop_scale = (settings["crop_scale"]["width"], settings["crop_scale"]["height"])
        # Probably not the best way to code this, as this line is only used for video scanning,
        # but I couldn't figure out a nicer way to have the video scanner set the image resolution.
        self.image_res_x, self.image_res_y = self.get_image_res()
        self.x_centre = int(self.image_res_x / 2)
        self.y_centre = int(self.image_res_y / 2)

        # Choose the crop width and height. Greater values give more reliable results when
        # matching images, as you are using more pixels.
        (self.crop_width, self.crop_height) = self.get_crop_width_and_height()
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
        self.load_time_total = 0
        # Counts the number of loads added. Useful for debugging.
        self.debug_load_number = 0

    def find_gcd_from_list(self, nums):
        # https://www.geeksforgeeks.org/gcd-two-array-numbers/
        # Code contributed by Mohit Gupta_OMG
        # GCD of more than two (or array) numbers

        # Function implements the Euclidian
        # algorithm to find the Highest Common Factor (H.C.F.) of two numbers
        def find_gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        num1 = nums[0]
        num2 = nums[1]
        gcd = find_gcd(num1, num2)

        for i in range(2, len(nums)):
            gcd = find_gcd(gcd, nums[i])
        return gcd

    # Determine the crop size depending on the image resolution
    def get_crop_width_and_height(self):
        (res_width, res_height) = self.get_image_res()

        # Parse the supported resolutions. We will proceed with the calculation even if our image
        # resolution is not listed as supported, as there might be a chance that the calculation works out
        # to be a nice number of pixels.
        resolutions = self.settings["res_supported"]
        res_widths = []
        res_heights = []
        for res in resolutions:
            res_widths.append(res[0])
            res_heights.append(res[1])

        # We want the greatest common factor of these resolutions, so that we can divide the width and height
        # by the greatest number possible, while still allowing the division to result in an integer number of
        # pixels. Using the greatest number possible lets the crop size parameter be tuned as finely as possible.
        # Tuning the crop size parameter finely is useful for cases where an image has a chance to
        # be falsely detected as a black screen due to having black pixels in the centre.
        gcd_res_width = self.find_gcd_from_list(res_widths)
        gcd_res_height = self.find_gcd_from_list(res_heights)

        # For any image of the resolutions specified in self.vid_res_supported, this calculation will always give us the
        # same looking crop in the image, just a larger number of patch pixels for higher resolution videos which have
        # more pixels. This helps debugging as the cropped image will not vary for different resolutions of the same
        # video.
        percentage_width = 1 / gcd_res_width
        percentage_height = 1 / gcd_res_height
        # Make sure these scales are ints to keep the pixel numbers even.
        width_scale = (int) (self.crop_scale[0])
        height_scale = (int) (self.crop_scale[1])
        # * 2 first so that the number is guaranteed to be even.
        crop_width = (int) ((res_width * percentage_width) * 2)
        crop_height = (int) ((res_height * percentage_height) * 2)
        crop_width *= width_scale
        crop_height *= height_scale
        return (crop_width, crop_height)

    # Gets the image resolution in pixels (width, height) to be used in the cropping
    # process. fn_vid is the video file name, if using video scanning.
    def get_image_res(self):
        raise NotImplementedError

    # Returns the cropped black frame to compare frames against for the start and end of the load.
    def get_black_cropped(self):
        return np.zeros((self.crop_y_end - self.crop_y_start, self.crop_x_end - self.crop_x_start, 3), np.uint8)

    # Returns whether getting the frame was successful, and the frame data as a numpy array of pixels.
    def get_next_frame_cropped(self):
        raise NotImplementedError

    # Adds the load to the total load time.
    def add_load_to_total(self, load_time):
        raise NotImplementedError

    # Functionality performed when going from a non-black frame to a black frame (entering).
    # This functionality is important for timing the loads.
    def enter_black_frame(self):
        if self.enter_black_count == 1:
            # We are at the end of the load.
            load_time = self.get_time_diff()
            # Only add the load if it is valid.
            if self.is_load_valid(load_time):
                self.load_time_total += load_time
                # DEBUGGING
                self.debug_load_number += 1
                print("Load number", str(self.debug_load_number), "added.")
                # Don't add one to enter_black_count, or it will carry over and interfere with the next load screen.
            else:
                # Count this scenario as a regular entering into a black frame.
                self.enter_black_count += 1
            self.reset_load_vars()
            return
        self.enter_black_count += 1

    # Functionality performed when going from a black frame to a non-black frame (exiting).
    # This functionality is important for timing the loads.
    def exit_black_frame(self):
        if self.enter_black_count == 1:
            self.record_position()

    def is_load_valid(self, load_time):
        return (load_time > self.CONST_LOAD_THRESH_LOW_SECONDS) and (load_time < self.CONST_LOAD_THRESH_HIGH_SECONDS)

    # Records the current position, which is either the current frame or current time.
    def record_position(self):
        raise NotImplementedError

    # Increments the position, which is either the frame number for the video scanning,
    # or the total time for the screen scanning.
    def increment_position(self):
        raise NotImplementedError

    # Get the current position, which is either the frame number for the video scanning,
    # or the current time for the screen scanning.
    def get_position(self):
        raise NotImplementedError

    # Get the difference in time between the last measured time and now. This is used to
    # time loads.
    def get_time_diff(self):
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

        self.print_finished_stats()

    # Prints stats about the program once it's finished.
    def print_finished_stats(self):
        print("Total load time is:", round(self.load_time_total, 2), "seconds")