"""
editlineinit.py - define and initialize global variables used in editline
"""

# line = str() # string being edited # NOW THIS IS A PASSED PARAMETER

point = 0 # index into line (above), string being edited

killed = str() # saved killed (cut) words, can be restored with yank (paste)

start_col = 0    # default, no prompt or other chars at left margin
# start_col = 2  # when prompt is '> ' for example

n_spaces = 4 # Used by tab.  In production maybe assign sked.indent.

prev_cmd = None # some functons behave differently when repeated



