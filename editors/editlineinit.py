"""
editlineinit.py - define and initialize global variables used in editline
"""

line = str() # the line we're editing
point = 0 # index into line

# start_col = 2  # prompt is '> '
start_col = 0    # default, no prompt or other chars at left margin

n_spaces = 4 # Used by tab.  In production maybe assign sked.indent.

yank_buffer = str() # save killed (cut) words here to restore with yank (paste)

prev_fcn = None # some functons behave differently when repeated



