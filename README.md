# Disclaimer about this fork
This fork was created by me, mostly to try and get the guffin script running in steam/kart versions. i do *not* actively update this fork, and i do *not* guarantee any scripts to work as intended. This fork is a straight up upload of my messy edited guffin script, which works for *my* goals. some experience with python is recommended, so you can have the scripts do as you please.
I highly recommend you to make saves of you game before running any scripts, and also to use a virtualenv for your python.
The main benefit of this fork is that the backend Inputs and window classes work with proper pyautoGUI implementation.

# About
This is a collection of functions I created for AHK and Python with the purpose of automating different aspects of the game [NGU-IDLE](https://www.kongregate.com/games/somethingggg/ngu-idle). This project first started because the built-in functions ControlClick/ControlSend in AHK did not work with the game, because of how Unity handles input. I first created replacements for these functions in AHK, but later moved over to Python because there was little reason to use AHK when the input was being sent directly via the Windows API.

### Features
These functions will send input to the game without using your keyboard or mouse, and they don't require the window to be active. The supplied functions found in [AHK](/AHK) or [functions.py](/Python/functions.py) can help you create your own scripts to run. You can also see my implementations in the [main.py](/Python/Scripts/main.py) file for inspiration of what you can do. This file changes as I progress myself and should only be used as a base for your own creations, check the blame as well for even further inspiration!

### Disclaimer
If you're automating the game using these or any other scripts, please consider disabling the high score submissions in the game settings.

The AHK script is unsupported and deleted, but I kept the functions here because they will work well in any Unity based browser game, where AHK's builtins fall short. 

**Kartridge and steam versions do not support background clicking**

## Requirements
* Windows 7 or later (NT >=6.1)
* Python 3 (only tested on 3.7)
* Tesseract OCR
* Use scientific notation in game
* The "simple inventory shortcuts" setting must be enabled
* The normal theme must be enabled
* Fancy titan HP bars must be disabled if using the ``kill_titan()`` method
* If you plan on using wishes/R3 I strongly recommend you to name your R3 to 'R' and use the green background, otherwise you will get spotty results from Tesseract. It's also strongly recommended to have 50 speed in all 3 resources.

## Installation
Install Python dependencies using [pip](https://pip.pypa.io/en/stable/quickstart/):
```
pip install -r requirements.txt
```
Install [Tesseract](https://github.com/tesseract-ocr/tesseract/releases) and add it to your [PATH variable](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/).

Remember to restart your command prompt/IDE after changing your environment variables.

Change the settings in ``usersettings_example.py`` and rename it to ``usersettings.py``

### Big Monitors
If you are using a big monitor (4K, 8K) or by some reason your Windows scaling is set to something other than 100%, the scripts won't work.
To solve this, on Firefox go to ```about:config``` and set ```layout.css.devPixelsPerPx``` to ```1.0```.

## FAQ
* Q: I get a ``ValueError``.

You're probably trying to cast a result from `ocr()`, that returns a string which might be empty or contain non-numeric characters. Use [try/except](https://docs.python.org/3/tutorial/errors.html#handling-exceptions) to handle this appropriately.

* Q: I get a ``IndexError: image index out of range`` error from ``pixel_search()``.

You're either sending invalid coordinates to the function, or the ``Window()`` class contains invalid offsets. You can debug this by printing ``Window.x`` and ``Window.y``, and you can also make the ``get_bitmap()`` function save the bitmap to disk in order to see what the script can see. This error usually occurs because the script has found the wrong window (it searches for `play ngu idle` in the window title) if you have multiple game sessions running it might not use the correct one. This error will also occur if you lock the computer screen, or if Windows put your monitors to sleep due to power settings. This can be changed in your power settings in Windows. However if you're using DisplayPort and you physically turn your monitors off, Windows might change the desktop resolution for some reason, causing the script to crash. If this is causing problems, there's a fix [here](https://answers.microsoft.com/en-us/windows/forum/windows_7-hardware/windows-7-movesresizes-windows-on-monitor-power/1653aafb-848b-464a-8c69-1a68fbd106aa).

* Q: I get a ``TypeError: cannot unpack non-iterable NoneType object`` error from ``pixel_search()``.

Make sure you have the game running in Firefox, and that the window is NOT minimized, you cannot minimize the window while running, but you can have other windows on top of the game window just fine. This error will also occur if you lock the computer screen, or if Windows put your monitors to sleep due to power settings. See answer above if you're using DisplayPort.
This can also happen on big monitors, as the search area might be too little. Try changing the script to ```pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 2000, 1000)``` instead. Note that reducing Firefox windows size can make this search area be out of bounds and throw an error.

* Q: I get a ``pywintypes.error: (0, 'GetPixel', 'No error message is available')`` error.

This can happen for various reasons, see answers above because they all apply to this. Some full-screen games have been reportedly causing this, also video card driver crashes will cause this error as well.
