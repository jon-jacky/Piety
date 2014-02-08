"""
ed.py - ed is the standard text editor.  

ed is a line-oriented text editor written in pure Python.  It provides
some of the commands from the classic Unix editor ed, augmented with
commands for managing multiple buffers and files from the later Unix
(and Plan 9) editor, sam.  You can use it in a command mode that
emulates Unix ed, or use its API to edit from the Python prompt or
write editing scripts in Python.

For more explanation see ed.md and the docstrings here.

Limitations: 
   In s(ubstitute) command, pattern must be literal string, not regexp
   search pattern must be literal string, not regexp
   searches only to end (or beginning) of buffer, no wraparound

"""

import re
from os.path import isfile, basename

import ed0  # editor core

# items appear in same order as in ed.md

# helper functions for commands

def isaddress(arg):
    """
    Return true if arg is a line address
    """
    # trivial - used to check pattern addresses here but now use f, z instead
    return isinstance(arg, int)
                     
def address(arg):
    """
    Return line number for line address of arg. assume isaddress(arg) is True.
    """
    # trivial - used to search pattern addresses here but now use f, z instead
    return arg


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
     0:() 
     1a:(start) 1b:(string) 
     2a:(start,end) 2b:(start,string) 
     3:(start,end,string)
    All other cases are errors
    start and end are addresses, either int or '/pattern/' or '?pattern?'
    string is text content, in case of 1b and 2b can't be '/.../' or '?...?'
    """
    if lines():
        start, end, string = o(), o()+1, ''
    else:
        start, end, string = 0, 1, '' # empty buffer, 0:1 is a valid slice
    if len(args) == 0:
        pass # use defaults
    elif len(args) == 1:
        if isaddress(args[0]):
            start = address(args[0])
            end = start + 1
        elif isinstance(args[0], str):
            string = args[0]
        else:
            print '? %s arg is not address or string' % f.__name__
            return False
    elif len(args) == 2:
        if isaddress(args[0]) and isaddress(args[1]):
            start, end  = address(args[0]), address(args[1])
        elif isaddress(args[0]) and isinstance(args[1], str):
            start, string = address(args[0]), args[1]
            end = start + 1
        else:
            print '? %s args are not address,address or address,string' % f.__name__
            return False
    elif len(args) == 3:
        if not (isaddress(args[0]) and isaddress(args[1])
                and isinstance(args[2], str)):
            print '? %s args are not address,address,string' % f.__name__
            return False
        else:
            start, end, string = address(args[0]), address(args[1]), args[2]
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
# All commands must use *args to deal with optional arguments

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
        ed0.r(iline, filename)
    # if no file, don't print error message, just say 0 lines read
    else:
        nlines = 0
    print '%s, %d lines' % (filename, nlines)

def b(*args):
    """
    Set current buffer to name.  If no buffer with that name, create one
    """
    global current
    if not args or not isinstance(args[0], str):
        print '? b buffername (string)'
        return
    name = args[0]
    ed0.b(name)

def B(*args):
    """
    Create a new Buffer and load the named file.  Print the number of
    lines read (0 when creating a new file). The new buffer becomes 
    the current buffer.  The name of the buffer is the same as the
    filename, but without any path prefix.
    """
    global current
    if not args or not isinstance(args[0], str):
        print '? B filename (string)'
        return
    filename = args[0]
    ed0.B(filename)

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
    ed0.w(name)
    buf().filename = name
    print '%s, %d lines' % (name, len(lines()))

def D(*args):
    """
    Delete the named buffer, if unsaved changes print message and exit
    """
    name = args[0] if args else current
    if name in buffers and buffers[name].unsaved:
        pass
        print '? unsaved changes, must use DD to delete'
        return
    DD(*args)

def DD(*args):
    """
    Delete the named buffer, even if it has unsaved changes
    """
    global buffers, current
    name = args[0] if args else current
    if name not in buffers:
        print '? D buffername (string)'
        return
    if name == 'scratch': 
        print "? Can't delete scratch buffer"
        return
    ed0.D(name)
    if name == current: # pick a new current buffer
        keys = buffers.keys()
        current = keys[0] if keys else None

# Displaying information

def print_status(bufname, iline):
    """
    as in  ./$    Buffer         File
           ---    ------         ----
       iline/N  .*bufname        filename 
    """
    buf = buffers[bufname]
    loc = '%s/%d' % (iline, len(buf.lines))
    print '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == current else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, buf.filename)

def e(*args):
    """
    Print first arg, should be an address. Also print other buffer information
    Implements = in command mode 
    """
    do_cmd(e, e_cmd, args)

def e_cmd(placeholder, start, end, placeholder1):
    """
    do e command, print value of start arg and other buffer information
    """
    print_status(current, start)

def n(*args):
    """
    Print status of all buffers
    """
    # ignore args
    print """    ./$    Buffer        File
    ---    ------        ----"""
    for name in buffers:
        print_status(name, buffers[name].dot)

    
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
    ed0.p(start, end)
    
def l(*args):
    """
    l(iline) Move dot to line iline and print it. Defaults to .+1, 
    line after dot, so repeatedly invoking l() advances through buffer, 
    printing lines. 
    """
    # We don't use do_cmd here because this uses o()+1 not o() as default
    # FIXME but do_cmd has f arg so we can handle special case there 
    if not lines():
        print '? empty buffer'
        return
    elif len(args) == 0:
        iline = o() + 1
    elif isaddress(args[0]):
        iline = address(args[0])
    else:
        print "? l (line number or '/pattern/' or '?pattern?')"
    if not (0 <= iline < S()):
        print '? line number out of range 0:%d' % S()
        return
    ed0.l(iline)

# Adding, changing, and deleting text

def a(*args):
    """
    a(iline, text)  Append text after iline, default .
    """
    do_cmd(a, aic_cmd, args)

def i(*args):
    """
    i(iline, text)  Insert text before iline, default .
    """
    do_cmd(i, aic_cmd, args)

# FIXME for now store line for a,i,c commands used in ed input mode - hack!
aic_line = 0

def aic_cmd(f, iline, placeholder, string):
    """
    implements a(ppend), i(nsert), and c(hange) commands
    f is the function to perform, used to select insertion point
    """
    global aic_line
    aic_line = iline # FIXME needed by a,i,c in ed input mode, hack
    if string:
        ed0.addlines(f, iline, string)

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
        ed0.d(start, end)
        
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
        aic_cmd(f,o(),end,string) # end here is placeholder, required but not used

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
        ed0.s(start, end, pattern, new, glbl)

# command mode

def q(*args):
    """
    quit command mode
    """
    # ignore args
    pass # caller quits when this command requested

# compile regexp for each command form
Cmd = re.compile(r'\s*([a-zA-Z])(.*)')
l1Cmd = re.compile(r'\s*(\d+)\s*([a-zA-Z])(.*)')
l1l2Cmd = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*([a-zA-Z])(.*)')

def parse(command):
    """
    Parses command string, returns multiple values in this order:
     cmd - single-character command name
     istart, jend - integer line numbers 
     params - string containing other command parameters
    All are optional except cmd, assigns None if item is not present
    """
    cmd, istart, jend, params = None, None, None, None
    m = Cmd.match(command)
    if m:
        cmd, params = m.group(1), m.group(2).strip()
    else:
        m = l1Cmd.match(command)
        if m:
            istart, cmd, params = (int(m.group(1)), 
                                   m.group(2), m.group(3).strip())
        else:
            m = l1l2Cmd.match(command)
            if m:
                istart, jend, cmd, params = (int(m.group(1)), int(m.group(2)),
                                             m.group(3), m.group(4).strip())
            else:
                print '? cannot parse command: %s' % command
    # change order, put cmd first, if params is empty string return None
    return cmd, istart, jend, params if params else None 

def ed_cmd(command):
    """
    Handle a single command: parse it, call function from API
    """
    tokens = tuple([ t for t in parse(command) if t != None ])
    cmd, args = tokens[0], tokens[1:]
    if cmd in globals(): # dict from name (string) to object (fcn or ...)
        globals()[cmd](*args)
    else:
        print '? command not implemented: %s' % cmd
    return cmd # so caller knows when to quit

command_mode = True # alternates with input mode used by a,i,c commands

def ed():
    """
    Top level ed command to use at Python prompt.
    Won't work in Piety because it calls blocking command raw_input
    """
    global command_mode
    command_mode = True
    cmd = 'ed' # anything but 'q'
    while not cmd == 'q':
        if command_mode:
            command = raw_input(':') # maybe make prompt a parameter
            cmd = ed_cmd(command)    # handler
            if cmd in ('a','i','c'):
                command_mode = False # enter input mode
                newlines = '' # one big string
        else: # input mode for a, i, c commands
            line = raw_input() # no prompt
            if line == '.':
                globals()[cmd](aic_line, newlines) # FIXME uses global aic_line
                command_mode = True # exit input mode
            else:
                newlines += line + '\n' # raw_input strips \n, put it back

# Run the editor from the system command line:  python ed.py

if __name__ == '__main__':
    ed()
