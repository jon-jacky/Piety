"""
ansi_keyboard.py - ASCII and ANSI control codes for keyboard

ASCII control codes
 http://en.wikipedia.org/wiki/ASCII#ASCII_control_characters
 http://www.inwap.com/pdp10/ansicode.txt
 http://ascii-table.com/control-chars.php

ANSI control sequences, Best explanation at:
 http://www.inwap.com/pdp10/ansicode.txt.  
 especially section "Minimum requirements for VT100 emulation"
See also:
 http://en.wikipedia.org/wiki/ANSI_escape_code
 http://invisible-island.net/xterm/ctlseqs/ctlseqs.html
This page says 'Line and column numbers start at 1':
 http://www.umich.edu/~archive/apple2/misc/programmers/vt100.codes.txt
"""

# ASCII codes for control characters

bel = '\a'   # bell
bs  = '\b'   # backspace 
cr  = '\r'   # carriage return

delete = '\x7F' # del is a python keyword
C_c = '\x03' # ^C, etx
C_d = '\x04' # ^D, eot
C_j = '\n'   # ^J, lf
C_l = '\f'   # ^L, ff
C_n = '\x0E' # ^N, so
C_p = '\x10' # ^P, dle
C_u = '\x15' # ^U, nak

# ANSI codes for arrow keys

esc = '\x1B'  # \e does not work 'invalid \x escape'
csi = esc+'[' # ANSI control sequence introducer

up = csi+'A'  # cursor up, default 1 char
down = csi+'B'  # cursor down, default 1 char

