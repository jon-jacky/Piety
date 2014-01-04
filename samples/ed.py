"""
ed.py - ed is the standard text editor.  

ed is a line-oriented text editor written in pure Python.  It provides
some of the commands from the classic Unix editor ed, augmented with
commands for managing multiple buffers and files from the later Unix
(and Plan 9) editor, sam.  You can use it in a command mode that
emulates Unix ed, or use its API to edit from the Python prompt or
write editing scripts in Python.

For more explanation see ed.md and the docstrings here.

Limitations: /pattern/ as line address only works in the l command,
   only for forward searches from . to $, with no wraparound
 For now other line addresses must be integers

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
    Return the current buffer, text and metadata
    """
    return buffers[current]

def lines():
    """
    Return text in the current buffer, a list of lines
    """
    return buf().lines

def o():
    """
    Return . (dot), index of the current line.
    where text is changed/inserted by default. 
    Returns None when the buffer is empty.
    """
    return buf().dot

def S():
    """
    Return number of lines in the current buffer, index of last line + 1
    """
    return len(lines()) # 0 when buffer is empty


# helper functions for commands

def do_cmd(f, f_cmd, args):
    """
    Get and check arguments from args, a sequence.
     then call function object f_cmd that does the work
    Used by functions a, c, d, i, p, r, s
    f is the caller, a function object.  
     f is only used for f.__name__ in the error message.
    f_cmd is the function that does the work, with arg list (f, start,end,string)
     f_cmd must take all 4 args, can assume they are valid, need not use them all
    If args are all valid, call f_cmd and return tuple (start,end,string)
    If any arg not valid, print error message and return False, don't call f_cmd
    Return value makes it possible to check args just once, then call g_cmd etc.
    Getting args is not trivial because usually every arg is optional
    Currently handles six cases, where args is:
     0:() 1a:(start) 1b:(string) 2a:(start,end) 2b:(start,string) 
      3:(start,end,string)
    All other cases are errors
    For now start and end must be int. Later we can add cases for /text/, ?text?
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
            return False
    elif len(args) == 2:
        if isinstance(args[0], int) and isinstance(args[1], int):
            start, end  = args[0], args[1]
        elif isinstance(args[0], int) and isinstance(args[1], str):
            start, string = args[0], args[1]
            end = start + 1
        else:
            print '? %s args are not int,int or int,string' % f.__name__
            return False
    elif len(args) == 3:
        if not (isinstance(args[0], int) and isinstance(args[1], int)
                and isinstance(args[2], str)):
            print '? %s args are not int,int,string' % f.__name__
            return False
        else:
            start, end, string = args[0], args[1], args[2]
    else:
        print '? %s more than 3 args given' % funct.__name__
        return False
    # print 'dot %s   start %d    end %d   S() %d' % (o(), start, end, S()) #DEBUG
    if not ((lines() and 0 <= start <= end <= S()) # allow start == end, nop
            or (not(lines()) and 0 == start == S())): # empty buffer
        print '? %s start, end out of range or wrong order' % f.__name__
        return False
    else:
        f_cmd(f, start, end, string)
        return start, end, string

def no_cmd(placeholder, placeholder1, placeholder2, placeholder3):
    """
    do-nothing command, pass to d_cmd to check arguments only
    """
    pass


# Commands - working with files and buffers

def u(name):
    """
    Create a new empty buffer, make it the current buffer
    """
    if not isinstance(name, str):
        print '? u name (string)'
        return 
    if name in buffers:
        print '? name in use'
        return
    u_cmd(name)

def u_cmd(name):
    """
    Do u (new buffer) command, assume valid arguments
    """
    global current
    temp = Buffer()
    buffers[name] = temp
    current = name


def r(*args):
    """
    r(iline, filename) read file into current buffer after iline, default .
    Print the file name and number of lines read. 
    Set . to the last line read.
    """
    valid_args = do_cmd(r, no_cmd, args)
    if valid_args: # if not, do_cmd already wrote error msgs
        iline, placeholder, filename = valid_args
        if not filename: # might be empty string
            print '? r(iline, filename), iline optional, filename must not be empty'
            return
        r_cmd(iline, filename)


def r_cmd(iline, filename):
    """
    Do r (read file) command, assume valid arguments
    """
    # r_cmd is used by both r and B
    if isfile(filename):
        fd = open(filename, mode='r')        
        lines = fd.readlines()
        fd.close()
        addlines(a, iline, lines) # a for append. Also updates dot, unsaved
        nlines = len(lines)
    # if no file, don't print error message, just say 0 lines read
    else:
        nlines = 0
    print '%s, %d lines' % (filename, nlines)


def B(filename):
    """
    Create a new Buffer and load the named file.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    global current
    if not isinstance(filename,str):
        print '? B filename (string)'
        return
    u_cmd(basename(filename)) # create buffer, make it current
    buf().filename = filename
    r_cmd(0, filename) # now new buffer is current, append at line 0

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
    Print the file name and the number of lines written. 
    Do not change dot.  Change buf().filename to name, 
    so subsequent writes go to the same file.
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
    buf().filename = name
    print '%s, %d lines' % (name, len(lines()))


def D(name):
    """
    Delete the named buffer
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
    p(i, j) Print text in range, default .,.+1.  
    Change dot to last line printed.
    """
    do_cmd(p, p_cmd, args)
    
def p_cmd(placeholder, start, end, placeholder1):
    """
    do p command, assumes valid arguments
    """
    for line in lines()[start:end]:
        print line.rstrip() # strip trailing \n
    if start < end:
        buf().dot = end - 1 # end is the line after the last printed
    
def l(*args):
    """
    l(iline) Move dot to line iline and print it. Defaults to .+1, 
    line after dot, so repeatedly invoking l() advances through buffer, 
    printing lines. 
    """
    # We don't use do_cmd here because this uses o()+1 not o() as default
    if not lines():
        print '? empty buffer'
        return
    elif len(args) == 0:
        iline = o() + 1
    elif isinstance(args[0], int):
        iline = args[0]
    # fold all this this into do_cmd ?
    elif (isinstance(args[0], str) and 
          args[0].startswith('/') and args[0].endswith('/')):
        pattern = args[0][1:-1]
        found = False
        # search only to end of buffer, no wrap around yet
        for imatch, line in enumerate(lines()[o()+1:]):
            if pattern in line:
                found = True
                break
        iline = o()+1 + imatch if found else o()
    elif (isinstance(args[0], str) and 
          args[0].startswith('?') and args[0].endswith('?')):
        pass # FIXME search backward, assign iline
    else:
        print "? l (line number or '/pattern/' or '?pattern?')"
    if not (0 <= iline < S()):
        print '? line number out of range 0:%d' % S()
        return
    buf().dot = iline
    print (lines()[iline]).rstrip() # strip trailing \n


# Adding, changing, and deleting text

def a(*args):
    """
    a(iline, text)  Append text after iline, default .
    """
    do_cmd(a, ai_cmd, args)

def i(*args):
    """
    i(iline, text)  Insert text before iline, default .
    """
    do_cmd(i, ai_cmd, args)

def ai_cmd(f, iline, placeholder, string):
    """
    implements a(ppend), i(nsert), and c(hange) commands
    f is the function to perform, used to select insertion point
    """
    if string:
        newlines = [ line + '\n' for line in string.split('\n') ]
        addlines(f, iline, newlines)

def addlines(f, iline, newlines):
    """
    append or insert newlines in current buffer at iline, used by a, c, i, r
    """
    # empty buffer when not lines() is a special case for append
    start = iline if (f == i or not lines()) else iline+1 # insert else append
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
    i,j default to .,.+1  Set dot to the last replacement line.
    """
    # delete then insert
    # if args are not valid, do_cmd does not change buffer and returns False
    valid_args = do_cmd(d, d_cmd, args) # delete if args are valid
    if valid_args:
        start, end, string = valid_args
        # now must reevaluate o(), preceding delete changed it
        # new o() is first line after deletes, so usually must insert not append
        # BUT last line is a special case, here o() is last line so must append
        # BUT BUT when last line is also first line is a special special case
        # Must check 'start' to find if that one line was start or end of file
        f = i if o() < S()-1 or start == 0 else a # f = insert if ... else append
        ai_cmd(f,o(),end,string) # end here is placeholder, required but not used


def s(*args):
    """
    s(i,j,pattern,new,glbl): substitute new for pattern in lines
    i up to j. When glbl is True (the default), substitute
    all occurrences in each line. To substitute only the first
    occurence on each line, set glbl to False.  Lines i,j default
    to .,.+1  Set dot to the last changed line.
    """
    # Use do_cmd to get and check i,j args, here just get pattern,new,glbl
    # valid args suffix are (...,pattern,new) (...,pattern,new,glbl)
    if len(args) > 1 and isinstance(args[-2],str) and isinstance(args[-1],str):
        pattern = args[-2]
        new = args[-1]
        glbl = True
        valid_args = do_cmd(s, no_cmd, args[:-2]) # get,check any i,j args
    elif (len(args) > 2 and isinstance(args[-3],str) and isinstance(args[-2],str)
          and True): # last arg can almost always be interpreted as Boolean
        pattern = args[-3]
        new = args[-2]
        glbl = bool(args[-1])
        valid_args = do_cmd(s, no_cmd, args[:-3]) # get,check any i,j args
    else:
        print '? s(start,end,pattern,new,global) int int str str bool'
        return
    if valid_args:
        start, end, string = valid_args # string is placeholder, not used
        for i in range(start,end):
            if pattern in lines()[i]: # test to see if we should advance dot
                lines()[i] = lines()[i].replace(pattern,new, -1 if glbl else 1)
                buf().dot = i
