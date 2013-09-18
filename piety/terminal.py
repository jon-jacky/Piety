"""
terminal.py - single character input and output from the console

Provides function getchar that reads a single character from the
console (stdin).  Also function putstr that can write a string of
characters (or just one) without formatting (unlike Python print)
so if you want newline you have to explicitly include it in string.

Also provides function setup to put stdin in single-character mode so
getchar returns as soon as a single character is typed (without
waiting for RETURN).  Function restore restores normal line mode (or
whatever was in effect when setup was called).

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

def putstr(s):
    """
    Print string (can be just one character) on console  
     with no formatting (unlike Python print).
    If you want newline, you must explicitly include it in s.
    """
    sys.stdout.write(s)
    sys.stdout.flush() # otherwise s doesn't appear until user types input
