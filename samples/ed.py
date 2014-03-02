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

import re, os

# ed0 is editor core: data structures and functions that update them
import ed0  # must prefix command names: ed0.p etc. to disambiguate from p here
# use these here without prefix
from ed0 import buffers, lines, o, S, buf, f, z, mk_start, mk_range, start_ok, start_empty_ok, range_ok
# must use ed0.current with prefix here to get correct value as it is updated

# arg lists, defaults, range checking

def parse_args(args):
    """
    Parse variable-length argument list, all arguments optional
    Return start, end: int or None, text: str or None, params: list. might be []
    """
    # get 2, 1, or 0 optional line numbers from head of args list
    if len(args) > 1 and isinstance(args[0],int) and isinstance(args[1],int):
        start, end, params = int(args[0]), int(args[1]), args[2:]
    elif len(args) > 0 and isinstance(args[0],int):
        start, end, params = int(args[0]), None, args[1:]
    else:
        start, end, params = None, None, args
    # get 1 or 0 optional strings and the rest of args list
    if params and isinstance(params[0], str):
        text, params = params[0], params[1:]
    else:
        text = None 
    return start, end, text, params # params might still be non-empty

# files and buffers

def r(*args):
    'Read file contents into buffer after iline'
    start, x, filename, xx = parse_args(args)
    if not filename:
        print '? file name'
        return
    iline = mk_start(start)
    if not start_empty_ok(iline): # r command works even for empty buffer
        print '? address out of range'
        return
    S0 = S() # record number of lines now to calc how many we read
    ed0.r(iline, filename)
    print '%s, %d lines' % (filename, S()-S0)

def b(*args):
    'Set current buffer to name.  If no buffer with that name, create one'
    x, xx, buffername, xxx = parse_args(args)
    if not buffername:
        print '? buffer name'
        return
    ed0.b(buffername)

def B(*args):
    'Create a new Buffer and load the named file'
    x, xx, filename, xxx = parse_args(args)
    if not filename:
        print '? file name'
        return
    b(os.path.basename(filename)) # buffername may differ from filename
    buf().filename = filename
    r(filename)

def w(*args):
    'write current buffer contents to file name'
    x, xx, text, xxx = parse_args(args)
    if text:
        filename = text
    elif buf().filename:
        filename = buf().filename 
    else:
        filename = ed0.current
    ed0.w(filename)
    buf().filename = filename
    print '%s, %d lines' % (filename, len(lines())-1) # don't print empty line 0

def D_cmd(confirm, *args):
    'Delete named buffer, used by D and DD'
    x, xx, text, xxx = parse_args(args)
    buffername = text if text else ed0.current
    if not buffername in buffers:
        print '? buffer name'
        return
    if buffername == 'scratch': 
        print "? Can't delete scratch buffer"
        return
    if confirm and buffers[buffername].unsaved:
        print '? unsaved changes, use DD to delete'
        return
    ed0.D(buffername)

def D(*args):
    'Delete the named buffer, if unsaved changes print message and exit'
    D_cmd(True, *args)

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    D_cmd(False, *args)

# Displaying information

def print_status(bufname, iline):
    'used by e and n, given bufname and iline prints dot, $, filename, unsaved'
    buf = buffers[bufname]
    loc = '%s/%d' % (iline, len(buf.lines)-1) # don't count empty first line
    print '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == ed0.current else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, buf.filename)

def e(*args):
    ' = in command mode, print_status for given line address and current buffer'
    start, x, xx, xxx = parse_args(args)
    iline = mk_start(start)
    # Even print out-of-range address for debugging, but warn after
    print_status(ed0.current, iline)
    if not start_empty_ok(iline): # don't print error message when file is empty
        print '? address out of range'

def n(*args):
    'Print status of all buffers'
    print """    ./$    Buffer        File
    ---    ------        ----"""
    for name in buffers:
        print_status(name, buffers[name].dot)
    
# Displaying and navigating text

def p(*args):
    'Print lines from start up to end, leave dot at last line printed'
    istart, jend, x, xx = parse_args(args)
    start, end = mk_range(istart, jend)
    if not range_ok(start, end):
        print '? address out of range'
        return
    ed0.p(start, end)
    
def l(*args):
    'Advance dot to iline and print it'
    iline, x, xx, xxx = parse_args(args)
    if not lines():
        print '? empty buffer'
        return
    # don't use usual default dot here, instead advance dot
    if iline == None:
        iline = o() + 1
    if not start_ok(iline):
        print '? address out of range'
        return
    ed0.l(iline)

# Adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    ai_cmd(ed0.a, args)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    ai_cmd(ed0.i, args)

# FIXME for now store line for a,i,c commands used in ed input mode - hack!
aic_line = 0

def ai_cmd(cmd, args):
    'a(ppend) or i(nsert) command'
    start, x, text, xx = parse_args(args)
    iline = mk_start(start)
    if not start_empty_ok(iline):  # a, i commands work even for empty buffer
        print '? address out of range'
        return
    if text:
        aic_line = iline  # FIXME, temporary
        cmd(iline, text)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes or...'
    start, end, x, xxx = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? address out of range'
        return
    ed0.d(istart, iend)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    start, end, text, x = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? address out of range'
        return
    aic_line = istart # FIXME needed?
    ed0.c(istart,iend,text)
        
def s(*args):
    """
    Substitute new for pattern in lines from start up to end.
    When glbl is True (the default), substitute all occurrences in each line,
    otherwise substitute only the first occurrence in each line.
    """
    start, end, pattern, params = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? address out of range'
        return
    # params might be [ new, glbl ]
    if pattern and len(params) > 0 and isinstance(params[0],str):
        new = params[0]
    else:
        print '? pattern, replacement'
        return
    if len(params) > 1:
        glbl = bool(params[1])
    else:
        glbl = True
    ed0.s(istart, iend, pattern, new, glbl)

# command mode

def q(*args):
    'quit command mode'
    pass # ignore args, caller quits when this command requested

# FIXME not practical to to match whole command at once - too many combinations
#  handle the addresses one at a time
# compile regexp for each command form
Cmd = re.compile(r'\s*([a-zA-Z])(.*)')
l1Cmd = re.compile(r'\s*(\d+)\s*([a-zA-Z])(.*)')
l1l2Cmd = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*([a-zA-Z])(.*)')

def parse_cmd(command):
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

complete_cmds = ('rbBwDDenpldsq') # commands that do not require further input
input_cmds = ('aic') # commands that use input mode to collect text

def ed():
    """
    Top level ed command to use at Python prompt.
    This version won't work in Piety because it calls blocking command raw_input
    """
    command_mode = True # alternates with input mode used by a,i,c commands
    cmd = 'ed' # anything but 'q'
    while not cmd == 'q':
        if command_mode:
            command = raw_input(':') # maybe make prompt a parameter
            tokens = tuple([ t for t in parse_cmd(command) if t != None ])
            cmd, args = tokens[0], tokens[1:]
            if cmd in complete_cmds:
                globals()[cmd](*args) # dict from name (string) to object (function)
            elif cmd in input_cmds:
                command_mode = False # enter input mode
                addlines = '' # one big string
            else:
                print '? command not implemented: %s' % cmd
        else: # input mode for commands that collect text
            line = raw_input() # no prompt
            if line == '.':
                args += (addlines,)
                globals()[cmd](*args)
                command_mode = True # exit input mode
            else:
                # \n is separator not terminator, first line is special case
                addlines += ('\n' + line) if addlines else line

# Run the editor from the system command line:  python ed.py

if __name__ == '__main__':
    ed()
