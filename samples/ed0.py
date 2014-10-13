"""
ed0.py - editor core: data structures and functions used by ed.py

In this module each function has a fixed (positional) argument list,
provides no error checking, and no error messages or progress
messages.  It has no print statements, and does not read or write at
the console.  This module updates buffers and reads and writes files.

This API uses the classic Unix ed conventions for indexing and range
(which are unlike Python): The index of the first line is 1, the index
of the last line is the same as the number of lines (the length of the
buffer in lines), and range i,j includes the last line with index j
(so the range i,i is just the line i, but it is not empty).
"""

import os.path

# data structures

class Buffer(object):
    'Text buffer for ed, a list of lines (strings) and metadata'
    def __init__(self):
        'New text buffer'
        # Buffer always contains empty line at index 0, never used or printed
        self.lines = [''] # text in current buffer, a list of strings
        self.dot = 0 # index of current line, 0 when buffer is empty
        self.filename = None # filename (string) 
        self.unsaved = False # True if buffer contains unsaved changes
        self.pattern = '' # search string - default '' matches any line
        self.npage = 22 # page length used, optionally set by z scroll command

buffers = dict() # dict from buffer names (strings) to Buffer instances

# There is always a current buffer so we can avoid check for special case
# Start with one empty buffer named 'main', can't ever delete it
current = 'main'
buffers[current] = Buffer()  

# access to data structures

def bufname():
    'Return current buffer name'
    return current

def buffer(bufname):
    'Return buffer identified by bufname'
    return buffers[bufname]

def buf():
    'Return the current buffer, text and metadata'
    return buffers[current]

def lines():
    """Return text in the current buffer: list of lines (strings)
    list of lines is never empty, there is always an empty line 0.
    Each line is a string terminated with \n, as returned by Python readlines()."""
    return buf().lines

def o():
    'Return index of the current line (called dot), 0 if the buffer is empty'
    return buf().dot

def S():
    'Return index of the last line, 0 if the buffer is empty'
    return len(lines())-1 # don't count empty first line at index 0

# defaults and range checking are done in this module 
# because they depend on indexing and range conventions

def mk_start(start):
    'Return start if given, else default dot, 0 if buffer is empty'
    return start if start != None else o()

def mk_range(start, end):
    'Return start, end if given, else return defaults, calc default end from start'
    istart = mk_start(start)
    return istart, end if end != None else istart

def start_ok(iline):
    """Return True if iline address is in buffer, always False for empty buffer
    Used by most commands, which don't make sense for an empty buffer"""
    return (0 < iline <= S()) 

def start_empty_ok(iline):
    """Return True if iline address is in buffer, or iline is 0 for start of buffer
    Used by commands which make sense for an empty buffer: insert, append, read"""
    return (0 <= iline <= S())

def range_ok(start, end):
    'Return True if start and end are in buffer, and start does not follow end'
    return start_ok(start) and start_ok(end) and start <= end

# search, line addresses

def search_buf(forward):
    """Search for buf().pattern.  Search forward from .+1 to end of buffer
    (or if forward is False, search backward from .-1 to start of buffer)
    If found, return line number.  If not found, return None.
    This version stops at end (or start) of buffer, does not wrap around.
    This version searches for exact match, not regex match."""
    found = False
    slines = lines()[o()+1:] if forward else reversed(lines()[:o()-1])
    for imatch, line in enumerate(slines):
        if buf().pattern in line:
            found = True
            break
    if not found:
        return None
    return o()+1 + imatch if forward else o()-2 - imatch

def search(pattern, forward):
    """Update buf().pattern if pattern is nonempty, otherwise retain old pattern
    Search for buf().pattern, return line number where found, dot if not found
    Search forward if forward is True, backward otherwise."""
    if pattern:
        buf().pattern = pattern 
    imatch = search_buf(forward)
    return imatch if imatch else o()

def F(pattern):
    'Forward Search for pattern, return line number where found, o() if not found'
    return search(pattern, True)

def R(pattern):
    'Backward search for pattern, return line number where found, o() if not found'
    return search(pattern, False)

# helpers for a(ppend), i(nsert), c(hange), r(ead)

def insert(iline, lines):
    'Insert lines (list of strings) before iline,update dot to last inserted line'
    buf().lines[iline:iline] = lines # sic, insert lines at this position
    buf().dot = iline + len(lines)-1
    buf().unsaved = True # usually the right thing but ed.B and E override it.

# files and buffers

def f(filename):
    'set default filename for current buffer'
    buf().filename = filename

def r(iline, filename):
    'Read file contents into buffer after iline'
    if os.path.isfile(filename): 
        fd = open(filename, mode='r')        
        # fd.readlines reads file into a list of strings, one per line
        strings = fd.readlines() # each string in lines ends with \n
        fd.close()
        insert(iline+1, strings) # like append, below

def b(name):
    'Set current buffer to name.  If no buffer with that name, create one'
    global current
    if name in buffers:
        current = name
        return
    b_new(name)

def b_new(name):
    'Create buffer with given name. Replace any existing buffer with same name'
    global current
    temp = Buffer()
    buffers[name] = temp # replace buffers[name] if it already exists
    current = name

def r_new(buffername, filename):
    'Create new buffer, Read in file contents'
    b_new(buffername)
    buf().filename = filename
    r(0, filename)
    buf().unsaved = False # insert in r sets unsaved = True, this is exception

def w(name):
    'Write current buffer contents to file name'
    fd = open(name, 'w')
    for line in lines()[1:]: # don't print empty line 0
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
    'Advance dot to iline and return it (so caller can print it)'
    buf().dot = iline
    return (lines()[iline]).rstrip() # strip trailing \n

# adding, changing, and deleting text

def a(iline, string):
    'Append lines from string after iline, update dot to last appended line'
    # string is one big str with linebreaks indicated by embedded \n
    # splitlines(True) breaks at \n to make list of strings
    # keepends True arg keeps each trailing \n, same convention as fd.readlines()
    insert(iline+1, string.splitlines(True))

def i(iline, string):
    'Insert lines from string before iline, update dot to last inserted line'
    # iline at initial empty line with index 0 is a special case, append instead
    insert(iline if iline else iline+1, string.splitlines(True))

def d(start, end):
    'Delete text from start up to end, set dot to first line after deletes or...'
    buf().lines[start:end+1] = [] # classic ed range is inclusive, unlike Python
    buf.unsaved = True
    if lines()[1:]: # retain empty line 0
        # first line after deletes, or last line in buffer
        buf().dot = min(start,S()) # S() if we deleted end of buffer
    else:
        buf().dot = 0

def c(start, end, string):
    'Change (replace) lines from start up to end with lines from string'
    d(start,end)
    i(start,string) # original start is now insertion point

def s(start, end, old, new, glbl):
    """Substitute new for old in lines from start up to end.
    When glbl is True, substitute all occurrences in each line,
    otherwise substitute only the first occurrence in each line."""
    for i in range(start,end+1): # classic ed range is inclusive, unlike Python
        if old in lines()[i]: # test to see if we should advance dot
            lines()[i] = lines()[i].replace(old,new, -1 if glbl else 1)
            buf().dot = i
            buf().unsaved = True
