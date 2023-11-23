"""
edselinit.py - Define and initialize global variables used by *edsel*.
"""  

import sked as ed

# The top of the frame is always the top of the terminal window, line 1
# flines must always fit within the terminal window.

tlines = 24 # N of lines in terminal window, later update with actual number
tcols = 80  # N of columns in terminal window, later update ...
flines = 20 # N of lines in frame, including all windows.

# From here on, 'window' means the software-generated window within the frame
# whose top line and num. of lines might not be the same as the terminal widow.
# Editing happens in the 'focus window', also called the 'current window'.

# Typical case is just one window that occupies the entire frame
# in that case wintop == 1 and wlines == flines

wintop = 1 # index in frame of top line of focus window
wlines = flines # N of lines in focus window, including status line.
buftop = 1 # index in buffer of line at the wintop, top of the window.
bufname = 'scratch.txt' # name of buffer displayed in focus window

displaying = False  # initially display is not enabled.

# saved windows including focus window, dict of dicts of window items
# windows are identified by integer keys
# saved windows are a dict not a list because smallest key might not be 0
focus = 0 # key of focus window
maxwindows = 2 # for now, the most that are useful in a vertical stack in term.
windows = {}
windows[focus] = { 'wintop': wintop, 'wlines': wlines, 'buftop': buftop,
                   'bufname': ed.bufname, 'dot': ed.dot }
wkeys = [ focus ] # keys of displayed windows, from top to bottom of frame
