"""
ed.py - line-oriented text editor in pure Python based on classic Unix ed.

This module provides both the classic command interface and the public
Python API.  It imports buffer.py which defines the Buffer class that
provides the core data structure and the internal API.

For more explanation see ed.md, ed.txt, the docstrings here, and the tests
in test/ed/
"""

import re, os, sys
import pysh  # provides embedded Python shell for ! command
import buffer

destination = sys.stdout # can redirect l z cmd output to os.devnull etc.

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


# central data structure and variables

buffers = dict() #  dict from buffer names (strings) to Buffer instances

# There is always a current buffer so we can avoid check for special case
# Start with one empty buffer named 'main', can't ever delete it
current = 'main'
buf = buffer.Buffer(current)  
buffers[current] = buf 


# line addresses

def o():
    'Return index of the current line (called dot), 0 if the buffer is empty'
    return buf.dot

def S():
    'Return index of the last line, 0 if the buffer is empty'
    return buf.S()


# search

def F(pattern):
    """Forward Search for pattern, 
    return line number where found, dot if not found"""
    return buf.F(pattern)

def R(pattern):
    """Backward search for pattern, 
    return line number where found, dot if not found"""
    return buf.R(pattern)


# buffers and files

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

def b_new(name):
    'Create buffer with given name. Replace any existing buffer with same name'
    global current, buf
    buf = buffer.Buffer(name)
    buffers[name] = buf # replace buffers[name] if it already exists
    current = name

def b(*args):
    """
    Set current buffer to name.  If no buffer with that name, create one.
    If no name given, print the name of the current buffer.
    """
    global current, buf
    x, xx, name, xxx = parse_args(args)
    if not name:
        print_status(current, o())
    elif name in buffers:
        current = name
        buf = buffers[current]
    else:
        b_new(name)

def r_new(buffername, filename):
    'Create new buffer, Read in file contents'
    b_new(buffername)
    buf.filename = filename
    r(0, filename)
    buf.unsaved = False # insert in r sets unsaved = True, this is exception

def f(*args):
    'set default filename, if filename not specified print current filename'
    x, xx, filename, xxx = parse_arg(args)
    if filename:
        buf.f(filename)
        return
    if buf.filename:
        print(buf.filename)
        return
    print('? no current filename')

def E(*args):
    'read in file, replace buffer contents despite unsaved changes'
    x, xx, filename, xxx = parse_args(args)
    if not filename:
        filename = buf.filename
    if not filename:
        print('? no current filename')
        return
    r_new(current, filename) # replace previous current buffer with new

def e(*args):
    'read in file, replace buffer contents unless unsaved changes'
    if buf.unsaved:
        print('? warning: file modified')
        return
    E(*args)

def r(*args):
    'Read file contents into buffer after iline'
    start, x, name, xx = parse_args(args)
    filename = current_filename(name)
    if not filename:
        return # current_filename already printed error msg
    iline = buf.mk_start(start)
    if not buf.start_empty_ok(iline): # r command works even for empty buffer
        print('? invalid address')
        return
    S0 = S() # record number of lines now to calc how many we read
    buf.r(iline, filename)
    print('%s, %d lines' % (filename, S()-S0))

def B(*args):
    'Create new Buffer and load the named file. Buffer name is file basename'
    x, xx, filename, xxx = parse_args(args)
    if not filename:
        print('? file name')
        return
    buffername = os.path.basename(filename) # may differ from filename
    if buffername in buffers:
        # FIXME? create new buffername a la emacs name<1>, name<2> etc.
        print('? buffer name %s already in use' % buffername)
        return
    r_new(buffername, filename)

def w(*args):
    'write current buffer contents to file name'
    x, xx, name, xxx = parse_args(args)
    filename = current_filename(name)
    if not filename:
        return # current_filename already printed error msg
    buf.w(filename)
    print('%s, %d lines' % (filename, S()))

D_count = 0 # number of consecutive times D command has been invoked

def D(*args):
    'Delete the named buffer, if unsaved changes print message and exit'
    global D_count
    x, xx, text, xxx = parse_args(args)
    name = text if text else current
    if name in buffers and buffers[name].unsaved and not D_count:
        print('? unsaved changes, repeat D to delete')
        D_count += 1 # must invoke D twice to confirm, see message below
        return
    DD(*args)

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    global current, buf
    x, xx, text, xxx = parse_args(args)
    name = text if text else current
    if not name in buffers:
        print('? buffer name')
    elif name == 'main':
        print("? Can't delete main buffer")
    else:
        del buffers[name]
        if name == current: # pick a new current buffer
            keys = list(buffers.keys())
            current = keys[0] if keys else None
            buf = buffers[current]
        print('%s, buffer deleted' % name)


# Displaying information

def print_status(bufname, iline):
    'used by e and n, given bufname and iline prints dot, $, filename, unsaved'
    ibuf = buffers[bufname] # avoid name confusion with global buf
    loc = '%s/%d' % (iline, len(ibuf.lines)-1) # don't count empty first line
    print('%7s  %s%s%-12s  %s' % (loc, 
                               '.' if bufname == current else ' ',
                               '*' if ibuf.unsaved else ' ', 
                               bufname, (ibuf.filename if ibuf.filename else 
                                         'no current filename')))

def A(*args):
    ' = in command mode, print the line number of the addressed line'
    start, x, xx, xxx = parse_args(args)
    iline = start if start != None else S() # default $ not .
    if buf.start_empty_ok(iline): # don't print error message when file is empty
        print(iline)
    else:
        print('? invalid address')

def n(*args):
    'Print status of all buffers'
    print("""    ./$    Buffer        File
    ---    ------        ----""")
    for name in buffers:
        print_status(name, buffers[name].dot)
    

# Displaying and navigating text
    
def l(*args):
    'Advance dot to iline and print it'
    iline, x, xx, xxx = parse_args(args)
    if not buf.lines:
        print('? empty buffer')
        return
    # don't use usual default dot here, instead advance dot
    if iline == None:
        iline = o() + 1
    if not buf.start_ok(iline):
        print('? invalid address')
        return
    print(buf.l(iline), file=destination) # can redirect to os.devnull etc.

def p_lines(ifirst,ilast):
    'Print line numbers ifirst through ilast, inclusive, without arg checking'
    for iline in range(ifirst,ilast+1): # +1 because ifirst,ilast is inclusive
        print(buf.l(iline), file=destination) # can redirect to os.devnull etc.

def p(*args):
    'Print lines from start up to end, leave dot at last line printed'
    istart, jend, x, xx = parse_args(args)
    start, end = buf.mk_range(istart, jend)
    if not buf.range_ok(start, end):
        print('? invalid address')
        return
    p_lines(start, end)
    
def z(*args):
    """
    Scroll: print buf.npage lines starting at iline.
    Leave dot at last line printed. If parameter is present, update buf.npage
    """
    start, x, npage_string, xxx = parse_args(args)
    #print('start %s, npage_string %s' % (start, npage_string))#DEBUG
    iline = buf.mk_start(start)
    if not buf.start_empty_ok(iline):
        print('? invalid address')
        return
    if npage_string:
        try:
            npage = int(npage_string)
        except:
            print('? integer expected: %s' % npage_string)
            return 
        if npage < 1:
            print('? integer > 1 expected %d' % npage)
            return
        buf.npage = npage
    end = iline + buf.npage 
    end = end if end <= S() else S()
    p_lines(iline, end)


# Adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    ai_cmd(buf.a, args)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    ai_cmd(buf.i, args)

def ai_cmd(cmd_fcn, args):
    'a(ppend) or i(nsert) command'
    start, x, text, xx = parse_args(args)
    iline = buf.mk_start(start)
    if not buf.start_empty_ok(iline): # a, i commands work even for empty buffer
        print('? invalid address')
        return
    if text:
        cmd_fcn(iline, text)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes or...'
    start, end, x, xxx = parse_args(args)
    istart, iend = buf.mk_range(start, end)
    if not buf.range_ok(istart, iend):
        print('? invalid address')
        return
    buf.d(istart, iend)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    start, end, text, x = parse_args(args)
    istart, iend = buf.mk_range(start, end)
    if not buf.range_ok(istart, iend):
        print('? invalid address')
        return
    buf.c(istart,iend,text)
        
def s(*args):
    """
    Substitute new for old in lines from start up to end.
    When glbl is False (the default), substitute only the first occurrence 
    in each line.  Otherwise substitute all occurrences in each line
    """
    start, end, old, params = parse_args(args)
    istart, iend = buf.mk_range(start, end)
    if not buf.range_ok(istart, iend):
        print('? invalid address')
        return
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
    buf.s(istart, iend, old, new, glbl)


# command mode

quit = False

def q(*args):
    'quit command mode, ignore args, caller quits'
    global quit
    quit = True

complete_cmds = 'deEflpqrswzbBDnA' # commands that do not require further input
input_cmds = 'aic' # commands that use input mode to collect text
ed_cmds = complete_cmds + input_cmds

# regular expressions for command parts, no spaces allowed
number = re.compile(r'(\d+)')
fwdnumber = re.compile(r'\+(\d+)')
bkdnumber = re.compile(r'\-(\d+)')
bkdcnumber = re.compile(r'\^(\d+)')
fwdsearch = re.compile(r'/(.*?)/') # non-greedy *? for /text1/,/text2/
bkdsearch = re.compile(r'\?(.*?)\?')
text = re.compile(r'(.*)') # nonblank

def match_address(cmd_string):
    """
    return line number at start of cmd_string (None of not found), 
     and rest of cmd_string
    """
    if cmd_string == '':
        return None, '' 
    if cmd_string[0] == '.': # current line
        return o(), cmd_string[1:]
    if cmd_string[0] == '$': # last line
        return S(), cmd_string[1:]
    if cmd_string[0] == ';': # equivalent to .,$  - current line to end
        return o(), ',$'+ cmd_string[1:]
    if cmd_string[0] in ',%': # equivalent to 1,$ - whole buffer
        return 1, ',$'+ cmd_string[1:]
    m = number.match(cmd_string) # digits, the line number
    if m:
        return int(m.group(1)), cmd_string[m.end():]
    m = fwdnumber.match(cmd_string) # +digits, relative line number forward
    if m:
        return o() + int(m.group(1)), cmd_string[m.end():]
    m = bkdnumber.match(cmd_string) # -digits, relative line number backward
    if m:
        return o() - int(m.group(1)), cmd_string[m.end():]
    m = bkdcnumber.match(cmd_string) # ^digits, relative line number backward
    if m:
        return o() - int(m.group(1)), cmd_string[m.end():]
    m = fwdsearch.match(cmd_string)  # /text/ or // - forward search
    if m: 
        return buf.F(m.group(1)), cmd_string[m.end():]
    m = bkdsearch.match(cmd_string)  # ?text? or ?? - backward search
    if m: 
        return buf.R(m.group(1)), cmd_string[m.end():]
    # FIXME - also handle -n +n 'c 
    return None, cmd_string

def parse_cmd(cmd_string):
    """
    Parses cmd_string, returns multiple values in this order:
     cmd_name - single-character command name
     istart, jend - integer line numbers 
     params - string containing other command parameters
    All are optional except cmd_name, assigns None if item is not present
    """
    global D_count
    cmd_name, istart, jend, params = None, None, None, None
    # look for start addr, optional. if no match istart,tail == None,cmd_string
    istart, tail = match_address(cmd_string)
    # look for end address, optional
    if istart != None:
        if tail and tail[0] == ',': # addr separator, next addr NOT optional
            jend, tail = match_address(tail[1:])
            if jend == None:
                print('? end address expected at %s' % tail)
                return 'ERROR', istart, jend, params
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
        return 'ERROR', istart, jend, params
    # special handling for commands that must be repeated to confirm
    D_count = 0 if cmd_name != 'D' else D_count
    # command-specific parameter parsing
    if cmd_name == 's' and len(params.split('/')) == 4: # s/old/new/g, g optional
        empty, old, new, glbl = params.split('/') # glbl == '' when g absent
        return cmd_name, istart, jend, old, new, glbl
    # all other commands, no special parameter parsing
    else:
        return cmd_name, istart, jend, params if params else None 

# state variables that must persist between ed_cmd invocations during input mode
command_mode = True # alternates with input mode used by a,i,c commands
cmd_name = '' # command name, must persist through input mode
args = []  # command arguments, must persist through input mode

pysh = pysh.mk_shell() # embedded Python shell for ! command

def cmd(line):
    """
    Process one input line without blocking in ed command or input mode
    Update buffers and control state variables: command_mode, cmd_name, args
    """
    # state variables that must persist between cmd invocations during input mode
    global command_mode, cmd_name, args
    if command_mode:
        if line and line[0] == '!': # special case - not a 1-char cmd_name
            pysh(line[1:]) # execute Python expression or statement
            return
        items = parse_cmd(line)
        if items[0] == 'ERROR':
            return None # parse_cmd already printed message
        else:
            tokens = tuple([ t for t in items if t != None ])
        cmd_name, args = tokens[0], tokens[1:]
        if cmd_name in complete_cmds:
            globals()[cmd_name](*args) # dict from name (string) to object (fcn)
        elif cmd_name in input_cmds:
            command_mode = False # enter input mode
            # Instead of using buf.a, i, c, we handle input mode cmds inline here
            # We will add each line to buffer when user types RET at end-of-line,
            # *unlike* in Python API where we pass multiple input lines at once.
            istart, jend, x, xxx = parse_args(args) # might be int or None
            input_line, end_line = buf.mk_range(istart, jend) # int only
            if not (buf.start_empty_ok(input_line) if cmd_name in 'ai'
                    else buf.range_ok(input_line, end_line)):
                print('? invalid address')
                command_mode = True
            # assign dot to prepare for input mode, where we a(ppend) each line
            elif cmd_name == 'a':
                buf.dot = input_line
            elif cmd_name == 'i': #and input_line >0: NOT! can insert in empty file
                buf.dot = input_line - 1 if input_line > 0 else 0 
                # so we can a(ppend) instead of i(nsert)
            elif cmd_name == 'c': # c(hange) command deletes changed lines first
                buf.d(input_line, end_line) # updates buf.dot
                buf.dot = input_line - 1
            else:
                print('? command not supported in input mode: %s' % cmd_name)
        else:
            print('? command not implemented: %s' % cmd_name)
        return
    else: # input mode for a,i,c commands that collect text
        if line == '.':
            command_mode = True # exit input mode
        else:
            # Recall raw_input returns each line with final \n stripped off,
            # BUT buf.a requires \n at end of each line
            buf.a(o(), line + '\n') # append new line after dot, advance dot
        return

prompt = '' # default no prompt

def main(*filename, **options):
    """
    Top level ed command to use at Python prompt.
    This version won't work in Piety, it calls blocking command raw_input
    """
    global cmd_name, quit, prompt
    quit = False # allow restart
    if filename:
        e(filename[0])
    if 'p' in options:
        prompt = options['p'] 
    while not quit:
        line = input(prompt) # blocking
        cmd(line) # non-blocking

# Run the editor from the system command line:  python ed.py

if __name__ == '__main__':
    main()
