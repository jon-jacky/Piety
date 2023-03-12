"""
frameinit.py - Define and initialize global variables used by *frame*.
"""

# The top of the frame is always the top of the terminal window, its line 1
# flines must always fit within the terminal window.

tlines = 24 # N of lines in terminal window, later update with actual number
tcols = 80  # N of columns in terminal window, later update ...
flines = 20 # N of lines in frame, including all windows.

# At this time there is just one window that occupies the entire frame
# so wintop == 1 and wlines == flines always

wintop = 1 # index of first line of window in frame
wlines = flines # N of lines in current window, including status line.
bufname = 'scratch.txt' # name of buffer displayed in current window
buftop = 1 # index in buffer of line displayed at the top of the window.

displaying = False  # initially display is not enabled.
