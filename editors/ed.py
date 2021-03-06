"""
ed.py - line-oriented text editor in pure Python based on classic Unix ed
"""

import re, os, sys
from contextlib import redirect_stdout
import parse, check

# Data structures, variables, fcns in text module: 
# previous current buf buffers create select
import text

# Each ed command is implemented here by a command function with the same
# one-letter name, whose arguments are the same as the ed command args.
# The current buffer is used by many of these functions, but to
# make the API similar to ed commands, it cannot appear as an argument.
# So the current buffer, buf, must be global.  The command functions
# must form an API that can be used without running the ed command line, 
# so each command function must gather and check its own arguments.

# helper functions: line addresses

def o(): # looks like ed .
    'Return index of the current line (called dot), 0 if the buffer is empty'
    return text.buf.dot

def S(): # looks like ed $
    'Return index of the last line, 0 if the buffer is empty'
    return text.buf.nlines()

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

def fname_in_use(filename):
    'Return list of names of buffers editing filename, print warning if not empty'
    fbufnames = text.bufs_for_file(filename)
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
        if not text.buf.filename:
            text.buf.filename = filename # side effect!
        return filename
    if text.buf.filename:
        return text.buf.filename
    print('? no current filename')
    return None

# command functions: buffers and files

def b(*args):
    """
    Set current buffer to name.
    If no buffer with given name, create scratch buffer with no file.
    If no name given, set current buffer to previous current buffer.
    """
    _, _, bufname, _ = parse.arguments(args)
    bufname = match_prefix(bufname, text.buffers)
    if bufname in text.buffers:
        text.select(bufname)
    elif bufname:
        text.create(bufname)
        # text.buf.filename = bufname # NOT, make scratch buffer with no file
    else:
        text.select(text.previous)
    print('.' + text.buf.info())

def f(*args):
    """
    Set default filename, if filename not given print current filename.
    If filename is already in use, just print warning.
    """
    _, _, filename, _ = parse.arguments(args)
    if filename:
        if fname_in_use(filename):
            return
        text.buf.f(filename)
    elif text.buf.filename:
        print(text.buf.filename)
    else:
        print('? no current filename')

def r(*args):
    'Read file contents into buffer after iline'
    valid, iline, fname = check.iline0_valid(text.buf, args)
    if valid:
        filename = current_filename(fname)
        if filename:
            nlines0 = text.buf.nlines()
            text.buf.r(iline, filename)
            print('%s, %d lines' % (filename, text.buf.nlines() - nlines0))

def E(*args):
    """
    Read named file into main buffer, replace main buffer contents.
    File name arg is not optional. It replaces the current file.
    If another buffer is already editing named file, print warning and exit.
    """
    _, _, filename, _ = parse.arguments(args)
    if not text.current == 'main':
        print('? e and E only work in main buffer')
        return
    if not filename:
        print('? no filename')
        return
    fbufnames = text.bufs_for_file(filename)
    if fbufnames and 'main' not in fbufnames:
        print('? buffer %s is already editing file %s' % (fbufnames[0], filename))
        return
    text.buf.filename = filename
    text.buf.d(1, text.buf.nlines())
    r(0, filename)
    text.buf.modified = False # insert in r sets modified = True, this is exception

def e(*args):
    """
    Read in named file, replace buffer contents.
    BUT exit with warning if buffer has unsaved changes.
    """
    if text.buf.modified:
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
    fbufnames = text.bufs_for_file(filename)
    if fbufnames:
        bufname = fbufnames[0]
        text.select(bufname) # Do NOT reload file over buffer contents!
        print('.' + text.buf.info())
        return
    basename = os.path.basename(filename)
    bufname = basename
    suffix = 1
    # assign unique names: README.md README.md<2> ...
    while bufname in text.buffers:
        suffix += 1
        bufname = basename + '<%d>' % suffix
    text.create(bufname)
    text.buf.filename = filename
    r(0, filename)
    text.buf.modified = False # insert in r sets modified = True, this is exception

def w(*args):
    """
    Write current buffer contents to given file name,
    but not if file name is already used by another buffer.
    If no file name given, use buffer's current file name.
    If file name given and no current file name, assign given.
    """
    _, _, fname, _ = parse.arguments(args)
    if fname:
        fbufnames = text.bufs_for_file(fname)
    if fname and fbufnames and text.current not in fbufnames:
        print('? buffer %s is already editing file %s' % (fbufnames[0], fname))
        return
    filename = current_filename(fname)
    if filename: # if not, current_filename printed error msg
        text.buf.w(filename)
        print('%s, %d lines' % (filename, text.buf.nlines()))

def DD(*args):
    'Delete the named buffer, even if it has unsaved changes'
    _, _, bufname, _ = parse.arguments(args)
    name = bufname if bufname else text.current
    if not name in text.buffers:
        print('? buffer name')
    elif name == 'main':
        print("? Can't delete main buffer")
    else:
        text.delete(name)
        print('%s, buffer deleted' % name)

D_count = 0 # number of consecutive times D command has been invoked

def D(*args):
    'Delete the named buffer, but if unsaved changes print message and exit'
    global D_count
    _, _, bufname, _ = parse.arguments(args)
    name = bufname if bufname else text.current
    if text.modified(name) and not D_count:
        print('? unsaved changes, repeat D to delete')
        D_count += 1 # must invoke D twice to confirm, see message below
        return
    DD(*args)

# command functions: displaying information

def A(*args):
    ' = in command mode, print the line number of the addressed line'
    iline, _, _, _ = parse.arguments(args)
    iline = iline if iline != None else text.buf.nlines() # default $ not .
    if check.iline_ok0(text.buf, iline): # don't print error message when file is empty
        print(iline)
    else:
        print('? no match' if iline == text.buffer.no_match else '? invalid address')        

def n(*args):
    'Print information about all buffers on stdout.'
    print('CRM Buffer            Lines  Mode     File')  # Current Readonly Modified
    for name in text.buffers:
        print(('.' if name == text.current else ' ') + text.info(name))

def N(*args):
    'Print information about all buffers in *Buffers* buffer.'
    b('*Buffers*')
    d(1,S())
    with redirect_stdout(text.buf):
        n(*args)

# command functions: displaying and navigating text

# called by l (below), might be called by display code elsewhere
def l_noprint(*args):
    'Advance dot to iline, return that line'
    iline, _, _, _ = parse.arguments(args)
    if not text.buf.lines:
        print('? empty buffer')
        return
    # don't use usual default dot here, instead advance dot
    if iline == None:
        iline = text.buf.dot + 1
    if not check.iline_ok(text.buf, iline):
        print('? no match' if iline == text.buffer.no_match else '? invalid address')
        return
    line, _ = text.buf.l(iline)
    return line

def l(*args):
    'Advance dot to iline, print it'
    line = l_noprint(*args)
    print(line)

def p(*args):
    'Unconditionally print lines from start through end, inclusive'
    valid, start, end, _, _ = check.irange(text.buf, args)
    if valid:
        for iline in range(start, end+1): # +1 because start,end is inclusive
            line, _ = text.buf.l(iline)
            print(line)

# Alternative to p_lines (below), might be called by display code elsewhere
def p_lines_noprint(start, end):
    'Advance dot to end, but do not print lines'
    _, _ = text.buf.l(end)
    
def p_lines(start, end):
    'Print lines start through end, inclusive'
    for iline in range(start, end+1): # +1 because start,end is inclusive
        line, _ = text.buf.l(iline)
        print(line)

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
    valid, iline, npage_string = check.iline_valid(text.buf, args)
    if valid:
      valid, npage = check.iparam(npage_string, npage)
      if valid:
        if npage >= 0:
            if not args or isinstance(args[0],str): # args[0] might be npage
                iline = text.buf.dot + 1
            end = iline + npage - 1
        else:
            end = iline - 1
            iline += npage # npage negative, go backward
            iline = iline if iline > 0 else 1
        end = end if end <= text.buf.nlines() else text.buf.nlines()
        p_lines(iline, end)
        if npage < 0:
            text.buf.dot = iline

# command functions: adding, changing, and deleting text

def a(*args):
    'Append lines from string after  iline, update dot to last appended line'
    valid, iline, lines = check.iline0_valid(text.buf, args)
    if valid and lines:
        text.buf.a(iline, lines)

def i(*args):
    'Insert lines from string before iline, update dot to last inserted line'
    valid, iline, lines = check.iline0_valid(text.buf, args)
    if valid and lines:
        text.buf.i(iline, lines)

def d(*args):
    'Delete text from start up to end, set dot to first line after deletes'
    valid, start, end, _, _ = check.irange(text.buf, args)
    if valid:
        text.buf.d(start, end)

def j(*args):
    'Delete lines from start to end, replace with single line of joined text'
    valid, start, end, _, _ = check.irange(text.buf, args)
    # For j command only, default end is start+1
    end = (start + 1 if end == start and check.iline_ok(text.buf, start+1)
           else end)
    if valid:
        text.buf.j(start, end)

def J(*args):
    'Replace lines from start to end with wrapped (filled) lines'
    valid, start, end, param, _ = check.irange(text.buf, args)
    if valid:
        valid, fill_column = check.iparam(param, 0)
        if valid:
            text.buf.J(start, end, fill_column)

# used for both indent and outdent
indent = 4

def I(*args):
    'Indent lines, optional parameter assigns n of indent/outdent spaces'
    global indent
    valid, start, end, param, _ = check.irange(text.buf, args)
    if valid:
        valid, indent = check.iparam(param, indent)
        if valid:
            text.buf.I(start, end, indent)
    
def O(*args):
    'Outdent lines, optional parameter assigns n of indent/outdent spaces'
    global indent
    valid, start, end, param, _ = check.irange(text.buf, args)
    if valid:
        valid, indent = check.iparam(param, indent)
        if valid:
            text.buf.M(start, end, indent)

def c(*args):
    'Change (replace) lines from start up to end with lines from string'
    valid, start, end, lines, _ = check.irange(text.buf, args)
    if valid:
        text.buf.c(start,end,lines)

def s(*args):
    """
    Substitute new for old in lines from start up to end.
    When glbl is False (the default), substitute only the first occurrence
    in each line.  Otherwise substitute all occurrences in each line.
    If old is absent, use pattern from most recent search if successsful.
    """
    valid, start, end, old, params = check.irange(text.buf, args)
    if valid:
        if not old and text.buf.found:
            old = text.buffer.Buffer.pattern # most recent successful search
        # params might be [ new, glbl, use_regex ]
        if old and len(params) > 0 and isinstance(params[0],str):
            new = params[0]
        else:
            print('? /old/new/')
            return
        glbl = bool(params[1])
        use_regex = bool(params[2])
        match = text.buf.s(start, end, old, new, glbl, use_regex)
        if not match:
            print('? no match')

def u(*args):
    'Undo last substitution: replace line at iline from cut buffer'
    valid, iline, _ = check.iline0_valid(text.buf, args)
    if valid:
        text.buf.u(iline)

def m(*args):
    'move lines to after destination line'
    valid, start, end, dest = check.range_dest(text.buf, args)
    if valid:
        if (start <= dest <= end):
            print('? invalid destination')
            return
        text.buf.m(start, end, dest)

def t(*args):
    'transfer (copy) lines to after destination line'
    valid, start, end, dest = check.range_dest(text.buf, args)
    if valid:
        text.buf.t(start, end, dest)

def y(*args):
    'Yank (copy, do not remove) lines to cut buffer'
    valid, start, end, _, _ = check.irange(text.buf, args)
    if valid:
        text.buf.y(start, end)

def x(*args):
    'Append (put, paste) cut buffer contents after dest. line address'
    iline, _, _, _ = parse.arguments(args)
    iline = check.mk_iline(text.buf, iline)
    if not (0 <= iline <= text.buf.nlines()+1): # allow +y at $ to append to buffer
        print('? no match' if iline == text.buffer.no_match else '? invalid address')
        return
    text.buf.x(iline)

# command functions: markers

def k(*args):
    """
    Mark addressed line in this buffer with character c (command parameter),
    to use with 'c address form.  'c address identifies both buffer and line.
    """
    valid, iline, marker = check.iline_valid(text.buf, args)
    if valid:
        if marker:
            c = marker[0]
            text.buf.mark[c] = iline
            print("Mark %s set at line %d in buffer %s" % (c, iline, text.current))
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
    if text.any_modified() and not q_count:
        print('? unsaved changes, repeat q to quit')
        q_count += 1 # must invoke q twice to confirm
        return
    Q(*args)

# Variables that must persist between do_command invocations, imported elsewhere
command_prompt = ':' # might be reassigned by startup() from -p option
input_prompt = ''    # input mode, a i c commands - empty prompt
prompt = command_prompt

command_mode = True

# Called by do_command (below), might be wrapped with display code elsewhere
def prepare_input_mode(cmd_name, start, end):
    'assign dot to prepare for input mode, where we a(ppend) each line'
    if cmd_name == 'a':
        text.buf.dot = start
    elif cmd_name == 'i': #and start >0: NOT! can insert in empty file
        text.buf.dot = start - 1 if start > 0 else 0
        # so we can a(ppend) instead of i(nsert)
    elif cmd_name == 'c': #c(hange) command deletes changed lines first
        text.buf.d(start, end) # d updates text.buf.dot, calls frame.delete()
        text.buf.dot = start - 1 # supercede dot assigned in preceding
    else:
        pass

def do_command(line):
    'Process one line without blocking in ed command mode or input mode'
    global command_mode, prompt, D_count, q_count
    results = parse.command(text.buf, line)
    if results:
        cmd_name, args = results
    else:
        return # parse already printed error message
    if cmd_name in parse.complete_cmds:
        globals()[cmd_name](*args) # dict from name (str) to object (fcn)
    elif cmd_name in parse.input_cmds:
        command_mode = False
        prompt = input_prompt
        # Instead of using text.buf.a i c fcns we handle input mode cmds inline here
        # We add each line to buffer when user types RET at end-of-line,
        # *unlike* in Python API where we pass multiple input lines at once
        start, end, params, _ = parse.arguments(args) # can be int or None
        start, end = check.mk_range(text.buf, start, end) # int only
        if not (check.iline_ok0(text.buf, start) if cmd_name in 'ai'
                else check.range_ok(text.buf, start, end)):
            print('? no match' if iline == text.buffer.no_match else '? invalid address')            
            command_mode = True
            prompt = command_prompt
        elif cmd_name in 'aic':
            prepare_input_mode(cmd_name, start, end)
        else:
            print('? command not supported in input mode: %s' % cmd_name)
    else:
        print('? command not implemented: %s' % cmd_name)
    # special handling for commands that must be repeated to confirm
    D_count = 0 if cmd_name != 'D' else D_count
    q_count = 0 if cmd_name != 'q' else q_count
    return

# Called by add_line (below), might be wrapped with display code elsewhere
def set_command_mode():
    'set mode and prompt for command mode'
    global command_mode, prompt
    command_mode = True
    prompt = command_prompt
    
def add_line(line):
    'Process one line without blocking in ed input mode'
    if line == '.':
        set_command_mode()
    else:
        # Recall input() returns each line with final \n stripped off,
        # BUT text.buf.a requires \n at end of each line.
        text.buf.a(text.buf.dot, line + '\n') # Append new line after dot, advance dot.
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

def startup(*filename, **options):
    global command_prompt, prompt, quit
    text.startup('main')
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
