"""
ed.py - ed is the standard text editor.  For more explanation see ed.md.

"""

from os.path import isfile, basename

class Buffer(object):
    """
    Text buffer for ed 
    """
    def __init__(self):
        """
        New text buffer
        """
        self.lines = list() # text in the current buffer, a list of strings
        self.dot = None # index of current line dot . in buf().lines
        self.filename = None # filename (string) 
        self.unsaved = False # True if  buffer contains unsaved changes

# Data structures

buffers = dict() # dictionary from buffer names (strings) to buffers

current = None #  name of the current buffer

def buf():
    """
    The current buffer: text and metadata
    """
    return buffers[current] if current in buffers else None

def lines():
    """
    Text in the current buffer: a list of lines
    """
    return buf().lines if current in buffers else None

def o():
    """
    ., index of the current line dot where text is changed/inserted by default
    """
    return buf().dot if current in buffers else None

def S():
    """
    $, index of the last line in the current buffer
    """
    return len(lines()) - 1 if current in buffers else None


# Commands

def B(filename):
    """
    Create a new Buffer and load the file name.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    global buffers, current
    temp = Buffer()
    if isfile(filename):
        fd = open(filename, mode='r')        
        temp.lines = fd.readlines()
        fd.close()
    # if we got this far, readlines must have succeeded
    temp.filename = filename
    nlines = len(temp.lines) # might be 0
    if nlines:
        temp.dot = nlines - 1 # last line
    current = basename(filename)
    buffers[current] = temp
    print '%s, %d lines' % (filename, nlines)


def b(name):
    """
    Set current buffer to name
    """
    global buffer
    if name in buffers:
        current = name
    else:
        print '?'

def D(name):
    """
    Delete buffer named 'name'
    """
    global buffer
    if name in buffers:
        del buffer[name]
    else:
        print '?'    


def n():
    """
    Print buffer names.  Current buffer is marked with
    . (period).  Buffers with unsaved changes are marked with an asterisk.
    Also print ., $,, name and filename of each buffer.
    """
    for n in buffers:
        print '%s %s %d %d %s %s' % \
            ('.' if n == current else ' ',
             '*' if buffers[n].unsaved else ' ',
             buffers[n].dot, 
             len(buffers[n].lines)-1,
             n, buffers[n].filename)

def m():
    """
    Print current line number, .  Also print other status
    information: number of last line $, buffer name current,
    filename.
    """
    print '%d/%d  %s  %s' % (o(),S(), current, buf().filename)

def l(i):
    """
    Move dot to line i and print it. Defaults to .+1,
    the line after dot, so repeatedly invoking l() advances through
    the buffer, printing successive lines. Invoking l(pattern) moves
    dot to the next line that contains pattern, and prints it.
    """
    if i in lines():
        buf().dot = i
        print lines()[i]
    else:
        print '?'
