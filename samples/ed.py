"""
ed.py - ed is the standard text editor.  For more explanation see ed.md.

Limitations: for now line addresses must be integers.
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
        self.dot = None # index of current line, None when buffer is empty
        self.filename = None # filename (string) 
        self.unsaved = False # True if buffer contains unsaved changes

# buffers are in a dict from buffer names (strings) to Buffer instances
buffers = dict() 

# There is always a current buffer so we can avoid check for special case
# Start with one empty buffer named 'scratch', can't ever delete it
current = 'scratch'
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
              returns None when buffer is empty
    """
    return buf().dot

def S():
    """
    $, number of lines in the current buffer, index of last line + 1
    """
    return len(lines()) # 0 when buffer is empty


# helper functions for commands

def do_cmd(f, f_cmd, args):
    """
    Get and check arguments from args, a sequence.
     then call function object f_cmd that does the work
    Getting args is not trivial because usually every arg is optional
    Currently handles six cases, where args is:
     0:() 1a:(start) 1b:(string) 2a:(start,end) 2b:(start,string) 
      3:(start,end,string)
    All other cases are errors
    For now start, end must be int. Later we can add cases for /text/
    f is the caller, a function object.  
     f is only used for f.__name__ in the error message.
    f_cmd is the function that does the work, with arg list (f, start,end,string)
     f_cmd must take all 4 args, can assume they are valid, need not use them all
    If args are all valid, call f_cmd
    If any arg not valid, print error message and return, don't call f_cmd
    """
    if lines():
        start, end, string = o(), o()+1, ''
    else:
        start, end, string = 0, 1, '' # empty buffer, 0:1 is a valid slice
    if len(args) == 0:
        pass # use defaults
    elif len(args) == 1:
        if isinstance(args[0], int):
            start = args[0]
            end = start + 1
        elif isinstance(args[0], str):
            string = args[0]
        else:
            print '? %s arg is not int or string' % f.__name__
            return
    elif len(args) == 2:
        if isinstance(args[0], int) and isinstance(args[1], int):
            start, end  = args[0], args[1]
        elif isinstance(args[0], int) and isinstance(args[1], str):
            start, string = args[0], args[1]
            end = start + 1
        else:
            print '? %s args are not int,int or int,string' % f.__name__
            return
    elif len(args) == 3:
        if not (isinstance(args[0], int) and isinstance(args[1], int)
                and isinstance(args[2], str)):
            print '? %s args are not int,int,string' % f.__name__
            return
        else:
            start, end, string = args[0], args[1], args[2]
    else:
        print '? %s more than 3 args given' % funct.__name__
        return
    # print 'dot %s   start %d    end %d   S() %d' % (o(), start, end, S()) #DEBUG
    if not ((lines() and 0 <= start <= end <= S()) # allow start == end, nop
            or (not(lines()) and 0 == start == S())): # empty buffer
        print '? %s start, end out of range or wrong order' % f.__name__
        return
    else:
        f_cmd(f, start, end, string)
    

# Commands - working with files and buffers

def B(filename):
    """
    Create a new Buffer and load the file name.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    # FIXME?  Can't we build this out of functions u and r - ?
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
    w(name) write current buffer contents to file name 
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
    if name not in buffers:
        print '? D buffername (string)'
        return
    if name == 'scratch': 
        print "? Can't delete scratch buffer"
        return
    if buffers[name].unsaved:
        pass
        # print '? unsaved changes'
        # return
        # FIXME but then how can we delete it anyway?
    del buffers[name]
    if name == current: # pick a new current buffer
        keys = buffers.keys()
        current = keys[0] if keys else None

# Displaying information

def n():
    """
    Print buffer names.  Current buffer is marked with
    . (period).  Buffers with unsaved changes are marked with an asterisk.
    Also print name, ., $, and filename of each buffer.
    """
    for name in buffers:
        print '%s%s%-12s %6s%6d %s' % \
            ('.' if name == current else ' ',
             '*' if buffers[name].unsaved else ' ',
             name, buffers[name].dot, len(buffers[name].lines),
             buffers[name].filename)

def m():
    """
    Print current line index, dot.  Also print other status information:
    length of buffer $, buffer name current, buffer filename.
    """
    print '%s/%d  %s  %s' % (o(), S(), current, buf().filename)


# Displaying and navigating text

def p(*args):
    """
    p(i, j) Print text in range, default .,.+1.  Do not change dot.
    """
    do_cmd(p, p_cmd, args)
    
def p_cmd(placeholder, start, end, placeholder1):
    """
    do p command, assumes valid arguments
    """
    # FIXME: should yield to scheduler after N lines
    for line in lines()[start:end]:
        print line.rstrip() # strip trailing \n
    

def l(*args):
    """
    l(iline) Move dot to line iline and print it. Defaults to .+1, line after dot,
    so repeatedly invoking l() advances through the buffer, printing lines. 
    """
    # We don't use do_cmd here because this uses o()+1 not o() as default
    if not lines():
        print '? empty buffer'
        return
    elif len(args) == 0:
        iline = o() + 1
    else:
        iline = args[0]
    if not (isinstance(iline, int) and (0 <= iline < S())):
        print '? l (line)'
        return
    buf().dot = iline
    print (lines()[iline]).rstrip() # strip trailing \n


# Adding, changing, and deleting text

def a(*args):
    """
    a(i, text)  Append text after line i (default .)
    """
    do_cmd(a, do_ai, args)

def i(*args):
    """
    i(i, text)  Insert text before line i (default .)
    """
    do_cmd(i, do_ai, args)


def do_ai(f, iline, placeholder, string):
    """
    implements both append *a* and insert *i* commands
    f is the function to perform, used to select insertion point
    """
    newlines = [ line + '\n' for line in string.split('\n') ]
    if string:
        start = iline if f == i else iline+1 # i insert else a append
        end = start
        buf().lines[start:end] = newlines
        buf().dot = start + len(newlines)-1
        buf().unsaved = True


def d(*args):
    """
    d(i,j)  delete text in range, default .,.+1
    Set dot to the first undeleted line
    """
    do_cmd(d, d_cmd, args)

def d_cmd(placeholder, start, end, placeholder1):
    """
    Do d command, assume valid arguments
    """
    if lines() and start < end:
        buf().lines[start:end] = []
        buf.unsaved = True
        if lines():
            buf().dot = min(start,S()-1) # S()-1 if we deleted end of buffer
        else:
            buf().dot = None
        

def c(*args):
    """
    c(i,j, text): change (replace) lines i up to j to text.
    (i,j default to .,.+1).  Set dot to the last replacement line.
    """
    # FIXME not yet tested
    d(args)
    i(args)
