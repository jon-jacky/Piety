"""
ansi.py - ANSI terminal control codes, see urwid/escape.py also
           http://en.wikipedia.org/wiki/ANSI_escape_code
           http://www.inwap.com/pdp10/ansicode.txt
           http://ascii-table.com/ansi-escape-sequences.php
           http://www.sweger.com/ansiplus/EscSeq.html
           http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
"""

from ascii import esc

csi = esc+'['  # control sequence introducer

cuf = csi+'%dC'  # cursor forward %d characters
cub = csi+'%dD'  # cursor backward %d characters
cha = csi+'%dG'  # cursor horizontal absolute, column %d

ich = csi+'%d@'  # insert chars, make room for %d chars at current position
dch = csi+'%dP'  # delete chars, remove %d chars at current position

el  = csi+'%dK'  # erase in line, %d 0: erase from cursor to end of line
                 #                %d 1: erase from start of line to cursor
                 #                %d 2: erase entire line
