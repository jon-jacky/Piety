"""
vt_display - Assign names to ansi control sequences for vt100-style display.
  These definitions also work in most terminal programs: xterm etc.
  Names here are the same as command names used by emacs, when possible.
"""

import sys
import ansi

# FIXME? Here we have sys.stdout.write throughout.
# Do we need terminal.putstr which also calls sys.stdout.flush?
 
# cursor positioning

def put_cursor(line, column):      # not in emacs or gnu readline
    sys.stdout.write(ansi.cup % (line, column))

def move_to_column(column):
    sys.stdout.write(ansi.cha % column)

def forward_char():
    sys.stdout.write(ansi.cuf) # move just one char

def backward_char():
    sys.stdout.write(ansi.cub)

def move_beginning_of_line():
    sys.stdout.write(ansi.cha % 1)

#def move_end_of_line():
#   sys.stdout.write(ansi.cha % eol) # just use move_to_column

# insertion

def self_insert_char(key):
    'Insert character in front of cursor'
    sys.stdout.write(ansi.ich % 1) # open space to insert char
    sys.stdout.write(key)

# deletion

def delete_char():
    'Delete character under the cursor'
    sys.stdout.write(ansi.dch % 1)

def backward_delete_char():
    'Delete character before cursor'
    sys.stdout.write(ansi.cub)
    sys.stdout.write(ansi.dch % 1)

def kill_line():
    'Erase from cursor to end of line'
    sys.stdout.write(ansi.el_end)

def kill_whole_line():
    'Erase entire line'
    sys.stdout.write(ansi.el_all)

def erase_display(): # name in gnu readline
    sys.stdout.write(ansi.ed)

# scrolling - not in emacs or gnu readline

def set_scroll(ltop, lbottom): 
    'Set scrolling region to lines ltop through lbottom (line numbers)'
    sys.stdout.write(ansi.decstbm % (ltop, lbottom))

def set_scroll_all():
    'Set scrolling region to entire display'
    sys.stdout.write(ansi.decstbmn)
