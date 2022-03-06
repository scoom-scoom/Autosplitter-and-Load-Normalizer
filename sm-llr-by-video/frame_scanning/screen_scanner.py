
from frame_scanning.frame_scanner import FrameScanner
import numpy as np
import win32gui
import win32ui
import win32com
import win32com.client
import win32con
import time

import glob
import os
from PIL import Image

# Represents scanning frames of the current screen.
class ScreenScanner(FrameScanner):

    # crop_x_start = 400
    # crop_x_end = 900
    # crop_y_start = 400
    # crop_y_end = 900

    # crop_x_start = 700
    # crop_x_end = 780
    # crop_y_start = 500
    # crop_y_end = 580

    crop_x_start = 740
    crop_x_end = 745
    crop_y_start = 540
    crop_y_end = 545
    crop_width = crop_x_end - crop_x_start
    crop_height = crop_y_end - crop_y_start

    def __init__(self):
        super(ScreenScanner, self).__init__()
        self.threshold = 0
        self.load_time_total = 0
        self.load_start_time = 0
        self.debug_frame_count = 0
        self.debug_start_time = time.perf_counter_ns()

    def get_black_cropped(self):
        return np.zeros((self.crop_y_end - self.crop_y_start, self.crop_x_end - self.crop_x_start, 3), np.uint8)

    def get_next_frame_cropped(self):
        # https://stackoverflow.com/questions/1080719/screenshot-an-application-regardless-of-whats-in-front-of-it
        # window_name = "sm-llr.py"
        window_name = "scan this now"
        shell = win32com.client.Dispatch("Wscript.Shell")
        # Returns true if focus given successfully.
        success = shell.AppActivate(window_name)
        if not success:
            raise RuntimeError("Could not give focus to screen capture window.")

        # https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
        hwnd = win32gui.FindWindow(None, window_name)
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.crop_width, self.crop_height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.crop_width, self.crop_height) , dcObj, (self.crop_x_start, self.crop_y_start), win32con.SRCCOPY)

        # DEBUGGING
        bmpfilenamename = "out.bmp"  # set this
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
        # img = Image.open("out.bmp")

        # https://github.com/Toufool/Auto-Split/blob/v1.6.1/src/capture_windows.py
        img: np._BufferType = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype='uint8')
        img.shape = (self.crop_width, self.crop_height, 4)
        # Convert img from 4-bit color depth to 3-bit color depth for future rgb pixel comparisons.
        temp = np.empty((self.crop_width, self.crop_height, 3))
        for x in range(len(img)):
            for y in range(len(img[0])):
                pixel = img[x][y]
                temp[x][y] = (pixel[0], pixel[1], pixel[2])
        img = temp

        # Free resources
        try:
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
        except win32ui.error:
            pass

        self.debug_frame_count += 1
        return (True, img)

    def enter_black_frame(self):
        if self.enter_black_count == 1:
            # We are at the end of the load.
            curr_time = time.perf_counter_ns()
            self.load_time_total += (curr_time - self.load_start_time)
            self.reset_load_vars()
            # Don't add one to enter_black_count, or it will carry over and interfere with the next load screen.
            # DEBUGGING
            self.is_finished = True
            return
        self.enter_black_count += 1

    def exit_black_frame(self):
        if self.enter_black_count == 1:
            self.load_start_time = time.perf_counter_ns()

    def increment_position(self):
        # No need to increment time, as time increments itself naturally according to the laws of physics.
        return

    def get_position(self):
        return round(time.perf_counter_ns() * 1e-9, 2)

    def print_final_load_time(self):
        print("Total load time is:", round(self.load_time_total * 1e-9, 2), "seconds")
        debug_end_time = time.perf_counter_ns()
        fps = self.debug_frame_count / ((debug_end_time - self.debug_start_time) * 1e-9)
        print("FPS is: ", round(fps, 2))