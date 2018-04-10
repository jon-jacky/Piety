"""
ed.py - line-oriented text editor in pure Python based on classic Unix ed
"""

import re, os, sys
from enum import Enum
import parse, check, buffer, view
from updates import Op

# Each ed command is implemented here by a command function with the same
# one-letter name, whose arguments are the same as the ed command args.
# The current buffer is used by many of these functions, but to
# make the API similar to ed commands, it cannot appear as an argument.
# So the current buffer, buf, must be global.  The command functions
# form an API that can be used without running the ed command line, 
# so each command function must gather and check its own arguments.

# Data structures and variables. Initialize these with create_buf (below)
buf = None       # current buffer
current = str()  # name of current buffer
buffers = dict() # dict from buffer names (strings) to Buffer instances

# helper functions: line addresses

def o(): # looks like ed .
    'Return index of the current line (called dot), 0 if the buffer is empty'
    return buf.dot

def S(): # looks like ed $
    'Return index of the last line, 0 if the buffer is empty'
    return buf.nlines()

# helper functions: search

def F(pattern):
    """Forward Search for pattern, 
    return line number where found, dot if not found"""
    return buf.F(pattern)

def R(pattern):
    """Backward search for pattern, 
    return line number where found, dot if not found"""
    return buf.R(pattern)

# helper functions: buffers and files

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
    view.update(Op.create, buffer=buf)

def select_buf(bufname):
    'Make buffer with given name the current buffer'
    global current, buf
    current = bufname
    buf = buffers[current]
    view.update(Op.select, buffer=buf)

# command functions: buffers and files

def b(*args):
    """
    Set current buffer to name.  If no buffer with that name, create one.
    Then print current buffer name.  If none given, print current name + info
    """
    global current, buf
    _, _, bufname, _ = parse.arguments(args)
    bufname = match_prefix(bufname, buffers)
    if bufname in buffers:
        select_buf(bufname)
    elif bufname:
        create_buf(bufname)
        buf.filename = bufname
    print('.' + buf.info()) # even if no bufname given

def f(*args):
    'set default filename, if filename not specified print current filename'
    _, _, filename, _ = parse.arguments(args)
    if filename:
        buf.f(filename)
    elif buf.filename:
        print(buf.filename)
    else:
        print('? no current filename')

def r(*args):
    'Read file contents into buffer after iline'
    valid, iline, fname = check.iline0_valid(buf, args)
    if valid:
        filename = current_filename(fname)
        if filename:
            nlines0 = buf.nlines()
            buf.r(iline, filename)
            print('%s, %d lines' % (filename, buf.nlines() - nlines0))

def E(*args):
    'read in file, replace buffer contents despite unsaved changes'
    _, _, filename, _ = parse.arguments(args)
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

def B(*args):
    'Create new Buffer and load the named file. Buffer name is file basename'
    _, _, filename, _ = parse.arguments(args)
    if not filename:
        print('? file name')
        return
    bufname = os.path.basename(filename) # may differ from filename
    if bufname in buffers:
        # FIXME? create new buffer name a la emacs name<1>, name<2> etc.
        print('? buffer name %s already in use' % bufname)
        return
    create_buf(bufname)
    buf.filename = filename
    r(0, filename)
    buf.unsaved = False # insert in r sets unsaved = True, this is exception

def w(*args):
    'write current buffer contents to file name'
    _, _, fname, _ = parse.arguments(args)
    filename = current_filename(fname)
    if filename: # if not, current_filename printed error msg
        buf.w(filename)
        print('%s, %d lines' % (filename, buf.nlines()))

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    global current, buf
    _, _, bufname, _ = parse.arguments(args)
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
        view.update(Op.remove, sourcebuf=delbuf, buffer=buf)
        print('%s, buffer deleted' % name)

D_count = 0 # number of consecutive times D command has been invoked

def D(*args):
    'Delete the named buffer, if unsaved changes print message and exit'
    global D_count
    _, _, bufname, _ = parse.arguments(args)
    name = bufname if bufname else current
    if name in buffers and buffers[name].unsaved and not D_count:
        print('? unsaved changes, repeat D to delete')
        D_count += 1 # must invoke D twice to confirm, see message below
        return
    DD(*args)

# command functions: displaying information

def A(*args):
    ' = in command mode, print the line number of the addressed line'
    iline, _, _, _ = parse.arguments(args)
    iline = iline if iline != None else buf.nlines() # default $ not .
    if check.iline_ok0(buf, iline): # don't print error message when file is empty
        print(iline)
    else:
        print('? invalid address')

def n(*args):
    'Print information about all buffers'
    print('C M Buffer            Size  File') # C current  M modified (unsaved)
    for name in buffers:
        print (('.' if name == current else ' ') + buffers[name].info())
    
# command functions: displaying and navigating text
    
def l(*args):
    'Advance dot to iline and print it'
    iline, _, _, _ = parse.arguments(args)
    if not buf.lines:
        print('? empty buffer')
        return
    # don't use usual default dot here, instead advance dot
    if iline == None:
        iline = buf.dot + 1
    if not check.iline_ok(buf, iline):
        print('? invalid address')
        return
    print(buf.l(iline), file=view.lz_print_dest)

def p_lines(start, end, destination): # arg here shadows global destination
    'Print lines start through end, inclusive, at destination'
    for iline in range(start, end+1): # +1 because start,end is inclusive
        print(buf.l(iline), file=destination) # file can be null or stdout or..

def p(*args):
    'Print lines from start up to end, leave dot at last line printed'
    valid, start, end, _, _ = check.irange(buf, args)
    if valid:
        p_lines(start, end, sys.stdout) # print unconditionally
    
def z(*args):
    """
    Scroll: print buf.npage lines, scroll backwards if npage is negative.
    If parameter is present, update buf.npage
    If npage is non-negative, start at iline, leave dot at last line printed.
    if npage is negative, start at iline+npage, leave dot at first line printed
    """
    valid, iline, npage_string = check.iline_valid(buf, args)
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
        p_lines(iline, end, view.lz_print_dest)
        if buf.npage < 0:
            buf.dot = iline

# command functions: adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    valid, iline, lines = check.iline0_valid(buf, args)
    if valid and lines:
        buf.a(iline, lines)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    valid, iline, lines = check.iline0_valid(buf, args)
    if valid and lines:
        buf.i(iline, lines)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes'
    valid, start, end, _, _ = check.irange(buf, args)
    if valid:
        buf.d(start, end)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    valid, start, end, lines, _ = check.irange(buf, args)
    if valid:
        buf.c(start,end,lines)
        
def s(*args):
    """
    Substitute new for old in lines from start up to end.
    When glbl is False (the default), substitute only the first occurrence 
    in each line.  Otherwise substitute all occurrences in each line
    """
    valid, start, end, old, params = check.irange(buf, args)
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
    valid, start, end, dest = check.range_dest(buf, args)
    if valid:
        if (start <= dest <= end):
            print('? invalid destination')
            return
        buf.m(start, end, dest)

def t(*args):
    'transfer (copy) lines to after destination line'
    valid, start, end, dest = check.range_dest(buf, args)
    if valid:
        buf.t(start, end, dest)

def y(*args):
    'Insert most recently deleted lines *before* destination line address'
    iline, _, _, _ = parse.arguments(args)
    iline = check.mk_iline(buf, iline)
    if not (0 <= iline <= buf.nlines()+1): # allow +y at $ to append to buffer
        print('? invalid address')
        return
    buf.y(iline)

# command functions: markers

def k(*args):
    """
    Mark addressed line in this buffer with character c (command parameter),
    to use with 'c address form.  'c address identifies both buffer and line.
    """
    valid, iline, marker = check.iline_valid(buf, args)
    if valid:
        c = marker[0]
        buf.mark[c] = iline
        print("Mark %s set at line %d in buffer %s" % (c, iline, current))

# command functions: control, debugging, etc.

def K(): return 1/0  # raise exception on demand, for testing

# control

quit = False

def q(*args):
    'exit from main loop'
    global quit
    quit = True

# Variables that must persist between do_command invocations, imported elsewhere
ps1 = ':' # ed command prompt, named like python prompts sys.ps1 and .ps2
ps2 = ''  # ed input mode prompt, empty
prompt = ps1

class Mode(Enum):
    'edit mode'
    command = 1 # classic ed, most commands
    input = 2   # classic ed a i c commands
    display = 3 # eden display editor, full-screen editing

mode = Mode.command

def do_command(line):
    'Process one line without blocking in ed command or input mode'
    global mode, prompt
    line = line.lstrip()
    if mode == Mode.command:
        if line and line[0] == '#': # comment, do nothing
            return 
        items = parse.command(buf, line)
        if items[0] == 'ERROR':
            return # parse.command already printed error message
        else:
            tokens = tuple([ t for t in items if t != None ])
        cmd_name, args = tokens[0], tokens[1:]
        if cmd_name in parse.complete_cmds:
            globals()[cmd_name](*args) # dict from name (str) to object (fcn)
        elif cmd_name in parse.input_cmds:
            mode = Mode.input
            prompt = ps2
            # Instead of using buf.a,i,c, we handle input mode cmds inline here
            # We add each line to buffer when user types RET at end-of-line,
            # *unlike* in Python API where we pass multiple input lines at once
            start, end, params, _ = parse.arguments(args) # can be int or None
            start, end = check.mk_range(buf, start, end) # int only
            if not (check.iline_ok0(buf, start) if cmd_name in 'ai'
                    else check.range_ok(buf, start, end)):
                print('? invalid address')
                mode = Mode.command # exit input mode
                prompt = ps1
            # assign dot to prepare for input mode, where we a(ppend) each line
            elif cmd_name == 'a':
                buf.dot = start
                view.update(Op.input)
            elif cmd_name == 'i': #and start >0: NOT! can insert in empty file
                buf.dot = start - 1 if start > 0 else 0 
                # so we can a(ppend) instead of i(nsert)
                view.update(Op.input)
            elif cmd_name == 'c': #c(hange) command deletes changed lines first
                buf.d(start, end) # d updates buf.dot, calls update(Op.delete).
                buf.dot = start - 1 # supercede dot assigned in preceding
                view.update(Op.input) # queues Op.input after buf.d Op.delete
            else:
                print('? command not supported in input mode: %s' % cmd_name)
        else:
            print('? command not implemented: %s' % cmd_name)
        return
    else: # input mode for a,i,c commands that collect text
        if line == '.':
            mode = Mode.command # exit input mode
            prompt = ps1
            view.update(Op.command) # return from input mode to cmd mode
        else:
            # Recall raw_input returns each line with final \n stripped off,
            # BUT buf.a requires \n at end of each line
            buf.a(buf.dot, line + '\n') # append new line after dot,advance dot
        return

def cmd_options():
    # import argparse inside this fcn so it isn't always a dependency.
    import argparse
    parser = argparse.ArgumentParser(description='editor in pure Python based on classic Unix ed')
    parser.add_argument('file', 
                        help='name of file to load into main buffer at startup (omit to start with empty main buffer)',
                        nargs='?',
                        default=None),
    parser.add_argument('-p', '--prompt', help="command prompt string (default ':')",
                        default=':')
    parser.add_argument('-c', '--cmd_h', help='number of lines in scrolling command region (display editor only, default 2)',
                        type=int, default=2)
    args = parser.parse_args()
    filename = [args.file] if args.file else []
    options = {'p': args.prompt }
    options.update({'c': args.cmd_h })
    return filename, options

create_buf('main')  # initialize main buffer only once on import

def startup(*filename, **options):
    global ps1, prompt, quit
    if filename:
        e(filename[0])
    if 'p' in options:
        ps1 = options['p'] 
        prompt = ps1
    quit = False
    view.update = view.noupdate
    view.lz_print_dest = sys.stdout

def ed(*filename, **options):
    'Top level ed command to invoke from Python REPL or __main__'
    startup(*filename, **options)
    while not quit:
        line = input(prompt) # blocks!
        do_command(line)

if __name__ == '__main__':
    filename, options = cmd_options()
    ed(*filename, **options)
