"""
terminal.py - functions to set character mode or line mode,
               read/write single char or string

This is a platform-dependent module.  It uses the termios and tty
modules, so it must run on a Unix-like host OS (including Linux and
Mac OS X).  For more about tty and termios see:

http://docs.python.org/2/library/tty.html
http://docs.python.org/2/library/termios.html
http://hg.python.org/cpython/file/1dc925ee441a/Lib/tty.py

http://man7.org/linux/man-pages/man3/termios.3.html

"""

import sys, tty, termios, subprocess # subprocess just for display dimensions

def dimensions():
    'Return nlines, ncols. Works on Mac OS X, probably other Unix.'
    return [ int(n) 
             for n in subprocess.check_output(['stty','size']).split()]

fd = sys.stdin.fileno() # Isn't sys.stdin always fileno 0 ?
line_mode_settings = termios.tcgetattr(fd) # in case someone calls restore first

# ...$ python
# >>> import terminal
# >>> terminal.line_mode_settings
# [27394, 3, 19200, 536872395, 9600, 9600, ['\x04', '\xff', '\xff', '\x7f', '\x17', '\x15', '\x12', '\xff', '\x03', '\x1c', '\x1a', '\x19', '\x11', '\x13', '\x16', '\x0f', '\x01', '\x00', '\x14', '\xff']]

def set_char_mode():
    """
    set sys.input to single character mode, save original mode
    """
    # DON'T save settings again - we alread saved them on import, see above
    #  this function should be idempotent.
    #global saved_settings
    #saved_settings = termios.tcgetattr(fd)
    # tty.setraw just calls termios.tcsetattr with particular flags
    # see http://hg.python.org/cpython/file/1dc925ee441a/Lib/tty.py
    tty.setraw(fd)


def set_line_mode():
    """
    restore sys.input to line mode
    """
    termios.tcsetattr(fd, termios.TCSAFLUSH, line_mode_settings)

def getchar():
    """
    Get a single character from console keyboard, without waiting for RETURN
    """
    return sys.stdin.read(1)

def getchars(n):
    """
    Get up to n characters from console keyboard, without waiting for RETURN
    """
    return sys.stdin.read(n)

def putstr(s):
    """
    Print string (can be just one character) on console with no
    formatting (unlike Python print).  Flush to force output immediately.  
    If you want newline, you must explicitly include it in s.
    """
    sys.stdout.write(s)
    sys.stdout.flush() # otherwise s doesn't appear until user types input

# Test

def main():
    c = line = ''
    set_char_mode() # enter single character more
    putstr('> ')
    while not c == '\r':
        c = getchar()
        putstr(c)
        line += c
    set_line_mode() # return to normal mode
    print
    print line

if __name__ == '__main__':
    main()
