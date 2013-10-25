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
        self.dot = None # index of current line dot . in lines
        self.filename = None # filename (string) 
        self.unsaved = False # True if  buffer contains unsaved changes

# Data structures

buffers = dict() # dictionary from buffer names (strings) to buffers

current = None #  name of the current buffer, None if no buffers

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
    nlines = len(buf().lines) if current in buffers else None
    return nlines - 1 if nlines else None


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
    # if we got this far, open and readlines must have succeeded
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
    global current
    if name in buffers:
        current = name
    else:
        print '?'

def D(name):
    """
    Delete buffer named 'name'.  What if it's the current buffer
    """
    global buffers
    if name in buffers:
        del buffer[name]
    else:
        print '?'    


def n():
    """
    Print buffer names.  Current buffer is marked with
    . (period).  Buffers with unsaved changes are marked with an asterisk.
    Also print name, ., $, and filename of each buffer.
    """
    for name in buffers:
        # use %s not %d everwhere, dot might be None
        print '%s%s%-12s %6s%6s %s' % \
            ('.' if name == current else ' ',
             '*' if buffers[name].unsaved else ' ',
             name, buffers[name].dot, 
             (len(buffers[name].lines))-1, # $, not N of lines
             buffers[name].filename)

def m():
    """
    Print current line number, .  Also print other status
    information: number of last line $, buffer name current,
    filename.
    """
    # use %s everywhere, not %d - . and $ might be None
    if current in buffers:
        print '%s/%s  %s  %s' % (o(),S(), current, buf().filename)
    else:
        print '?'

def l(*args):
    """
    args is empty or (i), a line
    Move dot to line i and print it. Defaults to .+1,
    the line after dot, so repeatedly invoking l() advances through
    the buffer, printing successive lines. Invoking l(pattern) moves
    dot to the next line that contains pattern, and prints it.
    """
    if args:
        i = args[0]
    else:
        i = o() + 1
    if current in buffers and (0 <= i <= S()):
        buf().dot = i
        print (lines()[i]).rstrip() # strip trailing \n
    else:
        print '?'
