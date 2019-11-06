"""Window class contains the coordinate for the top left of the game window."""
import win32gui
import ctypes
import platform

class Window():
    """This class contains game window coordinates."""

    id = 0
    x = 0
    y = 0
    dc = 0

    def __init__(self, debug=False):
        """Keyword arguments.

        hwnd -- The window ID
        x -- The x-coordinate for the top left corner of the game window.
        y -- The y-coordinate for the top left corner of the game window.
        """
        if platform.release() == "10":
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        else:
            ctypes.windll.user32.SetProcessDPIAware()

        def window_enumeration_handler(hwnd, top_windows):
            """Add window title and ID to array."""
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        if debug:
            window_name = "debugg"
        else:
            window_name = "NGU Idle" # for Kart, browser, and steam these titles may differ.

        top_windows = []
        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        for i in top_windows:
            #if i[1] != "":
            #    print("Window_name : {0}, id: {1}".format(i[1], i[0]))
			# use this to debug the detected windows
            if window_name == i[1]:
                Window.id = i[0]
        if Window.id == 0:
            raise RuntimeError(f"Couldn't find game window")
            