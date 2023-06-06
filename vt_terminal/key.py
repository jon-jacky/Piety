"""
key.py - ASCII and ANSI control codes for the terminal keyboard

ASCII control codes
 http://en.wikipedia.org/wiki/ASCII#ASCII_control_characters
 http://www.inwap.com/pdp10/ansicode.txt
 http://ascii-table.com/control-chars.php

ANSI control sequences, Best explanation at:
 http://www.inwap.com/pdp10/ansicode.txt.  
 especially section "Minimum requirements for VT100 emulation"
See also:
 http://vt100.net/
 http://en.wikipedia.org/wiki/ANSI_escape_code
 https://en.wikipedia.org/wiki/C0_and_C1_control_codes
 http://invisible-island.net/xterm/ctlseqs/ctlseqs.html (also dirs above)
This page says 'Line and column numbers start at 1':
 http://www.umich.edu/~archive/apple2/misc/programmers/vt100.codes.txt

"""

# Names of characters

space = ' '

# ASCII codes for control characters

bel = '\a'   # bell, ^G
bs  = '\b'   # backspace, ^H
cr  = '\r'   # carriage return, ^M
htab = '\t'  # horizontal tab, ^I

delete = '\x7F' # del is a python keyword, ^?

C_at = '\x00' # ^@, nul, also obtained by ^space on many terminals
C_a = '\x01' # ^A, soh
C_b = '\x02' # ^B, stx
C_c = '\x03' # ^C, etx
C_d = '\x04' # ^D, eot
C_e = '\x05' # ^E, enq
C_f = '\x06' # ^F, ack
C_g = '\a'   # ^G, bel
C_h = '\b'   # ^H, bs
C_i = '\t'   # ^I, ht
C_j = '\n'   # ^J, lf
C_k = '\v'   # ^K, vt
C_l = '\f'   # ^L, ff
C_m = '\r'   # ^M, cr
C_n = '\x0E' # ^N, so
C_o = '\x0F' # ^O, si
C_p = '\x10' # ^P, dle
C_q = '\x11' # ^Q, dc1, xon
C_r = '\x12' # ^R, dc2
C_s = '\x13' # ^S, dc3, xoff
C_t = '\x14' # ^T, dc4
C_u = '\x15' # ^U, nak
C_v = '\x16' # ^V, syn
C_w = '\x17' # ^W, etb
C_x = '\x18' # ^X, can
C_y = '\x19' # ^Y, em
C_z = '\x1a' # ^Z, sub
C_space = '\x99' # placeholder for'\x0' # ^space, alias for ^@, nul

# Define Meta keys, prefixed with esc

esc = '\x1B'  # \e does not work 'invalid \x escape'

M_a = esc + 'a'
M_b = esc + 'b'
M_c = esc + 'c'
M_d = esc + 'd'
M_e = esc + 'e'
M_f = esc + 'f'
M_g = esc + 'g'
M_h = esc + 'h'
M_i = esc + 'i'
M_j = esc + 'j'
M_k = esc + 'k'
M_l = esc + 'l'
M_m = esc + 'm'
M_n = esc + 'n'
M_o = esc + 'o'
M_p = esc + 'p'
M_q = esc + 'q'
M_r = esc + 'r'
M_s = esc + 's'
M_t = esc + 't'
M_u = esc + 'u'
M_v = esc + 'v'
M_w = esc + 'w'
M_x = esc + 'x'
M_y = esc + 'y'
M_z = esc + 'z'

M_lt = esc + '<'
M_gt = esc + '>'

M_percent = esc + '%'

# ANSI codes for arrow keys

csi = esc+'[' # ANSI control sequence introducer

up =    csi+'A'  # cursor up, default 1 char
down =  csi+'B'  # cursor down, default 1 char
right = csi+'C'  # cursor forward (right), default 1 char
left =  csi+'D'  # cursor backward (left), default 1 char

