"""Input class contains functions for mouse and keyboard input."""
from classes.window import Window as window
from ctypes import windll
from PIL import Image as image
from PIL import ImageFilter, ImageEnhance, ImageGrab
import numpy as np
import cv2
import datetime
import usersettings as userset
import numpy
import pyautogui
import pytesseract
import re
import time
import os
import win32api
import win32con as wcon
import win32gui
import win32ui


class Inputs():
    """This class handles inputs."""
    

    def click(self, x, y, button="left", fast=False):
        win32gui.ShowWindow(window.id, 5)
        win32gui.SetForegroundWindow(window.id)
        if (button == "left"):
            pyautogui.click(*win32gui.ClientToScreen(window.id, (x, y)))
        
        else:
            pyautogui.click(*win32gui.ClientToScreen(window.id, (x, y)), button="right")
        # Sleep lower than 0.1 might cause issues when clicking in succession
        if fast:
            time.sleep(userset.FAST_SLEEP)
        else:
            time.sleep(userset.MEDIUM_SLEEP)
        
    def click_drag(self, x, y, x2, y2):
        """Click at pixel xy."""
        pyautogui.mouseDown(*win32gui.ClientToScreen(window.id, (x, y)))
        time.sleep(userset.LONG_SLEEP * 2)
        pyautogui.dragTo(*win32gui.ClientToScreen(window.id, (x2, y2)), duration=userset.SHORT_SLEEP)
        pyautogui.mouseUp(*win32gui.ClientToScreen(window.id, (x2, y2)))
        time.sleep(userset.MEDIUM_SLEEP)

    def ctrl_click(self, x, y):
        """Clicks at pixel x, y while simulating the CTRL button to be down."""
        win32gui.ShowWindow(window.id, 5)
        win32gui.SetForegroundWindow(window.id)
        pyautogui.keyDown('ctrl')
        pyautogui.click(*win32gui.ClientToScreen(window.id, (x, y)))
        pyautogui.keyUp('ctrl')
        time.sleep(userset.MEDIUM_SLEEP)

    def send_string(self, string):
        """Send one or multiple characters to the window."""
        win32gui.ShowWindow(window.id, 5)
        win32gui.SetForegroundWindow(window.id)
        if type(string) == float:  # Remove decimal
            string = str(int(string))
        for c in str(string):
            pyautogui.press(c)
        time.sleep(userset.SHORT_SLEEP)

    def get_bitmap(self):
        """Get and return a bitmap of the window."""
        left, top, right, bot = win32gui.GetWindowRect(window.id)
        w = right - left
        h = bot - top
        hwnd_dc = win32gui.GetWindowDC(window.id)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bitmap)
        windll.user32.PrintWindow(window.id, save_dc.GetSafeHdc(), 0)
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)

        # This creates an Image object from Pillow
        bmp = image.frombuffer('RGB',
                               (bmpinfo['bmWidth'],
                                bmpinfo['bmHeight']),
                               bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(window.id, hwnd_dc)
        # bmp.save("asdf.png")
        return bmp

    def pixel_search(self, color, x_start, y_start, x_end, y_end):
        """Find the first pixel with the supplied color within area.

        Function searches per row, left to right. Returns the coordinates of
        first match or None, if nothing is found.

        Color must be supplied in hex.
        """
        bmp = self.get_bitmap()
        width, height = bmp.size
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if y > height or x > width:
                    continue
                t = bmp.getpixel((x, y))
                if (self.rgb_to_hex(t) == color):
                    return x - 8, y - 8

        return None

    def image_search(self, x_start, y_start, x_end, y_end, image, threshold, bmp=None):
        """Search the screen for the supplied picture.

        Returns a tuple with x,y-coordinates, or None if result is below
        the threshold.

        Keyword arguments:
        image -- Filename or path to file that you search for.
        threshold -- The level of fuzziness to use - a perfect match will be
                     close to 1, but probably never 1. In my testing use a
                     value between 0.7-0.95 depending on how strict you wish
                     to be.
        bmp -- a bitmap from the get_bitmap() function, use this if you're
               performing multiple different OCR-readings in succession from
               the same page. This is to avoid to needlessly get the same
               bitmap multiple times. If a bitmap is not passed, the function
               will get the bitmap itself. (default None)
        """
        if not bmp:
            bmp = self.get_bitmap()
        # Bitmaps are created with a 8px border
        search_area = bmp.crop((x_start + 8, y_start + 8,
                                x_end + 8, y_end + 8))
        search_area = numpy.asarray(search_area)
        search_area = cv2.cvtColor(search_area, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(image, 0)
        res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < threshold:
            return None

        return max_loc

    def ocr(self, x_start, y_start, x_end, y_end, debug=False, bmp=None):
        """Perform an OCR of the supplied area, returns a string of the result.

        Keyword arguments:

        debug -- saves an image of what is sent to the OCR (default False)
        bmp -- a bitmap from the get_bitmap() function, use this if you're
               performing multiple different OCR-readings in succession from
               the same page. This is to avoid to needlessly get the same
               bitmap multiple times. If a bitmap is not passed, the function
               will get the bitmap itself. (default None)
        """
        x_start += window.x
        x_end += window.x
        y_start += window.y
        y_end += window.y

        if not bmp:
            bmp = self.get_bitmap()
        # Bitmaps are created with a 8px border
        bmp = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
        *_, right, lower = bmp.getbbox()
        bmp = bmp.resize((right*4, lower*4), image.BICUBIC)  # Resize image
        enhancer = ImageEnhance.Sharpness(bmp)
        bmp = enhancer.enhance(0)
        bmp = bmp.filter(ImageFilter.SHARPEN)  # Sharpen image for better OCR

        if debug:
            bmp.save("debug_ocr.png")
        s = pytesseract.image_to_string(bmp, config='--psm 4')
        return s
        
    def ocrItopod(self, x_start, y_start, x_end, y_end):
        position = win32gui.GetWindowRect(window.id)
        screenshot = ImageGrab.grab(position, False, True)
        screenshot = np.array(screenshot)
        screenshot = screenshot[y_start:y_end, x_start:x_end]
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        width = int(screenshot.shape[1] * 4)
        height = int(screenshot.shape[0] * 4)
        dim = (width, height)
        screenshot = cv2.resize(screenshot, dim, interpolation = cv2.INTER_CUBIC)
        _, img_binarized = cv2.threshold(screenshot, 150, 255, cv2.THRESH_BINARY)
        img = image.fromarray(img_binarized)
        text = pytesseract.image_to_string(img, config='--psm 4 outputbase digits')
        return text

    def get_pixel_color(self, x, y, debug=False):
        """Get the color of selected pixel in HEX."""
        dc = win32gui.GetWindowDC(window.id)
        rgba = win32gui.GetPixel(dc, x + 8 + window.x, y + 8 + window.y)
        win32gui.ReleaseDC(window.id, dc)
        r = rgba & 0xff
        g = rgba >> 8 & 0xff
        b = rgba >> 16 & 0xff

        if debug:
            print(self.rgb_to_hex((r, g, b)))

        return self.rgb_to_hex((r, g, b))

    def check_pixel_color(self, x, y, checks):
        color = self.get_pixel_color(x, y)
        if isinstance(checks, list):
            for check in checks:
                if check == color:
                    return True
        else:
            return color == checks

    def remove_letters(self, s):
        """Remove all non digit characters from string."""
        return re.sub('[^0-9]', '', s)

    def rgb_to_hex(self, tup):
        """Convert RGB value to HEX."""
        return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

    def get_file_path(self, directory, file):
        """Get the absolute path for a file."""
        working = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(working, directory, file)
        return path

    def ocr_number(self, x_1, y_1, x_2, y_2):
        """Remove all non-digits."""
        return int(self.remove_letters(self.ocr(x_1, y_1, x_2, y_2)))

    def ocr_notation(self, x_1, y_1, x_2, y_2):
        """Convert scientific notation from string to int."""
        return int(float(self.ocr(x_1, y_1, x_2, y_2)))

    def save_screenshot(self):
        """Save a screenshot of the game."""
        bmp = self.get_bitmap()
        bmp = bmp.crop((window.x + 8, window.y + 8, window.x + 968, window.y + 608))
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
        bmp.save('screenshots/' + datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S') + '.png')
