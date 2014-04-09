"""
ed.py - ed is the standard text editor.  

ed is a line-oriented text editor written in pure Python.  It provides
many of the commands from the classic Unix editor ed, augmented with a
few commands for managing multiple buffers and files from the later
Unix (and Plan 9) editor, sam.  You can use it in a command mode that
emulates Unix ed, or use its API to edit from the Python prompt or
write editing scripts in Python.

This module provides both the classic command interface and the public
Python API.  Another module, ed0.py, provides the core: data structures
and the internal API.

For more explanation see ed.md, the docstrings here, and the tests
in Piety/test/ed/

"""

import re, os

# ed0 is editor core: data structures and functions that update them
import ed0  # must prefix command names: ed0.p etc. to disambiguate from p here
# use these here without prefix
from ed0 import buffers, lines, o, S, buf, F, R, mk_start, mk_range, start_ok, start_empty_ok, range_ok
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

def current_filename(filename):
    """
    Return filename arg if present, if not return current filename.
    Do not change current filename, assign only if it was previously absent.
    """
    if filename:
        if not buf().filename:
            buf().filename = filename
        return filename
    if buf().filename:
        return buf().filename 
    print('? no current filename')
    return None

# files and buffers

def f(*args):
    'set default filename, if filename not specified print current filename'
    x, xx, filename, xxx = parse_args(args)
    if filename:
        ed0.f(filename)
        return
    if buf().filename:
        print buf().filename
        return
    print '? no current filename'

def e(*args):
    'read in file, replace buffer contents unless unsaved changes'
    if buf().unsaved:
        print '? warning: file modified'
        return
    E(*args)

def E(*args):
    'read in file, replace buffer contents despite unsaved changes'
    x, xx, filename, xxx = parse_args(args)
    if not filename:
        filename = buf().filename
    if not filename:
        print '? no current filename'
        return
    ed0.b_new(ed0.current) # replace previous current buffer with new buffer
    # FIXME? next 3 lines repeated at end of B()
    buf().filename = filename
    ed0.r(0, filename, new_buffer=True) # FIXME? does r really need new_buffer 
    print '%s, %d lines' % (filename, S())

def r(*args):
    'Read file contents into buffer after iline'
    start, x, name, xx = parse_args(args)
    filename = current_filename(name)
    if not filename:
        return # current_filename already printed error msg
    iline = mk_start(start)
    if not start_empty_ok(iline): # r command works even for empty buffer
        print '? invalid address'
        return
    S0 = S() # record number of lines now to calc how many we read
    ed0.r(iline, filename)
    print '%s, %d lines' % (filename, S()-S0)

def b(*args):
    """
    Set current buffer to name.  If no buffer with that name, create one.
    If no name given, print the name of the current buffer.
    """
    x, xx, buffername, xxx = parse_args(args)
    if not buffername:
        print_status(ed0.current, o())
        return
    ed0.b(buffername)

def B(*args):
    'Create new Buffer and load the named file. Buffer name is file basename'
    x, xx, filename, xxx = parse_args(args)
    if not filename:
        print '? file name'
        return
    buffername = os.path.basename(filename) # may differ from filename
    if buffername in buffers:
        # FIXME? create new buffername a la emacs name<1>, name<2> etc.
        print '? buffer name %s already in use' % buffername
        return
    ed0.b(buffername)
    # FIXME? next 3 lines repeated at end of E
    buf().filename = filename
    ed0.r(0, filename, new_buffer=True)
    print '%s, %d lines' % (filename, S())

def w(*args):
    'write current buffer contents to file name'
    x, xx, name, xxx = parse_args(args)
    filename = current_filename(name)
    if not filename:
        return # current_filename already printed error msg
    ed0.w(filename)
    print '%s, %d lines' % (filename, len(lines())-1) # don't print empty line 0

def D(*args):
    'Delete the named buffer, if unsaved changes print message and exit'
    x, xx, text, xxx = parse_args(args)
    name = text if text else ed0.current
    if name in buffers and buffers[name].unsaved:
        print '? unsaved changes, use X to delete'
        return
    X(*args)

def X(*args):
    'Delete the named buffer, even if it has unsaved changes'
    x, xx, text, xxx = parse_args(args)
    name = text if text else ed0.current
    if not name in buffers:
        print '? buffer name'
        return
    if name == 'main':
        print "? Can't delete main buffer"
        return
    ed0.D(name)

# Displaying information

def print_status(bufname, iline):
    'used by e and n, given bufname and iline prints dot, $, filename, unsaved'
    buf = buffers[bufname]
    loc = '%s/%d' % (iline, len(buf.lines)-1) # don't count empty first line
    print '%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == ed0.current else ' ',
                               '*' if buf.unsaved else ' ', 
                               bufname, (buf.filename if buf.filename else 
                                         'no current filename'))

def A(*args):
    ' = in command mode, print the line number of the addressed line'
    start, x, xx, xxx = parse_args(args)
    iline = start if start != None else S() # default $ not .
    if start_empty_ok(iline): # don't print error message when file is empty
        print iline
    else:
        print '? invalid address'

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
        print '? invalid address'
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
        print '? invalid address'
        return
    ed0.l(iline)

# Adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    ai_cmd(ed0.a, args)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    ai_cmd(ed0.i, args)

def ai_cmd(cmd, args):
    'a(ppend) or i(nsert) command'
    start, x, text, xx = parse_args(args)
    iline = mk_start(start)
    if not start_empty_ok(iline):  # a, i commands work even for empty buffer
        print '? invalid address'
        return
    if text:
        cmd(iline, text)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes or...'
    start, end, x, xxx = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? invalid address'
        return
    ed0.d(istart, iend)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    start, end, text, x = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? invalid address'
        return
    ed0.c(istart,iend,text)
        
def s(*args):
    """
    Substitute new for old in lines from start up to end.
    When glbl is False (the default), substitute only the first occurrence 
    in each line.  Otherwise substitute all occurrences in each line
    """
    start, end, old, params = parse_args(args)
    istart, iend = mk_range(start, end)
    if not range_ok(istart, iend):
        print '? invalid address'
        return
    # params might be [ new, glbl ]
    if old and len(params) > 0 and isinstance(params[0],str):
        new = params[0]
    else:
        print '? /old/new/'
        return
    if len(params) > 1:
        glbl = bool(params[1])
    else:
        glbl = False # default
    ed0.s(istart, iend, old, new, glbl)

# command mode

def q(*args):
    'quit command mode'
    pass # ignore args, caller quits when this command requested


complete_cmds = 'deEflpqrswbBDnAX' # commands that do not require further input
input_cmds = 'aic' # commands that use input mode to collect text
ed_cmds = complete_cmds + input_cmds

# regular expressions for command parts, no spaces allowed
number = re.compile(r'(\d+)')
fwdsearch = re.compile(r'/(.*?)/') # non-greedy *? for /text1/,/text2/
bkdsearch = re.compile(r'\?(.*?)\?')
text = re.compile(r'(.*)') # nonblank

def match_address(command):
    'return line number at start of command (None of not found), and rest of command'
    if command == '':
        return None, '' 
    if command[0] == '.': # current line
        return o(), command[1:]
    if command[0] == '$': # last line
        return S(), command[1:]
    if command[0] == ';': # equivalent to .,$  - current line to end
        return o(), ',$'+ command[1:]
    if command[0] in ',%': # equivalent to 1,$ - whole buffer
        return 1, ',$'+ command[1:]
    m = number.match(command) # digits, the line number
    if m:
        return int(m.group(1)), command[m.end():]
    m = fwdsearch.match(command)  # /text/ or // - forward search
    if m: 
        return F(m.group(1)), command[m.end():] # FIXME rename S
    m = bkdsearch.match(command)  # ?text? or ?? - backward search
    if m: 
        return R(m.group(1)), command[m.end():] # FIXME rename R
    # FIXME - also handle -n +n 'c 
    return None, command

def parse_cmd(command):
    """
    Parses command string, returns multiple values in this order:
     cmd - single-character command name
     istart, jend - integer line numbers 
     params - string containing other command parameters
    All are optional except cmd, assigns None if item is not present
    """
    cmd, istart, jend, params = None, None, None, None
    # look for start addr, optional. if no match istart,tail == None,command
    istart, tail = match_address(command)
    # look for end address, optional
    if istart != None:
        if tail and tail[0] == ',': # addr separator, next addr NOT optional
            jend, tail = match_address(tail[1:])
            if jend == None:
                print '? end address expected at %s' % tail
                return 'ERROR', istart, jend, params
    # look for command, NOT optional
    if tail and tail[0] in ed_cmds:
        cmd, params = tail[0], tail[1:].strip()
    # special case command names
    elif tail == '':
        cmd = 'l' # default for empty command
    elif tail[0] == '=':
        cmd = 'A'
    else:
        print '? command expected at %s' % tail
        return 'ERROR', istart, jend, params
    # command-specific parameter parsing
    if cmd == 's' and len(params.split('/')) == 4: # s/old/new/g, g optional
        empty, old, new, glbl = params.split('/') # glbl == '' when g absent
        return cmd, istart, jend, old, new, glbl
    # all other commands, no special parameter parsing
    else:
        return cmd, istart, jend, params if params else None 

def ed():
    """
    Top level ed command to use at Python prompt.
    This version won't work in Piety, it calls blocking command raw_input
    """
    command_mode = True # alternates with input mode used by a,i,c commands
    cmd = 'ed' # anything but 'q'
    while not cmd == 'q':
        if command_mode:
            # FIXME blocks here at raw_input()
            command = raw_input() # no prompt - maybe make prompt a parameter
            items = parse_cmd(command)
            if items[0] == 'ERROR':
                continue # parse_cmd already printed message
            else:
                tokens = tuple([ t for t in items if t != None ])
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
