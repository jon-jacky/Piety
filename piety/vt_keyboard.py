"""
vt_keyboard - assign names to ascii, ansi key codes for vt100-style keyboard
  key names here are the same as printed by emacs help: C-h k <key>
  key codes have same meaning in most terminal programs: xterm etc.
"""

import ansi  
import ascii
from ascii import bel, bs, ff, lf, cr, ht, vt, esc, delete

# ASCII
# names on the left are same as in emacs help: C-h k <key>
#  except we use C_h etc instead of C-h, required for Python identifiers
# names on the right are from ASCII standard via std curses.ascii module
C_a = ascii.soh # \x01, ^A
C_b = ascii.stx # \x02, ^B
C_c = ascii.etx # \x03, ^C
C_d = ascii.eot # \x04, ^D
C_e = ascii.enq # \x05, ^E 
C_f = ascii.ack # \x06, ^F
C_g = ascii.bel
C_h = ascii.bs
C_i = ascii.ht 
C_j = ascii.lf
C_k = ascii.vt  # '\v', ^K
C_l = ascii.ff  # '\f', ^L
C_m = ascii.cr  # 
C_n = ascii.so  # \x0E, ^N

C_p = ascii.dle # \x10, ^P

C_u = ascii.nak # \x15, ^U

# ANSI
# names on the left are same as in emacs help: C-h k <key>
# names on the right are from ANSI standard via Wikipedia
up = ansi.cuu
down = ansi.cud
left = ansi.cub
right = ansi.cuf
