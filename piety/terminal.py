"""
terminal.py - single character input and output from the console

Has a main method, python terminal.py demonstrates most functions.

Provides function getchar that reads a single character from the
console (stdin).  Also function putstr that can write a string of
characters (or just one) without formatting (unlike Python print), so
if you want newline you have to explicitly include it in the string.

Also provides function setup to put stdin in single-character mode so
getchar returns as soon as a single character is typed (without
waiting for RETURN).  Function restore restores normal line mode (or
whatever was in effect when setup was called).

Terminal settings assigned by this module apply to all tasks
(including all Console instances) in the Piety session, because Piety
runs in a single Python interpreter session.

This is a platform-dependent module.  It uses the termios and tty
modules, so it must run on a Unix-like host OS (including Linux and
Mac OS X).  For more about tty and termios see:

http://docs.python.org/2/library/tty.html
http://docs.python.org/2/library/termios.html
http://hg.python.org/cpython/file/1dc925ee441a/Lib/tty.py

http://man7.org/linux/man-pages/man3/termios.3.html

"""

import sys, tty, termios

fd = sys.stdin.fileno() # Isn't sys.stdin always fileno 0 ?
saved_settings = termios.tcgetattr(fd) # in case someone calls restore first

def setup():
    """
    set sys.input to single character mode, save original mode
    """
    global saved_settings
    saved_settings = termios.tcgetattr(fd)
    # tty.setraw just calls termios.tcsetattr with particular flags
    # see http://hg.python.org/cpython/file/1dc925ee441a/Lib/tty.py
    tty.setraw(fd)


def restore():
    """
    restore sys.input to original mode saved by setup
    """
    termios.tcsetattr(fd, termios.TCSAFLUSH, saved_settings)

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
    Print string (can be just one character) on console  
     with no formatting (unlike Python print).
    If you want newline, you must explicitly include it in s.
    """
    sys.stdout.write(s)
    sys.stdout.flush() # otherwise s doesn't appear until user types input

# Test

def main():
    c = line = ''
    setup() # enter single character more
    putstr('> ')
    while not c == '\r':
        c = getchar()
        putstr(c)
        line += c
    restore() # return to normal mode
    print
    print line

if __name__ == '__main__':
    main()
