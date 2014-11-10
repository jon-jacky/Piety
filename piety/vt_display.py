"""
vt_display - Assign names to ansi control sequences for vt100-style display.
  These definitions also work in most terminal programs: xterm etc.
  Names here are the same as command names used by emacs, when possible.
"""

import sys
import ansi
from ansi import render, white_bg, clear # clients expect these 
import terminal

# Throughout, use terminal.putstr which also calls sys.stdout.flush
 
# cursor positioning

def put_cursor(line, column):      # not in emacs or gnu readline
    terminal.putstr(ansi.cup % (line, column))

def move_to_column(column):
    terminal.putstr(ansi.cha % column)

def forward_char():
    terminal.putstr(ansi.cuf) # move just one char

def backward_char():
    terminal.putstr(ansi.cub)

def move_beginning_of_line():
    terminal.putstr(ansi.cha % 1)

#def move_end_of_line():
#   terminal.putstr(ansi.cha % eol) # just use move_to_column

# insertion

def self_insert_char(key):
    'Insert character in front of cursor'
    terminal.putstr((ansi.ich % 1) + key) # open space to insert char

# deletion

def delete_char():
    'Delete character under the cursor'
    terminal.putstr(ansi.dch % 1)

def backward_delete_char():
    'Delete character before cursor'
    terminal.putstr(ansi.cub + ansi.dch % 1)

def kill_line():
    'Erase from cursor to end of line'
    terminal.putstr(ansi.el_end)

def kill_whole_line():
    'Erase entire line'
    terminal.putstr(ansi.el_all)

def erase_display(): # name in gnu readline
    terminal.putstr(ansi.ed)

# scrolling - not in emacs or gnu readline

def set_scroll(ltop, lbottom): 
    'Set scrolling region to lines ltop through lbottom (line numbers)'
    terminal.putstr(ansi.decstbm % (ltop, lbottom))

def set_scroll_all():
    'Set scrolling region to entire display'
    terminal.putstr(ansi.decstbmn)
