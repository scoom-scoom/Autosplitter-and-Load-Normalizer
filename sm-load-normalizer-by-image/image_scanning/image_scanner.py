import math
import os
import cv2
import numpy as np
from collections import deque

# Keeps track of where the scanner is in terms of load measurement.
# A black screen is a sequence of black images.
class ScannerState:
    DEFAULT = 1
    IN_FIRST_BLACK_SCREEN = 2
    IN_POTENTIAL_LOAD = 3
    IN_SECOND_BLACK_SCREEN = 4


# Debug frames code. Debug frames are frames around the measured loads which are printed out later for
# debugging purposes.
# class DebugFrames:
#
#     before = deque()
#     after = deque()
#
#     def __init__(self):
#         pass
#
#     def get_all_frames(self):
#         return self.before.extend(self.after)


# Represents the process of scanning frames.
class ImageScanner:

    def __init__(self, settings):
        self.settings = settings
        # Init crop settings
        # self.crop_scale = (settings["crop_scale"]["width"], settings["crop_scale"]["height"])
        self.image_res_width, self.image_res_height = self.get_image_res()
        x_centre = int(self.image_res_width / 2)
        y_centre = int(self.image_res_height / 2)
        # Crop size must be big, as the Remains ship cutscene has a big black pixel patch in the centre,
        # under the orange shaped remains planet, just before the load is finished.
        # (self.crop_width, self.crop_height) = (100, 100)
        # OG crop size which works for Alemusa Any% vid.
        (self.crop_width, self.crop_height) = (50, 50)
        # (self.crop_width, self.crop_height) = (2, 2)
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
        # self.threshold = 50
        self.threshold = 0
        # The number of times we have entered a black screen. Useful for checking when to start the load timing.
        # self.enter_black_count = 0
        self.scanner_state = ScannerState.DEFAULT
        # Number of extra debug frames to write before and after each debug frame.
        self.d_extra_frames_range = 5
        self.load_time_total = 0
        self.load_bounds = self.settings["load_bounds"]
        self.black_screen_bounds = self.settings["black_screen_bounds"]
        self.poki_sped_up = settings["poki_sped_up"]
        if self.poki_sped_up:
            print("Poki is sped up, so is already accounted for.")
        # Counts the number of loads added. Useful for debugging.
        self.loads_added = 1 if self.poki_sped_up else 0
        self.loads_to_skip = settings["loads_to_skip"]
        # Clear the old debug frame data.
        self.dir_working = os.path.abspath(os.getcwd())
        self.dir_frames = os.path.join(self.dir_working, "frames_output")
        if os.path.exists(self.dir_frames):
            # Delete previous output frames.
            for filename in os.listdir(self.dir_frames):
                f = os.path.join(self.dir_frames, filename)
                # Check if it is a file
                if os.path.isfile(f):
                    os.remove(f)
        else:
            os.mkdir(self.dir_frames)

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

    # Gets the next frame according to the current position.
    # Returns (success, frame):
    # - "success" states if the frame read was successful.
    # - "frame" is the frame data as a numpy array of pixels.
    def get_next_frame(self):
        raise NotImplementedError

    # Gets the frame given by the frame index.
    # Returns (success, frame):
    # - "success" states if the frame read was successful.
    # - "frame" is the frame data as a numpy array of pixels.
    def get_frame_by_index(self, frame_index):
        raise NotImplementedError

    def crop_frame(self, frame):
        raise NotImplementedError

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def record_load_start_position(self):
        raise NotImplementedError

    # Same functionality as "record_load_position", just for black screens instead.
    def record_black_screen_start_position(self):
        raise NotImplementedError

    # Get the difference in time between the last measured time and now. This is used to
    # time loads.
    def get_load_time_diff(self):
        raise NotImplementedError

    # Same functionality as "get_load_time_diff", just for black screens instead.
    def get_black_screen_time_diff(self):
        raise NotImplementedError

    def get_error_too_many_loads(self):
        return "ERROR: Trying to record more loads than there are in the category.\
                             A false load must have been recorded at some point."

    def get_load_bounds(self, load_number):
        try:
            load_bound = self.load_bounds[load_number]
        except IndexError as e:
            raise IndexError(self.get_error_too_many_loads()) from e
        return (load_bound[0], load_bound[1])

    def is_black_screen_valid(self, black_time):
        try:
            bound = self.black_screen_bounds[self.loads_added]
        except IndexError as e:
            raise IndexError(self.get_error_too_many_loads()) from e
        if bound == 'IGNORE':
            return True
        else:
            # Check if the black screen is valid given the bounds.
            if self.scanner_state != ScannerState.IN_FIRST_BLACK_SCREEN:
                raise RuntimeError("Trying to check valid black screen, but the scanner state is not\
                                   in the first black screen!")
            ignore_first_bound = bound[0] == 'IGNORE'
            ignore_second_bound = bound[1] == 'IGNORE'
            if ignore_first_bound and ignore_second_bound:
                return True
            elif ignore_first_bound:
                return black_time < bound[1]
            elif ignore_second_bound:
                return black_time > bound[0]
            return (bound[0] < black_time) and (black_time < bound[1])

    def record_load_time(self, load_time):
        # Check if it is the Pokitaru load (the first load), which is not counted
        # in the speed run.
        if (self.loads_added == 0):
            print("Pokitaru load detected and skipped")
        else:
            self.load_time_total += load_time
            # DEBUGGING
            # print("Load number", str(self.loads_added + 1), "added.")
            # print("Load time removed is: ", str(round(load_remove_time, 2)))
        self.loads_added += 1

    # Functionality performed when going from a non-black frame to a black frame (entering).
    # This functionality is important for timing the loads.
    def enter_black_frame(self, d_indices_enter_black, d_indices_exit_black):
        if self.scanner_state == ScannerState.DEFAULT:
            self.scanner_state = ScannerState.IN_FIRST_BLACK_SCREEN
            # self.debug_frame_before_load_enter_black = debug_frame_before_black
            # Time the black screen to make sure it is valid.
            self.record_black_screen_start_position()
        elif self.scanner_state == ScannerState.IN_POTENTIAL_LOAD:
            # We are at the end of the load.
            load_time = self.get_load_time_diff()
            # Only add the load if it is valid.
            load_bound_min, load_bound_max = self.get_load_bounds(self.loads_added)
            # "load_bound_min - 0.5" and "load_bound_max + 0.5" to be safe, as the bounds are taken
            # from a large sample of loads, but there may be a load which goes beyond these bounds.
            load_bound_min_relaxed = load_bound_min - 0.5
            load_bound_max_relaxed = load_bound_max + 0.5
            if (load_time > load_bound_min_relaxed) and (load_time < load_bound_max_relaxed):
                self.record_load_time(load_time)
                self.scanner_state = ScannerState.IN_SECOND_BLACK_SCREEN
                # DEBUGGING
                # cv2.imwrite("frames/enter-black-load_" + str(self.loads_added) + "-_before" + ".png",
                #             self.debug_frame_before_load_enter_black)
                # self.debug_frame_after_load = debug_frame_before_black
                # cv2.imwrite("frames/enter-black-load_" + str(self.loads_added) + "-after" + ".png",
                #             self.debug_frame_after_load)
                # Don't add one to "enter_black_count" here, just return and begin the process again.
            else:
                # No load was added, so count this as the first enter_black_frame.
                self.scanner_state = ScannerState.IN_FIRST_BLACK_SCREEN
                d_indices_enter_black.pop()
                d_indices_exit_black.pop()

                # Time the black screen to make sure it is valid.
                self.record_black_screen_start_position()
        d_indices_enter_black.append(self.get_position())
        return (d_indices_enter_black, d_indices_exit_black)

    # Functionality performed when going from a black frame to a non-black frame (exiting).
    # This functionality is important for timing the loads.
    def exit_black_frame(self, d_indices_enter_black, d_indices_exit_black):
        if self.scanner_state == ScannerState.IN_FIRST_BLACK_SCREEN:
            black_time = self.get_black_screen_time_diff()
            if self.is_black_screen_valid(black_time):
                self.scanner_state = ScannerState.IN_POTENTIAL_LOAD
                self.record_load_start_position()
                d_indices_exit_black.append(self.get_position())
            else:
                # We know that there cannot be a load after this black screen, so restart the
                # load measurement process.
                self.scanner_state = ScannerState.DEFAULT
                d_indices_enter_black.pop()
        elif self.scanner_state == ScannerState.IN_SECOND_BLACK_SCREEN:
            # We have finished recording this load. Set the scanner state back to default to
            # prepare for measuring the next load.
            self.scanner_state = ScannerState.DEFAULT
            d_indices_exit_black.append(self.get_position())
        return (d_indices_enter_black, d_indices_exit_black)

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def increment_position(self):
        raise NotImplementedError

    # The position is either a frame number for video scanning, or a time stamp for screen scanning.
    def get_position(self):
        raise NotImplementedError

    # Given two frames, returns true if the euclidean distance (pixel distance) between them is less than the threshold.
    def are_frames_almost_equal(self, frame_one, frame_two, threshold=0):
        str_debug = "Position: "
        str_debug += str(self.get_position())
        if threshold == 0:
            # Perform less expensive "array_equal" operation instead of calculating the norm.
            almost_equal = np.array_equal(frame_one, frame_two)
            str_debug += " Is Frame equal? " + str(almost_equal)
        else:
            # Perform more expensive norm calculation only if necessary.
            norm = np.linalg.norm(frame_one - frame_two)
            almost_equal = norm < threshold
            str_debug += " Norm: " + str(norm)
            # print(str_debug)
        # if almost_equal:
        #     print(str_debug)
        return almost_equal

    def start_scan_loop(self):
        # Debug frames to be printed out for debugging. These frames will be before and after each
        # black screen entrance and exit.
        # d_frames = []

        # Indices for the frame number entering and exiting the black screens before and after each load.
        # Used for debugging purposes.
        d_indices_enter_black = []
        d_indices_exit_black = []
        success, frame = self.get_next_frame()
        if not success:
            raise RuntimeError("Failed to read first frame.")
        self.increment_position()
        # d_frames.append(frame)
        frame_cropped = self.crop_frame(frame)

        is_prev_frame_almost_black = False
        # DEBUGGING
        # debug_prev_frame = frame
        # Debug frames additional count before and after the load.
        # d_f_adtnl_cnt_before_load = 0
        # d_f_adtnl_cnt_after_load = 0
        while success:
            if self.is_finished or self.loads_added == 13:
                break
            next_load = self.loads_added + 1
            if next_load in self.loads_to_skip:
                # Skip the load
                print("Load " + str(next_load) + " skipped.")
                self.loads_added += 1
            is_curr_frame_almost_black = self.are_frames_almost_equal(frame_cropped, self.black_cropped, self.threshold)
            if (not is_prev_frame_almost_black) and is_curr_frame_almost_black:
                (d_indices_enter_black, d_indices_exit_black) = self.enter_black_frame(d_indices_enter_black,
                                                                                       d_indices_exit_black)
                # DEBUGGING
                # cv2.imwrite("frames/test.png", frame)
            elif is_prev_frame_almost_black and (not is_curr_frame_almost_black):
                (d_indices_enter_black, d_indices_exit_black) = self.exit_black_frame(d_indices_enter_black,
                                                                                      d_indices_exit_black)
            # DEBUGGING
            # Keep track of the debug frames which will be printed out later.
            # if self.scanner_state == ScannerState.DEFAULT:
            #     self.d_f_before_load, d_f_adtnl_cnt_before_load = \
            #         self.add_d_f_before_black_screen(self.d_f_before_load, frame, d_f_adtnl_cnt_before_load)
            # elif self.scanner_state == ScannerState.IN_FIRST_BLACK_SCREEN:
            #     self.d_f_before_load.append(frame)
            #     d_f_adtnl_cnt_before_load = 0
            # elif self.scanner_state == ScannerState.IN_POTENTIAL_LOAD:
            #     self.d_f_before_load, d_f_adtnl_cnt_before_load = \
            #         self.add_d_f_after_black_screen(self.d_f_before_load, frame, d_f_adtnl_cnt_before_load)
            # debug_prev_frame = frame

            # Read the next frame.
            success, frame = self.get_next_frame()
            if success:
                # if self.scanner_state != ScannerState.DEFAULT:
                #     # Only append the save frames
                #     d_frames.append(frame)
                frame_cropped = self.crop_frame(frame)
                # Update the "is_prev_frame_almost_black" variable for the next loop iteration.
                is_prev_frame_almost_black = is_curr_frame_almost_black
                self.increment_position()

            # DEBUGGING
            # if self.get_position() > 100:
            #     break
        self.log_debug_frames(d_indices_enter_black, d_indices_exit_black)
        self.print_finished_stats()

    # # Adds the debug frame to the list according to the logic before the black screen.
    # # Returns
    # # - The debug frames list
    # # - The additional count of debug frames.
    # def add_d_f_before_black_screen(self, d_f_list, frame, additional_count):
    #     d_f_list.append(frame)
    #     additional_count += 1
    #     if additional_count > self.d_f_additional_num:
    #         del self.d_f_before_load[0]
    #         additional_count -= 1
    #     return (d_f_list, additional_count)
    #
    # # Adds the debug frame to the list according to the logic after the black screen.
    # # Returns
    # # - The debug frames list
    # # - The additional count of debug frames.
    # def add_d_f_after_black_screen(self, d_f_list, frame, additional_count):
    #     d_f_list.append(frame)
    #     additional_count += 1
    #     if additional_count > self.d_f_additional_num:
    #         length = len(d_f_list)
    #         del d_f_list[length - 1]
    #         additional_count -= 1
    #     return (d_f_list, additional_count)

    # Prints stats about the program once it's finished.
    def print_finished_stats(self):
        print("Total load time is:", round(self.load_time_total, 2), "seconds")

    def log_debug_frames(self,  d_indices_enter_black, d_indices_exit_black):
        self.log_frames_from_indices(d_indices_enter_black)
        self.log_frames_from_indices(d_indices_exit_black)

    def log_frames_from_indices(self, indices):
        for i in range(len(indices)):
            frame_index = indices[i]
            # 2 enter and exit black frames occur for each load, hence i / 2.
            load_num = math.floor(i / 2) + 1
            for j_before in range(self.d_extra_frames_range + 1):
                frame_index_new = frame_index - j_before
                self.write_d_frame(frame_index_new, load_num)
            for j_after in range(self.d_extra_frames_range + 1):
                if j_after == 0:
                    # Skip the case where frame_index_new == frame_index, which was covered
                    # in the previous for loop.
                    continue
                frame_index_new = frame_index + j_after
                self.write_d_frame(frame_index_new, load_num)

    def write_d_frame(self, frame_index, load_num):
        success, frame = self.get_frame_by_index(frame_index)
        filename = "load_" + str(load_num) + "-frame_num_" + str(frame_index) + ".png"
        frame_name = os.path.join(self.dir_frames, filename)
        if success:
            cv2.imwrite(frame_name, frame)
        else:
            print("WARNING: Failed to write debug frame named: ", frame_name)
