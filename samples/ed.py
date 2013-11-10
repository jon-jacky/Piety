"""
ed.py - ed is the standard text editor.  For more explanation see ed.md.

Limitations: for now line addresses i and j must be integers.
              Text patterns are not yet supported.
"""

from os.path import isfile, basename

# items appear in same order as in ed.md

# data structures

class Buffer(object):
    """
    Text buffer for ed 
    """
    def __init__(self):
        """
        New text buffer
        Be careful to only access lines by slice not index
        Then dot == 0 works even when lines == []
        """
        self.lines = [] # text in the current buffer, a list of strings
        self.dot = 0 # index of current line dot . in lines
        self.filename = None # filename (string) 
        self.unsaved = False # True if  buffer contains unsaved changes

current = 'scratch'  #  name of the current buffer, start with scratch buffer

# the state of ed is a dictionary from buffer names (strings) to buffers
# start with an empty scratch buffer, there is always a current buffer
buffers = dict() 
buffers[current] = Buffer()

# Access to data structures

def buf():
    """
    The current buffer: text and metadata
    """
    return buffers[current]

def lines():
    """
    Text in the current buffer: a list of lines
    """
    return buf().lines

def o():
    """
    . (dot), index of the current line where text is changed/inserted by default
    """
    return buf().dot

def S():
    """
    $, number of lines in the current buffer, index of last line + 1
    """
    return len(buf().lines)


# helper functions for commands: get and check arguments

def get_range(func, args):
    """
    Return start, end: ints that define range of lines.
     func: function object to name in error msg
     args: sequence of arguments (possibly empty)
    Assign defaults for missing arguments
    Check type and range.  If  error, print message and return None.
    """
    nargs = len(args)
    if nargs == 0:
        start, end = o(),o()+1
    elif nargs == 1:
        start, end = args[0], args[0]+1
    else:
        start, end = args[0], args[1]
    if (isinstance(start, int) and isinstance(end, int)
        and (0 <= start <= end <= S())):
        return start, end
    else:
        print '? %s start line, end line' % func.__name__
        return None


# Commands - working with files and buffers

def B(filename):
    """
    Create a new Buffer and load the file name.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    global current
    if not isinstance(filename,str):
        print '? B filename (string)'
        return
    temp = Buffer()
    if isfile(filename):
        fd = open(filename, mode='r')        
        temp.lines = fd.readlines()
        fd.close()
    # else new file will be created when buffer is written out
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
        print '? b buffername (string)'

def w(*args):
    """
    write current buffer contents to file name 
    (default: stored filename or, if none, current buffer name). 
    Print the file name and the number of lines written. Does not change dot.
    Does not change stored filename.
    """
    if len(args) > 0:
        name = args[0]
    elif buf().filename:
        name = buf().filename 
    else:
        name = current
    if not (isinstance(name,str)):
        print '? w filename (string)'
        return
    fd = open(name, 'w')
    for line in lines():
        fd.write(line)
    buf().unsaved = False
    print '%s, %d lines' % (name, len(lines()))

        
def D(name):
    """
    Delete buffer named 'name'
    """
    global buffers, current
    # there must always be at least one buffer
    if name in buffers and not name == 'scratch': 
        del buffers[name]
        if name == current: # pick a new current buffer
            keys = buffers.keys()
            current = keys[0] if keys else None
    else:
        print '? D buffername (string)'


# Displaying information

def n():
    """
    Print buffer names.  Current buffer is marked with
    . (period).  Buffers with unsaved changes are marked with an asterisk.
    Also print name, ., $, and filename of each buffer.
    """
    for name in buffers:
        lines = buffers[name].lines
        print '%s%s%-12s %6d%6d %s' % \
            ('.' if name == current else ' ',
             '*' if buffers[name].unsaved else ' ',
             name, buffers[name].dot, len(lines), buffers[name].filename)

def m():
    """
    Print current line index, dot.  Also print other status information:
    length of buffer $, buffer name current, buffer filename.
    """
    print '%d/%d  %s  %s' % (o(), S(), current, buf().filename)


# Displaying and navigating text

def p(*args):
    """
    Print text in range. Do not change dot.
    """
    limits = get_range(p, args)
    if limits:
        start, end = limits
    else:
        return
    for line in lines()[start:end]:
        print line.rstrip() # strip trailing \n

    
def l(*args):
    """
    args is iline
    Move dot to line iline and print it. Defaults to .+1, line after dot,
    so repeatedly invoking l() advances through the buffer, printing lines. 
    """
    if len(args) == 0:
        iline = o() + 1
    else:
        iline = args[0]
    if not (isinstance(iline, int) and (0 <= iline < S())):
        print '? l line'
        return
    buf().dot = iline
    print (lines()[iline]).rstrip() # strip trailing \n


# Adding, changing, and deleting text

def a(*args):
    """
    Append text after line i (default .)
    """
    return addlines(a, *args)

def i(*args):
    """
    Insert text before line i (default .)
    """
    return addlines(i, *args)


def addlines(func, *args):
    """
    implements both append *a* and insert *i* commands
    func is the function to perform - pass in function object, not name
    args might be iline, text or just text
    """
    iline, bigstring = o(), '' # defaults
    nargs = len(args)
    if nargs == 0:
        pass # use defaults
    elif nargs == 1:
        bigstring = args[0]
    else:
        iline, bigstring = args[0], args[1]
    if not (isinstance(iline, int) and isinstance(bigstring, str)
            and (0 <= iline <= S())): # S() == 0 when buffer is enpty
        print '? %s line (int) text (string)' % func.__name__
        return
    if bigstring:
        newlines = [ line + '\n' for line in bigstring.split('\n') ] 
    else:
        newlines = [] # no '\n' line when bigstring is empty
    if func == a: # append
        start = iline+1 
    elif func == i: # insert 
        start = iline
    else:
        print '? a or i (function object)'
        return
    end = start
    buf().lines[start:end] = newlines
    buf().dot = o() + len(newlines)
    if newlines:
        buf().unsaved = True


def d(*args):
    """
    delete text in range
    Set dot to the first undeleted line
    """
    limits = get_range(d, args)
    if limits:
        start, end = limits
    else:
        return
    buf().lines[start:end] = []
    buf().dot = min(start, S()-1) # if we deleted end of buffer
