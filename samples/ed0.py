"""
ed0.py - editor core: data structures and functions used by ed.py

In this API there are no optional or keyword arguments.

There is no error checking, no error messages, and no progress messages.

Line addresses use Python index conventions:
the first line number is 0 and the last line number is number of lines minus 1

Line address ranges use Python slice index conventions: the first line
is at the start index, the last line is at one less than the end index.
"""

import os.path

# data structures

class Buffer(object):
    'Text buffer for ed, a list of lines (strings) and other information'
    def __init__(self):
        'New text buffer'
        self.lines = [] # text in current buffer, a list of strings, each ends in \n
        self.dot = None # index of current line, None when buffer is empty
        self.filename = None # filename (string) 
        self.unsaved = False # True if buffer contains unsaved changes
        self.pattern = '' # search string - default '' matches any line

buffers = dict() # dict from buffer names (strings) to Buffer instances

# There is always a current buffer so we can avoid check for special case
# Start with one empty buffer named 'scratch', can't ever delete it
current = 'scratch'
buffers[current] = Buffer()  

# access to data structures

def buf():
    'Return the current buffer, text and metadata'
    return buffers[current]

def lines():
    'Return text in the current buffer, a list of lines'
    return buf().lines

def o():
    'Return dot (index of the current line), or None if buffer empty'
    return buf().dot

def S():
    'Return number of lines in the current buffer, index of last line + 1'
    return len(lines()) # 0 when buffer is empty

# search, line addresses

def search_buf(forward=True):
    """
    Search for buf().pattern.  Search forward from .+1 to end of buffer
    (or if forward=False, search backward from .-1 to start of buffer)
    If found, return line number.  If not found, return None.
    This version stops at end (or start) of buffer, does not wrap around.
    This verion searches for exact match, not regex match.
    """
    found = False
    slines = lines()[o()+1:] if forward else reversed(lines()[:o()-1])
    for imatch, line in enumerate(slines):
        if buf().pattern in line:
            found = True
            break
    if not found:
        return None
    return o()+1 + imatch if forward else o()-2 - imatch

def search(pattern, fwd=True):
    """
    Update buf().pattern if pattern is nonempty, otherwise retain old pattern
    Search for buf().pattern, return line number where found, dot if not found
    Search forward if fwd is True, backward otherwise
    """
    if pattern:
        buf().pattern = pattern 
    imatch = search_buf(forward=fwd) 
    return imatch if imatch else o()

def f(pattern):
    'Forward search for pattern, return line number where found, o() if not found'
    return search(pattern, fwd=True)

def z(pattern):
    'Backward search for pattern, return line number where found, o() if not found'
    return search(pattern, fwd=False)

# helpers for a(ppend), i(nsert), c(hange), r(ead)

def splitlines(string):
    'Split up string with embedded \n, return list of lines'
    return [ line + '\n' for line in string.split('\n') ]

def insert(iline, lines):
    'Insert lines (list of strings) before iline, update dot to last inserted line'
    buf().lines[iline:iline] = lines # sic, insert lines at this position
    buf().dot = iline + len(lines)-1
    buf().unsaved = True

# files and buffers

def r(iline, filename):
    'Read file contents into buffer after iline'
    if os.path.isfile(filename): 
        fd = open(filename, mode='r')        
        strings = fd.readlines() # each string in lines ends with \n
        fd.close()
        insert(iline+1 if lines() else iline, strings) # like append, below

def b(name):
    'Set current buffer to name.  If no buffer with that name, create one'
    global current
    if name in buffers:
        current = name
    else:
        temp = Buffer()
        buffers[name] = temp
        current = name

def w(name):
    'Write current buffer contents to file name'
    fd = open(name, 'w')
    for line in lines():
        fd.write(line)
    buf().unsaved = False

def D(name):
    'Delete the named buffer'
    global current
    del buffers[name]
    if name == current: # pick a new current buffer
        keys = buffers.keys()
        current = keys[0] if keys else None

# displaying and navigating text

def l(iline):
    'Advance dot to iline and print it'
    buf().dot = iline
    print (lines()[iline]).rstrip() # strip trailing \n

def p(start, end):
    'Print lines from start up to end, leave dot at last line printed'
    for iline in xrange(start,end):
        l(iline)

# adding, changing, and deleting text

def a(iline, string):
    'Append lines from string after iline, update dot to last appended line'
    insert(iline+1 if lines() else iline, splitlines(string)) #empty buf special case

def i(iline, string):
    'Insert lines from string before iline, update dot to last inserted line'
    insert(iline, splitlines(string))

def d(start, end):
    'Delete text from start up to end, set dot to first line after deletes or...'
    buf().lines[start:end] = []
    buf.unsaved = True
    if lines():
        # first line after deletes, or last line in buffer
        buf().dot = min(start,S()-1) # S()-1 if we deleted end of buffer
    else:
        buf().dot = None

def c(start, end, string):
    'Change (replace) lines from start up to end with lines from string'
    d(start,end)
    i(start,string) # original start is now insertion point

def s(start, end, pattern, new, glbl):
    """
    Substitute new for pattern in lines from start up to end.
    When glbl is True (the default), substitute all occurrences in each line,
    otherwise substitute only the first occurrence in each line.
    """
    for i in range(start,end):
        if pattern in lines()[i]: # test to see if we should advance dot
            lines()[i] = lines()[i].replace(pattern,new, -1 if glbl else 1)
            buf().dot = i
            buf().unsaved = True
