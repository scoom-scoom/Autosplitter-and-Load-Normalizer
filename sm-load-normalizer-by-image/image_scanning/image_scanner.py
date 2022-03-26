import cv2
import numpy as np

# Represents the process of scanning frames.
class ImageScanner:

    def __init__(self, settings):
        self.settings = settings
        # Init crop settings
        # self.crop_scale = (settings["crop_scale"]["width"], settings["crop_scale"]["height"])
        self.image_res_width, self.image_res_height = self.get_image_res()
        x_centre = int(self.image_res_width / 2)
        y_centre = int(self.image_res_height / 2)
        (self.crop_width, self.crop_height) = (2, 2)
        # (self.crop_width, self.crop_height) = self.get_crop_width_and_height()
        if (self.crop_width % 2) != 0:
            print("Crop width not divisible by 2.")
            self.crop_width += 1
        if (self.crop_height % 2) != 0:
            print("Crop height not divisible by 2.")
            self.crop_height += 1
        crop_half_width = int(self.crop_width / 2)
        crop_half_height = int(self.crop_height / 2)
        self.crop_x_start = x_centre - crop_half_width
        self.crop_x_end = x_centre + crop_half_width
        self.crop_y_start = y_centre - crop_half_height
        self.crop_y_end = y_centre + crop_half_height
        self.black_cropped = self.get_black_cropped()
        self.is_finished = False
        # Threshold for how much difference there needs to be between a frame and
        # the black frame to consider the frame as being almost black.
        self.threshold = 0
        # The number of times we have entered a black screen. Useful for checking when to start the load timing.
        self.enter_black_count = 0
        self.load_time_total = 0
        self.load_bounds = self.settings["load_bounds"]
        self.poki_sped_up = settings["poki_sped_up"]
        if self.poki_sped_up:
            print("Poki is sped up, so is already accounted for.")
        # Counts the number of loads added. Useful for debugging.
        self.loads_added = 1 if self.poki_sped_up else 0
        self.debug_frame_before_load = None
        self.debug_frame_after_load = None

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
        # We will proceed with the calculation even if our image resolution is not listed as
        # supported, as there might be a chance that the calculation works out to be a nice
        # number of pixels.
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
        # be falsely detected as a black screen due to having black pixels in the centre (e.g. during
        # ship proxies).
        gcd_res_width = self.find_gcd_from_list(res_widths)
        gcd_res_height = self.find_gcd_from_list(res_heights)

        # For any image of the resolutions specified in the "resolutions" variable, this calculation
        # will always give us the same looking crop in the image, just a larger number of cropped pixels
        # for higher resolution videos which have more pixels. This helps debugging as the content in the
        # cropped image will not vary for different resolutions of the same video.
        percentage_width = 1 / gcd_res_width
        percentage_height = 1 / gcd_res_height
        # Make sure these scales are ints to keep the pixel numbers integers.
        width_scale = (int) (self.crop_scale[0])
        height_scale = (int) (self.crop_scale[1])
        # * 2 first so that the number is guaranteed to be even.
        crop_width = (int) ((self.image_res_width * percentage_width) * 2)
        crop_height = (int) ((self.image_res_height * percentage_height) * 2)
        crop_width *= width_scale
        crop_height *= height_scale
        return (crop_width, crop_height)

    # Gets the image resolution in pixels (width, height) to be used in the cropping process.
    def get_image_res(self):
        raise NotImplementedError

    # Returns the cropped black frame to compare frames against for the start and end of the load.
    def get_black_cropped(self):
        return np.zeros((self.crop_y_end - self.crop_y_start, self.crop_x_end - self.crop_x_start, 3), np.uint8)

    # Returns (success, frame):
    # - "success" states if the frame read was successful.
    # - "frame" is the frame data as a numpy array of pixels.
    def get_next_frame(self):
        raise NotImplementedError

    def crop_frame(self, frame):
        raise NotImplementedError

    def is_load_valid(self, load_number, load_time):
        try:
            load_bound = self.load_bounds[load_number]
        except IndexError:
            load_bound = [2, 25]
        # load_bounds = self.settings["load_bounds"]
        # load_bound = load_bounds[load_number]

        # "load_bound[0] - 1" and "load_bound[1] + 1" to be safe, as the bounds are taken from a large sample of loads,
        # but there may be a load which goes beyond these bounds.
        load_bound_min = load_bound[0] - 1
        load_bound_max = load_bound[1] + 1
        return (load_time > load_bound_min) and (load_time < load_bound_max)

    def record_load(self, load_time):
        # Check if it is the Pokitaru load (the first load), which is not counted
        # in the speed run.
        if (self.loads_added == 0) and (not self.poki_sped_up):
            self.loads_added += 1
            print("Pokitaru load detected and skipped")
        else:
            self.load_time_total += load_time
            # DEBUGGING
            self.loads_added += 1
            print("Load number", str(self.loads_added), "added.")

    # Functionality performed when going from a non-black frame to a black frame (entering).
    # This functionality is important for timing the loads.
    def enter_black_frame(self, debug_frame_before_black):
        # DEBUGGING
        if self.enter_black_count == 0:
            self.enter_black_count = 1
            self.debug_frame_before_load = debug_frame_before_black
        elif self.enter_black_count == 1:
            # We are at the end of the load.
            load_time = self.get_time_diff()
            # Only add the load if it is valid.
            if self.is_load_valid(self.loads_added, load_time):
                self.record_load(load_time)
                self.enter_black_count = 0
                # DEBUGGING
                cv2.imwrite("frames/enter-black-load_" + str(self.loads_added) + "-_before" + ".png",
                            self.debug_frame_before_load)
                cv2.imwrite("frames/enter-black-load_" + str(self.loads_added) + "-after" + ".png",
                            debug_frame_before_black)
                # Don't add one to "enter_black_count" here, just return and begin the process again.
            else:
                # No load was added, so count this as the first enter_black_frame.
                self.enter_black_count = 1

    # Functionality performed when going from a black frame to a non-black frame (exiting).
    # This functionality is important for timing the loads.
    def exit_black_frame(self):
        if self.enter_black_count == 1:
            self.record_position()

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def record_position(self):
        raise NotImplementedError

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def increment_position(self):
        raise NotImplementedError

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def get_position(self):
        raise NotImplementedError

    # Get the difference in time between the last measured time and now. This is used to
    # time loads.
    def get_time_diff(self):
        raise NotImplementedError

    # Given two frames, returns true if the euclidean distance (pixel distance) between them is less than the threshold.
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
        success, frame = self.get_next_frame()
        if not success:
            raise RuntimeError("Failed to read first frame.")
        frame_cropped = self.crop_frame(frame)

        is_prev_frame_black = False
        # DEBUGGING
        debug_prev_frame = frame
        assign_debug_frame = 0
        while success:
            if self.is_finished:
                break

            is_curr_frame_black = self.are_frames_almost_equal(frame_cropped, self.black_cropped, self.threshold)
            if (not is_prev_frame_black) and is_curr_frame_black:
                self.enter_black_frame(debug_prev_frame)
            elif is_prev_frame_black and (not is_curr_frame_black):
                self.exit_black_frame()
            # DEBUGGING
            # Save every 50th frame, as many frames right before the black screen are very close to black due to the
            # ship fade out, so are not useful for telling where the load was measured.
            if assign_debug_frame % 50 == 0:
                debug_prev_frame = frame
            # Read the next frame.
            success, frame = self.get_next_frame()
            if success:
                frame_cropped = self.crop_frame(frame)
                # Update the "is_prev_frame_black" variable for the next loop iteration.
                is_prev_frame_black = is_curr_frame_black
                self.increment_position()

            # DEBUGGING
            # break
            assign_debug_frame += 1
        self.print_finished_stats()

    # Prints stats about the program once it's finished.
    def print_finished_stats(self):
        print("Total load time is:", round(self.load_time_total, 2), "seconds")