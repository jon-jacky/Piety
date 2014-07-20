"""
ansi.py - ANSI terminal control codes.  Best explanation at:
           http://www.inwap.com/pdp10/ansicode.txt.  
          See also:
           http://en.wikipedia.org/wiki/ANSI_escape_code
           http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
          Other pages with the same information in different formats:
           http://ascii-table.com/ansi-escape-sequences.php
           http://www.sweger.com/ansiplus/EscSeq.html
"""

import re
from ascii import esc

csi = esc+'['    # control sequence introducer

# Inputs: arrow keys
up    = csi+'A'
down  = csi+'B'
right = csi+'C'
left  = csi+'D'

# Outputs with parameters

cuf = csi+'%dC'  # cursor forward %d characters
cub = csi+'%dD'  # cursor backward %d characters
cha = csi+'%dG'  # cursor horizontal absolute, column %d
cup = csi+'%d;%dH' # cursor to line, column

ich = csi+'%d@'  # insert chars, make room for %d chars at current position
dch = csi+'%dP'  # delete chars, remove %d chars at current position

el  = csi+'%dK'  # erase in line, %d 0: erase from cursor to end of line
                 #                %d 1: erase from start of line to cursor
                 #                %d 2: erase entire line

decstbm = csi+'%d;%dr' # DEC Set Top Bottom Margins (set scrolling region)
                       # %d,%d is top, bottom, 23;24 is bottom two lines
                       # then it sets cursor at the top of the page

decstbm_all  = csi+';r' # decstbm default: set scrolling region to full window

# regex from https://github.com/helgefmi/ansiterm/blob/master/ansiterm.py 
ctlseq = re.compile(r'^\x1b\[?([\d;]*)(\w)')
