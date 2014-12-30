"""
ansi_display - update the display using ansi control sequences
                just the mininum needed by the edd display editor
               also, get display dimensions
"""

import sys
import subprocess # just to get display dimensions

def dimensions():
    'Return nlines, ncols. Works on Mac OS X, probably other Unix.'
    return [ int(n) 
             for n in subprocess.check_output(['stty','size']).split()]
         
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

putstr = sys.stdout.write # print string without newline at end

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
    putstr(ed)

def put_cursor(line, column):      # not in emacs or gnu readline
    putstr(cup % (line, column))

def kill_line():
    'Erase from cursor to end of line'
    putstr(el_end)

def kill_whole_line():
    'Erase entire line'
    putstr(el_all)

def set_scroll(ltop, lbottom): 
    'Set scrolling region to lines ltop through lbottom (line numbers)'
    putstr(decstbm % (ltop, lbottom))

def set_scroll_all():
    'Set scrolling region to entire display'
    putstr(decstbmn)
