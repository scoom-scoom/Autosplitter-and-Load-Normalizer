import numpy as np
import win32gui
import win32ui
import win32com.client
import win32con

from PIL import Image

# https://stackoverflow.com/questions/1080719/screenshot-an-application-regardless-of-whats-in-front-of-it
# window_name = "scan this now"
window_name = "NG+ 26 - &"
shell = win32com.client.Dispatch("Wscript.Shell")
# Returns true if focus given successfully.
success = shell.AppActivate(window_name)

# https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
w = 1920 # set this
h = 1080 # set this
bmpfilenamename = "out.bmp" # set this

hwnd = win32gui.FindWindow(None, window_name)
wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
cDC.SelectObject(dataBitMap)
cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

# dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
# img = Image.open("out.bmp")

# https://github.com/Toufool/Auto-Split/blob/v1.6.1/src/capture_windows.py
img: np._BufferType = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype='uint8')
img.shape = (h, w, 4)
# arr = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype='uint8')
# img = arr.shape(h, w, 4)

# Free Resources
try:
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
except win32ui.error:
    pass