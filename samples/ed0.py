"""
ed0.py - editor core

In this API there are no optional or keyword arguments.

There is no error checking, no error messages, and no progress messages.

Numeric line addresses use Python numbering conventions:
the first line is number 0 and the last line number is length-1.

Ranges use Python slice conventions: the first element is at the
start index, the last element is at one less than the end index.
"""

# data structures

class Buffer(object):
    'Text buffer for ed'
    def __init__(self):
        'New text buffer'
        self.lines = [] # text in the current buffer, a list of strings
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
    'Return . (dot), index of the current line, None if buffer empty'
    return buf().dot

def S():
    'Return number of lines in the current buffer, index of last line + 1'
    return len(lines()) # 0 when buffer is empty

# search

def search(forward=True):
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

def f_cmd(pattern, fwd=True):
    """
    Update buf().pattern if pattern is nonempty, otherwise retain old pattern
    Search for pattern, return line number where found, o() if not found
    Search forward if fwd is True, backward otherwise
    """
    if pattern:
        buf().pattern = pattern 
    imatch = search(forward=fwd) 
    return imatch if imatch else o()

def f(pattern):
    'Forward search for pattern, return line number where found, o() if not found'
    return f_cmd(pattern, fwd=True)

def z(pattern):
    'Backward search for pattern, return line number where found, o() if not found'
    return f_cmd(pattern, fwd=False)

# helper for ed commands a, i, c, r

def addlines(f, iline, string):
    """
    append or insert string (maybe multiple lines separated by \n)
    in current buffer at iline, used by function f, which might be a, c, i, r
    """
    # FIXME don't pass in f, there are really just two cases, use a boolean
    newlines = [ line + '\n' for line in string.split('\n') ]
    # empty buffer when not lines() is a special case for append
    start = iline if (f == i or not lines()) else iline+1 # insert else append
    end = start # sic, insert newlines at this position
    buf().lines[start:end] = newlines
    buf().dot = start + len(newlines)-1
    buf().unsaved = True

# working with files and buffers

def r(iline, filename):
    """
    read file contents into buffer after iline
    """
    fd = open(filename, mode='r')        
    lines = fd.readlines()
    fd.close()
    addlines(a, iline, lines) # a for append. Also updates dot, unsaved
    nlines = len(lines)

def b(name):
    'Set current buffer to name.  If no buffer with that name, create one'
    global current
    if name in buffers:
        current = name
    else:
        temp = Buffer()
        buffers[name] = temp
        current = name

def B(filename):
    'Create a new buffer and load the named file'
    b(basename(filename)) # create buffer, make it current
    buf().filename = filename
    r(0, filename) # now new buffer is current, append at line 0

def w(name):
    'Write current buffer contents to file name'
    fd = open(name, 'w')
    for line in lines():
        fd.write(line)
    buf().unsaved = False

def D(name):
    'Delete the named buffer'
    del buffers[name]

# displaying and navigating text

def l(iline):
    'Advance to iline and print it'
    buf().dot = iline
    print (lines()[iline]).rstrip() # strip trailing \n

def p(start, end):
    'Print lines from start up to (but not including) end'
    for iline in xrange(start,end):
        l(iline)

# adding, changing, and deleting text

def a(iline, text):
    'Append text after iline'
    # FIXME
    pass

def i():
    'Insert text before iline'
    # FIXME
    pass

def d(start, end):
    'Delete text from start up to end, set dot to first undeleted line'
    buf().lines[start:end] = []
    buf.unsaved = True
    if lines():
        buf().dot = min(start,S()-1) # S()-1 if we deleted end of buffer
    else:
        buf().dot = None

def s(start, end, pattern, new, glbl):
    """
    s(i,j,pattern,new,glbl): substitute new for pattern in lines
    i up to j. When glbl is True (the default), substitute
    all occurrences in each line. To substitute only the first
    occurence on each line, set glbl to False.  Lines i,j default
    to .,.+1  Set dot to the last changed line.
    """
    for i in range(start,end):
        if pattern in lines()[i]: # test to see if we should advance dot
            lines()[i] = lines()[i].replace(pattern,new, -1 if glbl else 1)
            buf().dot = i
