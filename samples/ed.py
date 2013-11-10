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
        """
        self.lines = list() # text in the current buffer, a list of strings
        self.dot = None # index of current line dot . in lines
        self.filename = None # filename (string) 
        self.unsaved = False # True if  buffer contains unsaved changes

buffers = dict() # dictionary from buffer names (strings) to buffers

current = None #  name of the current buffer, None if no buffers

# Any function might be called in the initial state with no buffers

def buf():
    """
    The current buffer: text and metadata
    """
    # buffers might be empty
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


# Commands - working with files and buffers

def B(filename):
    """
    Create a new Buffer and load the file name.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    global buffers, current
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
    elif current in buffers and buf().filename:
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
    print '%s, %d' % (name, len(lines()))

        
def D(name):
    """
    Delete buffer named 'name'
    """
    global buffers, current
    if name in buffers:
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
        # use %s not %d everwhere, dot might be None
        lines = buffers[name].lines
        print '%s%s%-12s %6s%6s %s' % \
            ('.' if name == current else ' ',
             '*' if buffers[name].unsaved else ' ',
             name, buffers[name].dot, 
             len(lines)-1 if lines else None, # $, not N of lines
             buffers[name].filename)

def m():
    """
    Print current line number, .  Also print other status
    information: number of last line $, buffer name current,
    filename.
    """
    # use %s everywhere, not %d - . and $ might be None
    if current in buffers: # initially None
        print '%s/%s  %s  %s' % (o(),S(), current, buf().filename)

# Displaying and navigating text

def p(*args):
    """
    Print lines i through j in the current buffer
    i defaults to dot, j defaults to i
    Does not change dot
    """
    nargs = len(args)
    if nargs == 0:
        i,j = o(),o()
    elif nargs == 1:
        i,j = args[0],args[0]
    else: # nargs > 1
        i,j = args[0],args[1]
    if current in buffers and (0 <= i <= S()) and (0 <= j <= S()) and (i <= j):
        text = lines()
        for iline in xrange(i,j+1): # xrange upper limit is not inclusive
            print text[iline].rstrip() # strip trailing \n
    else: 
        print '? p start (int) end (int)'

    
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
        if not isinstance(i,int):
            print '? l line (int)'
            return
    else:
        i = o() + 1
    if current in buffers and (0 <= i <= S()):
        buf().dot = i
        print (lines()[i]).rstrip() # strip trailing \n
    else:
        print '? l line (int)'

# Adding, changing, and deleting text

def a(*args):
    """
    Append text after line i (default .)
    Here the first argument i might be missing but the next argument,
    the text - a string - is almost always going to be present.
    """
    return changelines(a, *args)

def i(*args):
    """
    Insert text before line i (default .)
    Here the first argument i might be missing but the next argument,
    the text - a string - is almost always going to be present.
    """
    return changelines(i, *args)


def changelines(func, *args):
    """
    implements both append *a* and insert *i* commands
    func is the function to perform - pass in function object, not name
    """
    iline,jline, text = o(),o(),None # defaults, 'i' is name of insert fcn
    nargs = len(args)
    if nargs == 0:
        print '? a|i line (int) text (string)'
        return
    elif nargs == 1:
        bigstring = args[0]
    elif nargs == 2:
        iline, bigstring = args[0], args[1]
    elif nargs == 3: # used for change only
        iline, jline, bigstring = args[0], args[1]
    newlines = [ line + '\n' for line in bigstring.split('\n') ]
    old_dot = o()
    if current in buffers and (0 <= iline <= S()): # unempty buffer
        if func == a: # append
            start = iline+1 
            end = start
        elif func == i: # insert 
            start = iline
            end = start
        # other functions to come?
        else: 
            print '? a|i (function object)'
            return
        buf().lines[start:end] = newlines
        buf().dot = old_dot + len(newlines)
    elif current in buffers and not lines(): # empty buffer
        buf().lines = newlines
        buf().dot = len(newlines) - 1
    else: # no buffer or bad iline,jline
        print '? a|i line (int) text (string)'
        return
    if newlines:
        buf().unsaved = True


def get_range(func, args):
    """
    Return start, end: ints that define range of lines.
     func: function object to name in error msg
     args: sequence of arguments (possibly empty)
    Assign defaults for mussing arguments
    Check type and range.  If  error, print message and return None.
    """
    nargs = len(args)
    if nargs == 0:
        start, end = o(),o()+1
    elif nargs == 1:
        start, end = args[0], args[0]+1
    elif nargs == 2:
        start, end = args[0], args[1]
    if (isinstance(start, int) and isinstance(end, int)
        and (0 <= start < end <= S())):
        return start, end
    else:
        print '? %s start line, end line' % func.__name__
        return None

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
