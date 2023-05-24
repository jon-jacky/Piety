"""
sked.py - Stone Knife Editor, line editor inspired by classic Unix ed.

No main program!  Editor commands are just functions defined here, to
call from the Python REPL.

Global variables used by these functions are defined and initialized
in skedinit.py, which must be executed before calling any of the
functions here.

The name sked is inspired by Kragen Sitaker's Stone Knife Forth.
"""

import os # for os.path.basename, used in store_buffer
import textwrap

# Define and initialize global variables used by sked editing functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables,
# so we retain buffer contents and other state when we reload.
try:
    _ = dot # if dot is already defined, then skedinit was already exec'd
except:
    exec(open("skedinit.py").read())

# Utility functions

def o():
    'Return dot, index of current line.  o looks a bit like classic ed .'
    return dot

def S():
    'Return index of last line in buffer.  S looks a bit like classic ed $'
    return len(buffer)-1  # -1 because of zero based index

def line_valid(iline):
    """
    If iline is within buffer return True,
    otherwise print error message and return False.
    """
    if 0 < iline <= S():
        return True
    else:
        print(f'? line {iline} out of range 1 .. {S()}')
        return False

def range_valid(start, end):
    """
    If start .. end is within buffer return True,
    otherwise print error message(s) and return false.
    """
    if line_valid(start) and ((start == end) or line_valid(end)): 
        return True
    else: 
        return False

def status():
    'status: return string of information about editing session'
    return (f'{bufname}, at line {dot} of {S()}, file {filename}, ' 
            f"{'saved' if saved else 'unsaved changes'}")

# Display code hooks

# These functions are passed as arguments to other functions here.
# They do not produce display output, but can be replaced by 
# functions from other modules that do produce display output.  

def move_dot(iline):
    'Assign iline to dot. Replacement function can then move display cursor'
    global dot
    dot = iline

def change_lines(start, end):
    'In sked, just assign end to dot.  Replacement function does much more.'
    move_dot(end)

def set_saved(status): 
    'Assign status to saved.  Replacement function can update status line'
    global saved
    saved = status

def restore_buffer(bname):
    'Restore state of saved buffer bname to current saved buffer'
    global bufname, filename, buffer, dot, saved
    bufname, filename, buffer, dot, saved = buffers[bname]
    print(status()) # print the new buffer name

def input_line():
    'Call builtin input and return the line it gets'
    return input()

# File and buffer functions

def save_buffer():
    'Save state of current buffer including text, dot etc.'
    global buffers
    # index         0         1       2   3    4
    bstate = bufname, filename, buffer, dot, saved 
    buffers[bufname] = bstate

def bname(filename):
    'Generate buffer name from file name, ensure each file gets unique bname'
    basename = os.path.basename(filename)
    # Make unique bufname for example for both README.md and editors/README.md 
    bufname = basename
    suffix = 1
    while bufname in buffers and filename != buffers[bufname][1]:
        suffix += 1
        bufname = basename + f'<{suffix}>'
    return bufname

def e(fname, move_dot=move_dot):  # move_dot is a hook for display code 
    """
    e(dit), load named file into buffer, replacing previous contents.
    But first save buffer state so it can be restored on command.
    """
    global filename, buffer, saved, bufname, prev_bufname
    if S() > 0: save_buffer()
    try:
        with open(fname, mode='r') as fd:
            # fd.readlines reads file into a list of strings, one per line
            # First line of file is at index 1 not 0
            buffer = ['\n'] + fd.readlines() # each line in buffer ends with \n
    except FileNotFoundError:
        buffer = ['\n'] # start new file
    prev_bufname = bufname
    filename = fname
    bufname = bname(filename)
    saved = True # put this *before* move_dot for display code
    move_dot(min(S(),1)) # start of buffer, empty buffer S() is 0
    print(f'{filename}, {S()} lines')

def w(fname=None, set_saved=set_saved): # Hook for display code
    """
    w(rite) buffer to file, default fname is in filename.
    If fname is given, assign it to filename to be used for future writes.
    """
    global filename, bufname, saved
    if not fname: fname = filename
    success = False # Might fail if path doesn't exist, no permission etc.
    with open(fname, 'w') as fd:
        fd.writelines(buffer[1:]) # first line of file is at index 1 not 0
        success = True
    if success:
        filename = fname
        bufname = bname(filename)
        set_saved(True)
        print(f'{filename}, {S()} lines')

def b(bname=None, restore_buffer=restore_buffer): 
    """
    b(uffer), save current buffer and restore named buffer.
    If buffer name not given, switch back to previous buffer
    """
    global prev_bufname
    if S() > 0: save_buffer()
    if not bname: bname = prev_bufname
    if bname == bufname:
        print(f'? buffer {bufname} is already the current buffer')
        return
    if bname in buffers:
        prev_bufname = bufname
        restore_buffer(bname)
    else:
        print(f'? no buffer {bname}')

def bstatus(bname):
    'Return string of information about named stored buffer'
    if bname in buffers:
        buf = buffers[bname]
        # Use old fashinoned % formatting to get left-justified columns
        status = ('%s%-15s %7d   %-30s  %s' % 
                  ('*' if bufname == buf[0] else ' ', 
                   buf[0], len(buf[2])-1, buf[1], 
                   'saved' if buf[4] else 'unsaved changes'))
    else:
        status = f'{bname} not in stored buffers'
    return status

def n():
    'n(ames), print names and other information about stored buffers'
    for bname in buffers: print(bstatus(bname))

def k(restore_buffer=restore_buffer):
    """
    k(ill) the current buffer and delete it from stored buffers.
    Replace the current buffer with the previous buffer.
    """
    if bufname == 'scratch.txt':
        print("? can't kill scratch.txt buffer")
        return
    if not saved:
        answer = input(f'{bufname} has unsaved changes, type y to kill anyway: ')
        if not answer[0] in 'yY':
            return
    if bufname in buffers: # current buffer might not be saved yet
        del buffers[bufname]
    # prev buffer may have been killed, but there is always a saved scratch.txt
    restore_buffer(prev_bufname if prev_bufname in buffers else 'scratch.txt')

# File viewer functions

def p(start=None, end=None, printline=print, move_dot=move_dot): # hooks 
    """
    p(rint) lines start through end, *inclusive*.
    Default with no arguments prints the line at dot.
    With no end argument, just print the one line at start.
    """
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    for iline in range(start, end+1):
        printline(buffer[iline], end='') # line already ends with \n
    move_dot(end)

def l(p=p):  # p is hook for display code
    'l(ine), advance one line and print'
    p(dot+1)

def rl(p=p):  # p is hook for display code
    'r(everse) l(ine), go back one line and print'
    p(dot-1)

def v(nlines=None, p=p):  # p is hook for display code
    """
    v, page down, print next nlines lines starting with dot.
    Default nlines is pagesize, if nlines present assign to pagesize.
    Stop at end of buffer if we reach it.  Set dot to last line printed.
    """
    global pagesize
    if dot == S():
        print('? end of buffer')
        return
    if nlines is None: nlines = pagesize
    pagesize = nlines
    p(dot, min(dot+pagesize-1, S()))

def rv(nlines=None, p=p, move_dot=move_dot):  # hooks for display code
    'r(everse) v, page up, print previous nlines lines ending with dot.'
    global pagesize
    if dot == 1:
        print('? start of buffer')
        return
    if nlines is None: nlines = pagesize
    pagesize = nlines
    start = max(dot-pagesize, 1)
    p(start, dot)
    move_dot(start) # p puts dot at end

def s(target=None, forward=True, printline=print, move_dot=move_dot):  # hooks 
    """
    s(earch) forward  for next line containing target string.
    Default searches forward, set forward=False to search backward.
    If target found, print line and assign to dot.
    If target not found, leave dot unchanged and print '? <target> not found'
    Assign target to searchstring for use in future searches.
    If target is omitted, use stored searchstring.  
    """
    global searchstring
    found = False
    if not target: target = searchstring
    searchstring = target
    for iline in range(dot+1,S()+1) if forward else range(dot-1,0,-1):
        if target in buffer[iline]:
            found = True
            printline(buffer[iline], end='') # line already ends with \n
            move_dot(iline)
            break
    if not found:
        print(f"? '{searchstring}' not found")

def grep(target=None, start=None, end=None):
    """
    Print each line in range start, end that contains target string.
    Default range is entire buffer.  Current line, dot, is *not* changed.
    """
    global searchstring
    found = False
    if not target: target = searchstring
    searchstring = target
    if not start: start = 1
    if not end: end = S()
    for iline in range(start, end+1):
        if target in buffer[iline]:
            found = True
            print('%3d %s' % (iline, buffer[iline]), end='') 
    if not found:
        print(f"? '{searchstring}' not found")

def r(target=None):
    'r(everse) search backward for next line containing target string'
    s(target, forward=False)

def tail(nlines=None, p=p):  # p is hook for display code
    """
    tail: print the last nlines lines of the buffer, leave dot at the end.
    Default nlines is pagesize, if nlines present assign to pagesize.
    """
    global pagesize
    if not nlines: nlines = pagesize
    pagesize = nlines
    p(max(S()-pagesize, 1), S())

# Basic editing functions

def a(iline=None, move_dot=move_dot, input_line=input_line,
      move_dot_a=move_dot):
    """
    a(ppend) lines after iline (default dot).
    This function is the only way to add text to the buffer in sked.
    Type a() RET, then type lines of text, type just . on a line to exit.
    Just type a() to begin adding text to an empty buffer.
    After that, must type a(0) to insert text at the beginning of a buffer.
    move_dot, input_line, and move_dot_a are placeholders for display fcns.
    """
    global buffer, saved
    if iline is None: iline = dot
    # Can't use line_valid - must allow append after line 0 to append at line 1.
    if not (0 <= iline <= S()):
        print(f'? line {iline} out of range 1 .. {S()}')
        return
    move_dot(iline)
    while True:
        success = False
        line = input_line()  # Can this fail?  Yes, by ^C for example
        success = True
        if success:
            if line == '.':
                return
            buffer[dot+1:dot+1] = [line + '\n'] # sic, append line after dot
            saved = False # put this before move_dot for display
            move_dot_a(dot+1)

def d(start=None, end=None, move_dot=move_dot): # hook for display code
    """
    d(elete) lines start through end *inclusive*.
    Save deleted lines in yank (paste) buffer.
    Set dot to last line *preceding* deletion, 
    so we can then use y(ank) to replace the deletion.
    """
    global buffer, yank, saved
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    yank = buffer[start:end+1] # range includes end, unlike Python slices
    buffer[start:end+1] = [] 
    saved = False # put this before move_dot for display
    move_dot(start-1)

def y(iline=None, move_dot=move_dot): # hook for display code
    'y(ank), that is paste, yank buffer contents after iline (default dot)'
    global buffer, saved
    if not iline: iline = dot
    if not line_valid(iline):
        return
    buffer[iline+1:iline+1] = yank # append yank buffer contents after iline
    saved = False # put this before move_dot for display
    move_dot(iline + len(yank))

def c(old=None, new=None, start=None, end=None, count=-1, move_dot=move_dot):
    """
    c(hange), replace old string with new string on each line in range.
    Replace in lines start through end, default replaces in current line.
    If old is None or '', use stored searchstring
     otherwise assign old to searchstring
     Can use '' as placeholder for default old
    If new is None, use stored replacestring.
     Can use '' in new to delete old, but can't use '' as placeholder.
    If new is not None, assign new to replacestring.
    Default count=-1 replaces all occurences on each line.
    Assign count to n to replace first n occurrences on each line.
    """
    global searchstring, replacestring, saved
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    if not old: old = searchstring
    searchstring = old
    if new is None: new = replacestring
    if new is not None: replacestring = new
    for iline in range(start, end+1): # range is not inclusive so +1
        if old in buffer[iline]:
            buffer[iline] = buffer[iline].replace(old, new, count)
            saved = False # put this *before* move_dot for display code
            move_dot(iline) # puts cursor on the command line for print below
            print(buffer[iline], end='') # print even when display enabled

# Formatting functions

def indent(start=None, end=None, nspaces=None, outdent=False,
           change_lines=change_lines): # hook for display code
    """
    indent, move text to the right by prefixing spaces at the left margin.
    Indent lines start through end inclusive, default just indent at dot.
    Indent by nspaces spaces, default lmargin, assign given nspaces to lmargin.
    If outdent, move text to left by removing characters from left margin.
    """
    global lmargin
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    if not nspaces: nspaces = lmargin
    lmargin = nspaces # int
    margin = ' '*nspaces # str
    for iline in range(start, end+1): # start, end inclusive
        if outdent:
            buffer[iline] = buffer[iline][nspaces:]
        else: # indent
            buffer[iline] = margin + buffer[iline]
    change_lines(start, end) # move dot to end

def outdent(start=None, end=None, nspaces=None, change_lines=change_lines):
    'outdent: move text left by removing characters at left margin.'
    indent(start, end, nspaces, True, change_lines)

def wrap(start=None, end=None, lmarg=None, rmarg=None,
         move_dot=move_dot): # hook for display code
    """
    Replace lines from start through end with wrapped (filled) lines.
    start and end both default to dot, good for wrapping one long line.
    left and right margins default to lmargin, rmargin.
    if lmarg (or rmarg) is given, lmargin (or rmargin) is set to that value.
    """
    global lmargin, rmargin, yank
    if not start: start = dot
    if not end: end = dot
    if not range_valid(start, end):
        return
    if not lmarg: lmarg = lmargin
    lmargin = lmarg
    if not rmarg: rmarg = rmargin
    rmargin = rmarg
    lines = buffer[start:end+1]
    slines = ''.join(lines) # textwrap requires single string not list
    margin = lmargin*' '
    wlines = textwrap.wrap(slines, width=rmargin, initial_indent=margin,
                           subsequent_indent=margin) # returns list of lines
    wrapped = [ line + '\n' for line in wlines ]
    buffer[start:end+1] = []  # delete unwrapped lines
    buffer[start:start] = wrapped # sic, insert lines at this position
    yank = wrapped # FIXME hack so we can use edsel display_y for move_dot
    move_dot(start + len(wrapped) - 1) # move dot to end of wrapped text

def j(start=None, end=None, move_dot=move_dot):
    """
    j(oin) successive lines into one line. Replace line breaks with spaces.
    start defaults to dot, end defaults to dot+1 to join next line to dot.
    """
    if not start: start = dot
    if not end: end = dot+1
    if not range_valid(start, end):
        return
    lines = [ line.rstrip('\n') for line in buffer[start:end+1] ]
    joined = ' '.join(lines)+'\n' # put spaces between joined lines
    buffer[start:end+1] = [] # delete unjoined lines
    buffer[start:start] = [ joined ] # insert [ joined ] lines at start
    move_dot(start) # move dot to joined line
