"""
ansi_display - update the display using ansi control sequences
                just the mininum needed by the edd display editor
"""

import sys
import terminal # for putstr

esc = '\x1B' # \e does not work 'invalid \x escape'

csi = esc+'['    # ANSI control sequence introducer
cup = csi+'%d;%dH' # cursor position %d line, %d column
ed  = csi+'J'    # erase display from cursor to end
el  = csi+'%dK'  # erase in line, %d is 0 start, 1 end, or 2 all
el_end = el % 0  # 0: erase from cursor to end of line
el_all = el % 2  # 2: erase entire line
decstbm = csi+'%d;%dr' # DEC Set Top Bottom Margins (set scrolling region)
                       # %d,%d is top, bottom, so 23;24 is bottom two lines
                       # then it sets cursor at the top of the page
decstbmn  = csi+';r' # decstbm default: set scrolling region to full screen

sgr = csi + '%s' + 'm' # set graphic rendition. %s is ;-separated integers like
                 # bold+inverse: esc[0;1;7m by ansi.sgr % ';'.join('017')

# sgr, attribute values
clear = 0      # clears attributes (not transparent!)
white_bg = 47 # gray on mac terminal

def attrs(*attributes):
    """
    Convert variable length arg list of integers to ansi attributes string
    Then the sgr control sequence is just sgr % attrs(*attributes)
    """
    return ';'.join([ str(i) for i in attributes ])

def render(text, *attributes):
    """
    Print text with one or more attributes, each given by separate int arg,
    then clear attributes, but do not print newline.
    """
    # use write not print, we don't want newline or trailing space
    sys.stdout.write(sgr % attrs(*attributes) + text + sgr % attrs(clear))

def erase_display(): # name in gnu readline
    terminal.putstr(ed)

def put_cursor(line, column):      # not in emacs or gnu readline
    terminal.putstr(cup % (line, column))

def kill_line():
    'Erase from cursor to end of line'
    terminal.putstr(el_end)

def kill_whole_line():
    'Erase entire line'
    terminal.putstr(el_all)

def set_scroll(ltop, lbottom): 
    'Set scrolling region to lines ltop through lbottom (line numbers)'
    terminal.putstr(decstbm % (ltop, lbottom))

def set_scroll_all():
    'Set scrolling region to entire display'
    terminal.putstr(decstbmn)
