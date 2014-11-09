"""
ascii.py - ASCII control codes
              http://en.wikipedia.org/wiki/ASCII#ASCII_control_characters
              http://www.inwap.com/pdp10/ansicode.txt
              http://ascii-table.com/control-chars.php

https://docs.python.org/2/library/curses.ascii.html is not helpful
 it defines integers SOH etc. not characters
"""
                                                
# names from ASCII standard via Wikipedia, ref above

# these already have Python escape codes
bel = '\a'   # bell
bs  = '\b'   # backspace 
ff  = '\f'   # form feed
lf  = '\n'   # line feed
cr  = '\r'   # carriage return
ht  = '\t'   # horizontal tab
vt  = '\v'   # vertical tab

soh = '\x01' # ^A
stx = '\x02' # ^B
etx = '\x03' # ^C
eot = '\x04' # ^D
enq = '\x05' # ^E
ack = '\x06' # ^F                    

# bel = x07, ^G, \a, defined above
# bs =  x08, ^H, \b
# ht =  x09, ^I, \t
# lf =  xOA, ^J, \n
# vt =  xOB, ^K, \v
# ff =  xOC, ^L, \f
# cr =  x0D, ^M, \r

so  = '\x0E' # ^N
dle = '\x10' # ^P
nak = '\x15' # ^U
esc = '\x1B' # \e does not work 'invalid \x escape'

delete = '\x7F' # del is a python keyword
