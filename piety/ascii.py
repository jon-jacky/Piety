"""
ascii.py - ASCII control codes
              http://en.wikipedia.org/wiki/ASCII#ASCII_control_characters
              http://www.inwap.com/pdp10/ansicode.txt
              http://ascii-table.com/control-chars.php
"""

esc = '\x1b'    # escape, ESC
lf  = '\n'      # Line Feed, LF, ^J, '\x0A'
vt  = '\v'      # Vertical Tab, VT, ^K, '\x0B'
delete = '\x7F' # del is a python keyword

# here ca means ctrl-A or ^A

ca = '\x01' # ^A
cb = '\x02' # ^B
cc = '\x03' # ^C
cd = '\x04' # ^D
ce = '\x05' # ^E
cf = '\x06' # ^F
cn = '\x0E' # ^N
cp = '\x10' # ^P
cu = '\x15' # ^U


