"""
editlineinit.py - define and initialize global variables used in editline
"""

# For testing
line = str() # immutable

# For testing
buffer = [ str() ] # mutable
dot = 0 # index into buffer

point = 0 # index into string being edited: line or buffer[dot]

start_col = 0    # default, no prompt or other chars at left margin
# start_col = 2  # when prompt is '> ' for example

n_spaces = 4 # Used by tab.  In production maybe assign sked.indent.

yank_buffer = str() # save killed (cut) words here to restore with yank (paste)

prev_fcn = None # some functons behave differently when repeated



