"""
ed.py - line-oriented text editor in pure Python based on classic Unix ed.

For more explanation see ed.md, ed.txt, docstrings and comments here,
and tests in test/ed/
"""

import re, os, sys, enum
import time # only used for sleep() in do_commands, FIXME write piety.sleep
import pysh  # provides embedded Python shell for ! command
import buffer
from updates import Op

# arg lists, defaults, range checking

# We parse twice, to provide both command strings and new Python API.
# Here parse_args parses variable-length argument lists for Python API.
# Below parse_cmd parses traditional ed command strings.

def parse_args(args):
    """
    Parse variable-length argument list for new Python API, all args optional.
    Return fixed length tuple: start, end, text, params 
    start, end are line numbers, for example the first and last line of region.
    When present, start and end are int, both might be absent, indicated None.
    text is the first token in the parameter list, str or None if absent
    params is the parameter list, [] if absent.
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

# The commands and API for ed.py use the classic Unix ed conventions for
# indexing and range (which are unlike Python): The index of the first
# line is 1, the index of the last line is the same as the number of
# lines (the length of the buffer in lines), and range i,j includes the
# last line with index j (so the range i,i is just the line i, but it is
# not empty).

# Defaults and range checking, use the indexing and range conventions above.
# mk_ functions replace None missing arguments with default line numbers

def mk_iline(iline):
    'Return iline if given, else default dot, 0 if buffer is empty'
    return iline if iline != None else buf.dot

def mk_range(start, end):
    """Return start, end if given, 
    else return defaults, calc default end from start"""
    start = mk_iline(start)
    return start, end if end != None else start

def iline_ok(iline):
    """Return True if iline address is in buffer, always False for empty buffer
    Used by most commands, which don't make sense for an empty buffer"""
    return (0 < iline <= buf.nlines()) 

def iline_ok0(iline):
    """Return True if iline address is in buffer, or iline is 0 for start 
    Used by commands which make sense for an empty buffer: insert, append, read
    """
    return (0 <= iline <= buf.nlines())

def range_ok(start, end):
    'Return True if start and end are in buffer, and start does not follow end'
    return iline_ok(start) and iline_ok(end) and start <= end

# parse_check_ functions used by many commands to parse line address args,
# replace missing args by defaults, check args, and print error messages.

def parse_check_line(ok0, args):
    'Building block for parse_check_... functions'
    iline, _, param, _ = parse_args(args)
    iline = mk_iline(iline)
    valid = iline_ok0(iline) if ok0 else iline_ok(iline)
    if not valid:
        print('? invalid address')
    return valid, iline, param

def parse_check_iline(args):
    'for commands that use one line address where 0 is not valid: k z'
    return parse_check_line(False, args)

def parse_check_iline0(args):
    'for commands that use one line address where 0 is valid: r a i'
    return parse_check_line(True, args)

def parse_check_range(args):
    'for cmds that can affect a range of lines: p d c s'
    start, end, param, param_list = parse_args(args)
    start, end = mk_range(start, end)
    valid = range_ok(start, end)
    if not valid:
        print('? invalid address')
    return valid, start, end, param, param_list

def parse_check_range_dest(args):
    'for cmds that can affect a range of lines and a destination: m t'
    valid, start, end, dest, x = parse_check_range(args)
    if valid:
        dest, x = match_address(dest)
        # dest can be 0 because lines are moved to *after* dest
        dest_valid = iline_ok0(dest)
        if not dest_valid:
            print('? invalid destination')
    return (valid and dest_valid), start, end, dest

def match_prefix(prefix, names):
    """
    If prefix ends with -, return name (if any) that matches, 
    otherwise return same prefix.  'Poor person's tab completion'.
    """
    if isinstance(prefix, str) and prefix.endswith('-'): # might be None
        for n in names:
            if n.startswith(prefix[:-1]):
                return n
    return prefix


# data structures and variables

# Each ed command is implemented by a function with the same
# one-letter name, whose arguments are the same as the ed command
# args.  The current buffer is used by many of these functions but to
# make the API similar to ed commands, it cannot appear as an arg. 
# So the current buffer, buf, must be global.

# initialize these with create_buf
buf = None
current = str()
buffers = dict() # dict from buffer names (strings) to Buffer instances

# line addresses

def o(): # looks like ed .
    'Return index of the current line (called dot), 0 if the buffer is empty'
    return buf.dot

def S(): # looks like ed $
    'Return index of the last line, 0 if the buffer is empty'
    return buf.nlines()

def k(*args):
    """
    Mark addressed line in this buffer with character c (command parameter),
    to use with 'c address form.  'c address identifies both buffer and line.
    """
    valid, iline, marker = parse_check_iline(args)
    if valid:
        c = marker[0]
        buf.mark[c] = iline
        print("Mark %s set at line %d in buffer %s" % (c, iline, current))

# search

def F(pattern):
    """Forward Search for pattern, 
    return line number where found, dot if not found"""
    return buf.F(pattern)

def R(pattern):
    """Backward search for pattern, 
    return line number where found, dot if not found"""
    return buf.R(pattern)

def current_filename(filename):
    """
    Return filename arg if present, if not return current filename.
    Do not change current filename, assign only if it was previously absent.
    """
    if filename:
        if not buf.filename:
            buf.filename = filename
        return filename
    if buf.filename:
        return buf.filename 
    print('? no current filename')
    return None

def create_buf(bufname):
    'Create buffer with given name. Replace any existing buffer with same name'
    global current, buf
    buf = buffer.Buffer(bufname)
    buffers[bufname] = buf # replace buffers[bufname] if it already exists
    current = bufname
    update(Op.create, buffer=buf)

def select_buf(bufname):
    'Make buffer with given name the current buffer'
    global current, buf
    current = bufname
    buf = buffers[current]
    update(Op.select, buffer=buf)

def b(*args):
    """
    Set current buffer to name.  If no buffer with that name, create one.
    Then print current buffer name.  If none given, print current name + info
    """
    global current, buf
    _, _, bufname, _ = parse_args(args)
    bufname = match_prefix(bufname, buffers)
    if bufname in buffers:
        select_buf(bufname)
    elif bufname:
        create_buf(bufname)
        buf.filename = bufname
    print('.' + buf.info()) # even if no bufname given

def r_new(bufname, filename):
    'Create new buffer, Read in file contents'
    create_buf(bufname)
    buf.filename = filename
    r(0, filename)
    buf.unsaved = False # insert in r sets unsaved = True, this is exception

def f(*args):
    'set default filename, if filename not specified print current filename'
    _, _, filename, _ = parse_args(args)
    if filename:
        buf.f(filename)
    elif buf.filename:
        print(buf.filename)
    else:
        print('? no current filename')

def E(*args):
    'read in file, replace buffer contents despite unsaved changes'
    _, _, filename, _ = parse_args(args)
    if not filename:
        filename = buf.filename
    if not filename:
        print('? no current filename')
        return
    buf.d(1, buf.nlines())
    r(0, filename)
    buf.unsaved = False

def e(*args):
    'read in file, replace buffer contents unless unsaved changes'
    if buf.unsaved:
        print('? warning: file modified')
        return
    E(*args)

def r(*args):
    'Read file contents into buffer after iline'
    valid, iline, fname = parse_check_iline0(args)
    if valid:
        filename = current_filename(fname)
        if filename:
            nlines0 = buf.nlines()
            buf.r(iline, filename)
            print('%s, %d lines' % (filename, buf.nlines() - nlines0))

def B(*args):
    'Create new Buffer and load the named file. Buffer name is file basename'
    _, _, filename, _ = parse_args(args)
    if not filename:
        print('? file name')
        return
    bufname = os.path.basename(filename) # may differ from filename
    if bufname in buffers:
        # FIXME? create new buffer name a la emacs name<1>, name<2> etc.
        print('? buffer name %s already in use' % bufname)
        return
    r_new(bufname, filename)

def w(*args):
    'write current buffer contents to file name'
    _, _, fname, _ = parse_args(args)
    filename = current_filename(fname)
    if filename: # if not, current_filename printed error msg
        buf.w(filename)
        print('%s, %d lines' % (filename, buf.nlines()))

D_count = 0 # number of consecutive times D command has been invoked

def D(*args):
    'Delete the named buffer, if unsaved changes print message and exit'
    global D_count
    _, _, bufname, _ = parse_args(args)
    name = bufname if bufname else current
    if name in buffers and buffers[name].unsaved and not D_count:
        print('? unsaved changes, repeat D to delete')
        D_count += 1 # must invoke D twice to confirm, see message below
        return
    DD(*args)

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    global current, buf
    _, _, bufname, _ = parse_args(args)
    name = bufname if bufname else current
    if not name in buffers:
        print('? buffer name')
    elif name == 'main':
        print("? Can't delete main buffer")
    else:
        delbuf = buffers[name]
        del buffers[name]
        if name == current: # pick a new current buffer
            keys = list(buffers.keys()) # always nonempty due to main
            select_buf(keys[0])
        update(Op.remove, sourcebuf=delbuf, buffer=buf)
        print('%s, buffer deleted' % name)

# Displaying information

def A(*args):
    ' = in command mode, print the line number of the addressed line'
    iline, _, _, _ = parse_args(args)
    iline = iline if iline != None else buf.nlines() # default $ not .
    if iline_ok0(iline): # don't print error message when file is empty
        print(iline)
    else:
        print('? invalid address')

def n(*args):
    'Print information about all buffers'
    print('C M Buffer            Size  File') # C current  M modified (unsaved)
    for name in buffers:
        print (('.' if name == current else ' ') + buffers[name].info())
    
# Displaying and navigating text
    
def l(*args):
    'Advance dot to iline and print it'
    iline, _, _, _ = parse_args(args)
    if not buf.lines:
        print('? empty buffer')
        return
    # don't use usual default dot here, instead advance dot
    if iline == None:
        iline = buf.dot + 1
    if not iline_ok(iline):
        print('? invalid address')
        return
    print(buf.l(iline), file=lz_print_dest) # null destination suppresses print

def p_lines(start, end, destination): # arg here shadows global destination
    'Print lines start through end, inclusive, at destination'
    for iline in range(start, end+1): # +1 because start,end is inclusive
        print(buf.l(iline), file=destination) # file can be null or stdout or..

def p(*args):
    'Print lines from start up to end, leave dot at last line printed'
    valid, start, end, _, _ = parse_check_range(args)
    if valid:
        p_lines(start, end, sys.stdout) # print unconditionally
    
def z(*args):
    """
    Scroll: print buf.npage lines, scroll backwards if npage is negative.
    If parameter is present, update buf.npage
    If npage is non-negative, start at iline, leave dot at last line printed.
    if npage is negative, start at iline+npage, leave dot at first line printed
    """
    valid, iline, npage_string = parse_check_iline(args)
    if valid: 
        if npage_string:
            try:
                npage = int(npage_string)
            except:
                print('? integer expected at %s' % npage_string)
                return 
            buf.npage = npage
        if buf.npage >= 0:
            end = iline + buf.npage 
        else:
            end = iline
            iline += buf.npage # npage negative, go backward
            iline = iline if iline > 0 else 1
        end = end if end <= buf.nlines() else buf.nlines()
        p_lines(iline, end, lz_print_dest) # null destination suppresses print
        if buf.npage < 0:
            buf.dot = iline

# Adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    valid, iline, lines = parse_check_iline0(args)
    if valid and lines:
        buf.a(iline, lines)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    valid, iline, lines = parse_check_iline0(args)
    if valid and lines:
        buf.i(iline, lines)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes'
    valid, start, end, _, _ = parse_check_range(args)
    if valid:
        buf.d(start, end)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    valid, start, end, lines, _ = parse_check_range(args)
    if valid:
        buf.c(start,end,lines)
        
def s(*args):
    """
    Substitute new for old in lines from start up to end.
    When glbl is False (the default), substitute only the first occurrence 
    in each line.  Otherwise substitute all occurrences in each line
    """
    valid, start, end, old, params = parse_check_range(args)
    if valid:
        # params might be [ new, glbl ]
        if old and len(params) > 0 and isinstance(params[0],str):
            new = params[0]
        else:
            print('? /old/new/')
            return
        if len(params) > 1:
            glbl = bool(params[1])
        else:
            glbl = False # default
        buf.s(start, end, old, new, glbl)

def m(*args):
    'move lines to after destination line'
    valid, start, end, dest = parse_check_range_dest(args)
    if valid:
        if (start <= dest <= end):
            print('? invalid destination')
            return
        buf.m(start, end, dest)

def t(*args):
    'transfer (copy) lines to after destination line'
    valid, start, end, dest = parse_check_range_dest(args)
    if valid:
        buf.t(start, end, dest)

def y(*args):
    'Insert most recently deleted lines *before* destination line address'
    iline, _, _, _ = parse_args(args)
    iline = mk_iline(iline)
    if not (0 <= iline <= buf.nlines()+1): # allow +y at $ to append to buffer
        print('? invalid address')
        return
    buf.y(iline)

quit = False

def q(*args):
    'quit command mode, ignore args, caller quits'
    global quit
    quit = True

complete_cmds = 'AbBdDeEfklmnpqrstwxXyz' # commands that require no more input
input_cmds = 'aci' # commands that use input mode to collect text
ed_cmds = complete_cmds + input_cmds

# regular expressions for line address forms and other command parts
number = re.compile(r'(\d+)')
fwdnumber = re.compile(r'\+(\d+)')
bkdnumber = re.compile(r'\-(\d+)')
bkdcnumber = re.compile(r'\^(\d+)')
plusnumber = re.compile(r'(\++)')
minusnumber = re.compile(r'(\-+)')
caratnumber = re.compile(r'(\^+)')
fwdsearch = re.compile(r'/(.*?)/') # non-greedy *? for /text1/,/text2/
bkdsearch = re.compile(r'\?(.*?)\?')
text = re.compile(r'(.*)') # nonblank
mark = re.compile(r"'([a-z])")  # 'c, ed mark with single lc char label

def match_address(cmd_string):
    """
    Return line number for address at start of cmd_string (None of not found), 
     and rest of cmd_string.
    This is where we convert the various line address forms to line numbers.
    All other code in this module and the buffer module uses line numbers only.
    """
    if cmd_string == '':
        return None, '' 
    if cmd_string[0] == '.': # current line
        return buf.dot, cmd_string[1:]
    if cmd_string[0] == '$': # last line
        return buf.nlines(), cmd_string[1:]
    if cmd_string[0] == ';': # equivalent to .,$  - current line to end
        return buf.dot, ',$'+ cmd_string[1:]
    if cmd_string[0] in ',%': # equivalent to 1,$ - whole buffer
        return 1, ',$'+ cmd_string[1:]
    m = number.match(cmd_string) # digits, the line number
    if m:
        return int(m.group(1)), cmd_string[m.end():]
    m = fwdnumber.match(cmd_string) # +digits, relative line number forward
    if m:
        return buf.dot + int(m.group(1)), cmd_string[m.end():]
    m = bkdnumber.match(cmd_string) # -digits, relative line number backward
    if m:
        return buf.dot - int(m.group(1)), cmd_string[m.end():]
    m = bkdcnumber.match(cmd_string) # ^digits, relative line number backward
    if m:
        return buf.dot - int(m.group(1)), cmd_string[m.end():]
    m = plusnumber.match(cmd_string) # + or ++ or +++ ...
    if m:
        return buf.dot + len(m.group(0)), cmd_string[m.end():]
    m = minusnumber.match(cmd_string) # digits, the line number
    if m:
        return buf.dot - len(m.group(0)), cmd_string[m.end():]
    m = caratnumber.match(cmd_string) # digits, the line number
    if m:
        return buf.dot - len(m.group(0)), cmd_string[m.end():]
    m = fwdsearch.match(cmd_string)  # /text/ or // - forward search
    if m: 
        return buf.F(m.group(1)), cmd_string[m.end():]
    m = bkdsearch.match(cmd_string)  # ?text? or ?? - backward search
    if m: 
        return buf.R(m.group(1)), cmd_string[m.end():]
    m = mark.match(cmd_string) # 'c mark with single lc char label
    if m: 
        c = m.group(1)
        i = buf.mark[c] if c in buf.mark else -9999 # invalid address
        return i, cmd_string[m.end():] 
    return None, cmd_string

def parse_cmd(cmd_string):
    """
    Parses traditional ed cmd_string, returns multiple values in this order:
     cmd_name - single-character command name
     start, end - integer line numbers 
     params - string containing other command parameters
    All are optional except cmd_name, assigns None if item is not present
    """
    global D_count
    cmd_name, start, end, params = None, None, None, None
    # look for start addr, optional. if no match start,tail == None,cmd_string
    start, tail = match_address(cmd_string)
    # look for end address, optional
    if start != None:
        if tail and tail[0] == ',': # addr separator, next addr NOT optional
            end, tail = match_address(tail[1:])
            if end == None:
                print('? end address expected at %s' % tail)
                return 'ERROR', start, end, params
    # look for cmd_string, NOT optional
    if tail and tail[0] in ed_cmds:
        cmd_name, params = tail[0], tail[1:].strip()
    # special case command names
    elif tail == '':
        cmd_name = 'l' # default for empty cmd_string
    elif tail[0] == '=':
        cmd_name = 'A'
    else:
        print('? command expected at %s' % tail)
        return 'ERROR', start, end, params
    # special handling for commands that must be repeated to confirm
    D_count = 0 if cmd_name != 'D' else D_count
    # command-specific parameter parsing
    if cmd_name == 's' and len(params.split('/')) == 4: #s/old/new/g,g optional
        empty, old, new, glbl = params.split('/') # glbl == '' when g absent
        return cmd_name, start, end, old, new, glbl
    # all other commands, no special parameter parsing
    else:
        # return each space-separated parameter as separate arg in sequence
        return (cmd_name,start,end) + (tuple(params.split() if params else ()))

# State variables that must persist between cmd invocations during input mode
command_mode = True # alternates with input mode used by a,i,c commands
cmd_name = '' # command name, must persist through input mode
args = []  # command arguments, must persist through input mode

# Assigned by cmd before command executes, before any insertions or deletions
start = 0  # line address, first line of affected region, often dot
end = 0    # line address, last line of affected region
dest = 0   # line address, destination for m(ove), t(ransfer, copy) commands

pysh = pysh.mk_shell() # embedded Python shell for ! command

def do_command(line):
    """
    Process one input line without blocking in ed command or input mode
    Update buffers and control variables: command_mode,cmd_name,args,start,end
    """
    global command_mode, cmd_name, args, start, end, dest
    if command_mode:
        # special prefix characters, don't parse these lines
        if line and line[0] == '#': # comment
            return 
        if line and line[0] == '!': 
            pysh(line[1:]) # execute Python expression or statement
            return
        items = parse_cmd(line)
        if items[0] == 'ERROR':
            return None # parse_cmd already printed message
        else:
            tokens = tuple([ t for t in items if t != None ])
        cmd_name, args = tokens[0], tokens[1:]
        start, end, dest, _ = parse_args(args) # might be int or None
        start, end = mk_range(start, end) # int only
        dest,_ = (None,None) if dest is None else match_address(dest) #str->int
        if cmd_name in complete_cmds:
            globals()[cmd_name](*args) # dict from name (str) to object (fcn)
        elif cmd_name in input_cmds:
            command_mode = False # enter input mode
            # Instead of using buf.a,i,c, we handle input mode cmds inline here
            # We add each line to buffer when user types RET at end-of-line,
            # *unlike* in Python API where we pass multiple input lines at once
            if not (iline_ok0(start) if cmd_name in 'ai'
                    else range_ok(start, end)):
                print('? invalid address')
                command_mode = True
            # assign dot to prepare for input mode, where we a(ppend) each line
            elif cmd_name == 'a':
                buf.dot = start
                update(Op.input)
            elif cmd_name == 'i': #and start >0: NOT! can insert in empty file
                buf.dot = start - 1 if start > 0 else 0 
                # so we can a(ppend) instead of i(nsert)
                update(Op.input)
            elif cmd_name == 'c': #c(hange) command deletes changed lines first
                buf.d(start, end) # d updates buf.dot, calls update(Op.delete).
                buf.dot = start - 1 # supercede dot assigned in preceding
                update(Op.input)  # queues Op.input after Op.delete from buf.d
            else:
                print('? command not supported in input mode: %s' % cmd_name)
        else:
            print('? command not implemented: %s' % cmd_name)
        return
    else: # input mode for a,i,c commands that collect text
        if line == '.':
            command_mode = True # exit input mode
            update(Op.command) # return from input (insert) mode to cmd mode
        else:
            # Recall raw_input returns each line with final \n stripped off,
            # BUT buf.a requires \n at end of each line
            buf.a(buf.dot, line + '\n') # append new line after dot,advance dot
        return

def do_commands(do_command, lines, echo, delay):
    """
    Execute a sequence of command lines.
     do_command - function to call on each line to execute one command
     lines - list of lines, one command per line
     echo - if True, print each line before executing it
     delay - if not None, wait delay seconds after printing each line
    This function *blocks* each time it reaches time.sleep(delay)
    """
    for line in lines:
        line1 = line.rstrip() # remove terminal \n
        if echo: 
            print(line1)
        do_command(line1) 
        if delay and delay > 0:
            time.sleep(delay)

falses, trues = ('0','f','F','False'), ('1','t','T','True')
booleans = falses + trues

def parse_echo_delay(params):
    'Parse echo and delay from params, a sequence of 0, 1, or 2 strings'
    valid, echo, delay = True, None, None
    if params:
        if params[0] in booleans:
            echo = False if params[0] in falses else True
        else:
            print('%s ? echo, 0 f F False or 1 t T True expected' % params[0])
            valid = False
        if len(params) > 1:
            try:
                delay = float(params[1])
            except ValueError:
                print('%s ? delay, float expected' % params[1])
                valid = False
    return valid, echo, delay

def x(*args):
    """
    Execute ed commands in another buffer: x(bufname, echo, delay)
     No start, end arugments - the range is always the entire buffer.
     bufname is not optional - it cannot be the current buffer.
     echo - optional, default True; delay - optional, default 0.2 sec
    """
    _, _, bufname, params = parse_args(args)
    bufname = match_prefix(bufname, buffers)
    if bufname in buffers:
        valid, echo, delay = parse_echo_delay(params)
        if valid:
            echo = echo if echo != None else True
            delay = delay if delay != None else 0.2
            do_commands(x_cmd_fcn, buffers[bufname].lines[1:], echo, delay)
            # cmds in buffer advance dot
    else:
        print('? buffer name')

def X(*args):
    """
    Execute Python statements in the current buffer: X(start, end, echo, delay)
     start, end default to dot, so X cmd without range single-steps thru buffer
     echo - optional, default False; delay - optional, default no delay
    Leaves dot at last line executed, to single-step through file, repeat +X
    """
    valid,start,end,echo,delay_singleton = parse_check_range(args) # no bufname
    if valid:
        # delay if present is in a singleton tuple. If echo absent, so is delay
        params = (echo,)+delay_singleton if echo else ()
        params_valid, echo, delay = parse_echo_delay(params)
        if params_valid:
            echo = echo if echo != None else False
            delay = delay if delay != None else None
            do_commands(pysh, buffers[current].lines[start:end+1], echo, delay)
            buffers[current].dot = end 

# Hooks to configure ed behavior for display editor
x_cmd_fcn = do_command  # default: ed do_command does not update display etc.
lz_print_dest = sys.stdout  # default: l and z commands print in scroll region
def update(op, **kwargs): pass # default: ed has no display,update does nothing

def configure(cmd_fcn=None, update_fcn=None, print_dest=None):
    'Call from display editor to configure ed behavior'
    global x_cmd_fcn, lz_print_dest, update
    if cmd_fcn: x_cmd_fcn = cmd_fcn
    if print_dest: lz_print_dest = print_dest
    if update_fcn: 
        update = update_fcn
        buffer.update = update_fcn

prompt = '' # default no prompt

def startup(*filename, **options):
    global quit, prompt
    create_buf('main')
    quit = False # allow restart
    if filename:
        e(filename[0])
    if 'p' in options:
        prompt = options['p'] 

def main(*filename, **options):
    """
    Top level ed command to invoke from Python prompt or command line.
    Won't work with cooperative multitasking, calls blocking input().
    """
    startup(*filename, **options)
    while not quit:
        prompt_string = prompt if command_mode else ''
        line = input(prompt_string) # blocking
        do_command(line) # non-blocking

def cmd_options():
    # import argparse inside this fcn so it isn't always a dependency.
    import argparse
    parser = argparse.ArgumentParser(description='editor in pure Python based on classic Unix ed')
    parser.add_argument('file', 
                        help='name of file to load into main buffer at startup (omit to start with empty main buffer)',
                        nargs='?',
                        default=None),
    parser.add_argument('-p', '--prompt', help='command prompt string (default no prompt)',
                        default='')
    parser.add_argument('-c', '--cmd_h', help='number of lines in scrolling command region (display editor only, default 2)',
                        type=int, default=2)
    args = parser.parse_args()
    filename = [args.file] if args.file else []
    options = {'p': args.prompt } if args.prompt else {}
    options.update({'c': args.cmd_h } if args.cmd_h else {})
    return filename, options

if __name__ == '__main__':
    filename, options = cmd_options()
    main(*filename, **options)
