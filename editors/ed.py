"""
ed.py - line-oriented text editor in pure Python based on classic Unix ed
"""

import re, os, sys
from enum import Enum
from contextlib import redirect_stdout
import parse, check, buffer, view
from updates import Op

# Each ed command is implemented here by a command function with the same
# one-letter name, whose arguments are the same as the ed command args.
# The current buffer is used by many of these functions, but to
# make the API similar to ed commands, it cannot appear as an argument.
# So the current buffer, buf, must be global.  The command functions
# must form an API that can be used without running the ed command line, 
# so each command function must gather and check its own arguments.

# Data structures and variables. Initialize these with create_buf (below)
buf = None       # current buffer
previous = str() # name of previous buffer
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

def bufs_for_file(filename):
    'Return list of names of buffers editing filename, empty list if none'
    return [ buffers[b].name for b in buffers
             if buffers[b].filename == filename ]

def fname_in_use(filename):
    'Return list of names of buffers editing filename, print warning if not empty'
    fbufnames = bufs_for_file(filename)
    if fbufnames:
        print('? buffer %s is already editing file %s' % (fbufnames[0], filename))
    return fbufnames

def current_filename(filename):
    """
    Return filename arg if present, if not return current filename.
    If neither is present, print warning and return None
    SIDE EFFECT! Assign current filename only if it was previously absent.
    """
    if filename:
        if not buf.filename:
            buf.filename = filename # side effect!
        return filename
    if buf.filename:
        return buf.filename
    print('? no current filename')
    return None

def create_buf(bufname):
    'Create buffer with given name. Replace any existing buffer with same name'
    global previous, current, buf
    buf = buffer.Buffer(bufname)
    buffers[bufname] = buf # replace buffers[bufname] if it already exists
    previous = current
    current = bufname
    view.update(Op.create, buffer=buf)

def select_buf(bufname):
    'Make buffer with given name the current buffer'
    global previous, current, buf
    previous = current
    current = bufname
    buf = buffers[current]
    view.update(Op.select, buffer=buf)

# command functions: buffers and files

def b(*args):
    """
    Set current buffer to name.
    If no buffer with given name, create scratch buffer with no file.
    If no name given, set current buffer to previous current buffer.
    """
    global previous, current, buf
    _, _, bufname, _ = parse.arguments(args)
    bufname = match_prefix(bufname, buffers)
    if bufname in buffers:
        select_buf(bufname)
    elif bufname:
        create_buf(bufname)
        # buf.filename = bufname # NOT, make scratch buffer with no file
    else:
        select_buf(previous)
    print('.' + buf.info())

def f(*args):
    """
    Set default filename, if filename not given print current filename.
    If filename is already in use, just print warning.
    """
    _, _, filename, _ = parse.arguments(args)
    if filename:
        if fname_in_use(filename):
            return
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
    """
    Read named file into main buffer, replace main buffer contents.
    File name arg is not optional. It replaces the current file.
    If another buffer is already editing named file, print warning and exit.
    """
    _, _, filename, _ = parse.arguments(args)
    if not current == 'main':
        print('? e and E only work in main buffer')
        return
    if not filename:
        print('? no filename')
        return
    if fname_in_use(filename):
        return
    buf.filename = filename
    buf.d(1, buf.nlines())
    r(0, filename)
    buf.modified = False # insert in r sets modified = True, this is exception

def e(*args):
    """
    Read in named file, replace buffer contents.
    BUT exit with warning if buffer has unsaved changes.
    """
    if buf.modified:
        print('? unsaved changes, use E to reload')
        return
    E(*args)

def B(*args):
    """
    Create new Buffer and load the named file. Buffer name is file basename.
    If needed, make unique buffer name by adding suffix <1>, <2>, ...
    If another buffer is already editing file, just switch to that buffer.
    """
    _, _, filename, _ = parse.arguments(args)
    if not filename:
        print('? file name')
        return
    fbufnames = bufs_for_file(filename)
    if fbufnames:
        bufname = fbufnames[0]
        select_buf(bufname) # Do NOT reload file over buffer contents!
        print('.' + buf.info())
        return
    basename = os.path.basename(filename)
    bufname = basename
    suffix = 1
    # assign unique names: README.md README.md<2> ...
    while bufname in buffers:
        suffix += 1
        bufname = basename + '<%d>' % suffix
    create_buf(bufname)
    buf.filename = filename
    r(0, filename)
    buf.modified = False # insert in r sets modified = True, this is exception

def w(*args):
    """
    Write current buffer contents to given file name,
    but not if file name is already used by another buffer.
    If no file name given, use buffer's current file name.
    If file name given and no current file name, assign given.
    """
    _, _, fname, _ = parse.arguments(args)
    if fname:
        fbufnames = bufs_for_file(fname)
    if fname and fbufnames and current not in fbufnames:
        print('? buffer %s is already editing file %s' % (fbufnames[0], fname))
        return
    filename = current_filename(fname)
    if filename: # if not, current_filename printed error msg
        buf.w(filename)
        view.update(Op.status, buffer=buf)
        print('%s, %d lines' % (filename, buf.nlines()))

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    global previous, current, buf
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
            select_buf(keys[0]) # reassigns current
            previous = current
        view.update(Op.remove, sourcebuf=delbuf, buffer=buf)
        print('%s, buffer deleted' % name)

D_count = 0 # number of consecutive times D command has been invoked

def D(*args):
    'Delete the named buffer, but if unsaved changes print message and exit'
    global D_count
    _, _, bufname, _ = parse.arguments(args)
    name = bufname if bufname else current
    if name in buffers and buffers[name].modified and not D_count:
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

def print_buffers():
    """
    Print information about all buffers on stdout.
    Called by n to print on stdout, called by N with redirection
    """
    print('CRM Buffer            Lines  Mode     File')  # Current Readonly Modified
    for name in buffers:
        print(('.' if name == current else ' ') + buffers[name].info())

def n(*args):
    'print information about all buffers on stdout'
    print_buffers()

def N(*args):
    'Print information about all buffers in *Buffers* buffer'
    b('*Buffers*')
    d(1,S())
    with redirect_stdout(buf):
        print_buffers()

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
    'Print lines from start through end, leave dot at last line printed'
    valid, start, end, _, _ = check.irange(buf, args)
    if valid:
        p_lines(start, end, sys.stdout) # print unconditionally

npage = 22 # n of lines printed by z command, can be changed by optional param

def z(*args):
    """
    Scroll: print npage lines. If parameter is present, update npage.
    If npage is non-negative, start at iline, leave dot at last line printed.
    If iline arg is not given (that's typical), set iline to dot+1 not dot
     like classic ed, so repeated z commands print with no repeated lines
    if npage is negative, scroll back up (not supported in classic ed):
     start at iline+npage (preceding iline), leave dot at first line printed.
    """
    global npage
    valid, iline, npage_string = check.iline_valid(buf, args)
    if valid:
        if npage_string:
            try:
                npage = int(npage_string)
            except:
                print('? integer expected at %s' % npage_string)
                return
        if npage >= 0:
            if not args or isinstance(args[0],str): # args[0] might be npage
                iline = buf.dot + 1
            end = iline + npage - 1
        else:
            end = iline - 1
            iline += npage # npage negative, go backward
            iline = iline if iline > 0 else 1
        end = end if end <= buf.nlines() else buf.nlines()
        p_lines(iline, end, view.lz_print_dest) # assigns buf.dot = iline
        if npage < 0:
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

def j(*args):
    'Delete lines from start to end, replace with single line of joined text'
    valid, start, end, _, _ = check.irange(buf, args)
    # For j command only, default end is start+1
    end = (start + 1 if end == start and check.iline_ok(buf, start+1)
           else end)
    if valid:
        buf.j(start, end)

def J(*args):
    'Replace lines from start to end with wrapped (filled) lines'
    valid, start, end, param, _ = check.irange(buf, args)
    if valid:
        if param:
            try:
                fill_column = int(param)
            except:
                print('? integer expected at %s' % param)
                return
        else:
            fill_column = 0
        buf.J(start, end, fill_column)

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
    'Yank (copy, do not remove) lines to cut buffer'
    valid, start, end, _, _ = check.irange(buf, args)
    if valid:
        buf.y(start, end)

def x(*args):
    'Append (put, paste) cut buffer contents after dest. line address'
    iline, _, _, _ = parse.arguments(args)
    iline = check.mk_iline(buf, iline)
    if not (0 <= iline <= buf.nlines()+1): # allow +y at $ to append to buffer
        print('? invalid address')
        return
    buf.x(iline)

# command functions: markers

def k(*args):
    """
    Mark addressed line in this buffer with character c (command parameter),
    to use with 'c address form.  'c address identifies both buffer and line.
    """
    valid, iline, marker = check.iline_valid(buf, args)
    if valid:
        if marker:
            c = marker[0]
            buf.mark[c] = iline
            print("Mark %s set at line %d in buffer %s" % (c, iline, current))
        else:
            print("No mark")

# command functions: control, debugging, etc.

def K(): return 1/0  # raise exception on demand (crash), for testing

# control

quit = False

def Q(*args):
    'Quit ed, despite unsaved changes'
    global quit
    quit = True

q_count = 0

def q(*args):
    'Quit ed, unless unsaved changes'
    global q_count
    if any([buffers[b].modified for b in buffers]) and not q_count:
        print('? unsaved changes, repeat q to quit')
        q_count += 1 # must invoke q twice to confirm
        return
    Q(*args)

# Variables that must persist between do_command invocations, imported elsewhere
command_prompt = ':' # might be reassigned by startup() from -p option
input_prompt = ''    # input mode, a i c commands - empty prompt
prompt = command_prompt

command_mode = True

def do_command(line):
    'Process one line without blocking in ed command mode or input mode'
    global command_mode, prompt, D_count, q_count
    results = parse.command(buf, line)
    if results:
        cmd_name, args = results
    else:
        return # parse already printed error message
    if cmd_name in parse.complete_cmds:
        globals()[cmd_name](*args) # dict from name (str) to object (fcn)
    elif cmd_name in parse.input_cmds:
        command_mode = False
        prompt = input_prompt
        # Instead of using buf.a i c fcns we handle input mode cmds inline here
        # We add each line to buffer when user types RET at end-of-line,
        # *unlike* in Python API where we pass multiple input lines at once
        start, end, params, _ = parse.arguments(args) # can be int or None
        start, end = check.mk_range(buf, start, end) # int only
        if not (check.iline_ok0(buf, start) if cmd_name in 'ai'
                else check.range_ok(buf, start, end)):
            print('? invalid address')
            command_mode = True
            prompt = command_prompt
        # assign dot to prepare for input mode, where we a(ppend) each line
        elif cmd_name == 'a':
            buf.dot = start
            view.update(Op.input) # depends on buf.dot so can't be moved up
        elif cmd_name == 'i': #and start >0: NOT! can insert in empty file
            buf.dot = start - 1 if start > 0 else 0
            # so we can a(ppend) instead of i(nsert)
            view.update(Op.input) # depends on buf.dot so can't be moved up
        elif cmd_name == 'c': #c(hange) command deletes changed lines first
            buf.d(start, end) # d updates buf.dot, calls update(Op.delete).
            buf.dot = start - 1 # supercede dot assigned in preceding
            view.update(Op.input) # queues Op.input after buf.d Op.delete
        else:
            print('? command not supported in input mode: %s' % cmd_name)
    else:
        print('? command not implemented: %s' % cmd_name)
    # special handling for commands that must be repeated to confirm
    D_count = 0 if cmd_name != 'D' else D_count
    q_count = 0 if cmd_name != 'q' else q_count
    return

def add_line(line):
    'Process one line without blocking in ed input mode'
    global command_mode, prompt
    if line == '.':
        command_mode = True
        prompt = command_prompt
        view.update(Op.command)
    else:
        # Recall input() returns each line with final \n stripped off,
        # BUT buf.a requires \n at end of each line.
        buf.a(buf.dot, line + '\n') # Append new line after dot, advance dot.
    return

def process_line(line):
    'process one line without blocking, according to mode'
    if command_mode:
        do_command(line)
    else:
        add_line(line)

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
previous = 'main'

def startup(*filename, **options):
    global command_prompt, prompt, quit
    if filename:
        e(filename[0])
    if 'p' in options:
        command_prompt = options['p']
        prompt = command_prompt
    quit = False

def main(*filename, **options):
    'Top level ed command to invoke from Python REPL or __main__'
    startup(*filename, **options)
    while not quit:
        line = input(prompt) # blocks!
        process_line(line)

if __name__ == '__main__':
    filename, options = cmd_options()
    main(*filename, **options)
