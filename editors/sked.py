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

# Define and initialize global variables used by sked editing functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = dot # if dot is already defined, then skedinit was already exec'd
except:
    exec(open("skedinit.py").read())

# utility functions

def o():
    'Return dot, index of current line.  o looks a bit like classic ed .'
    return dot

def S():
    'Return index of last line in buffer.  S looks a bit like classic ed $'
    return len(buffer)-1  # -1 because of zero based index

def line_valid(iline):
    """
    If iline is within range return True,
    otherwise print error message and return False.
    """
    if 0 < iline <= S():
        return True
    else:
        print(f'? line {iline} out of range 1 .. {S()}')
        return False

def range_valid(start, end):
    """
    If start .. end is within range return True,
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

def st():
    'st(atus), print line of information about editing session'
    print(status())

# File and buffer functions

def save_buffer():
    'Save state of current buffer including text, dot etc.'
    global buffers
    # index         0         1       2   3    4
    bstate = bufname, filename, buffer, dot, yank, saved 
    buffers[bufname] = bstate

def restore_buffer(bname):
    'Restore state of buffer bname to current buffer'
    global bufname, filename, buffer, dot, yank, saved
    bufname, filename, buffer, dot, yank, saved = buffers[bname]

def bname(filename):
    'Generate buffer name from filename'
    basename = os.path.basename(filename)
    # Make unique bufname for example for both README.md and editors/README.md 
    bufname = basename
    suffix = 1
    while bufname in buffers and filename != buffers[bufname][1]:
        suffix += 1
        bufname = basename + f'<{suffix}>'
    return bufname

def e(fname): 
    """
    Load named file into buffer, replacing previous contents.
    But first save buffer state so it can be restored on command.
    """
    global filename, buffer, dot, saved, bufname, prev_bufname
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
    dot = S() # index of last line 
    saved = True
    print(f'{filename}, {dot} lines')

def w(fname=None):
    """
    Write buffer to file, default fname is in filename.
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
        saved = True
        print(f'{filename}, {S()} lines')

def b(bname=None):
    """
    Save current buffer and restore named buffer.
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
        st()
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
                   'saved' if buf[5] else 'unsaved changes'))
    else:
        status = f'{bname} not in stored buffers'
    return status

def n():
    'Print information about stored buffers'
    for bname in buffers: print(bstatus(bname))

def k():
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

def p(start=None, end=None):
    """
    Print lines start through end, *inclusive*.
    Default with no arguments prints the line at dot.
    With no end argument, just print the one line at start.
    """
    global dot
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    for iline in range(start, end+1):
        print(buffer[iline], end='') # line already ends with \n
    dot = end

def l():
    'advance one line and print'
    p(dot+1)

def rl():
    'go back one line and print'
    p(dot-1)

def v(nlines=None):
    """
    Page down, print next nlines lines starting with  dot.
    Default nlines is pagesize, if nlines present assign to pagesize.
    Stop at end of buffer if we reach it.  Set dot to last line printed.
    """
    global pagesize
    if nlines is None: nlines = pagesize
    pagesize = nlines
    start, end = dot, min(dot+pagesize-1, S())
    p(start, end)

def rv(nlines=None):
    """
    Page up, print previous nlines lines ending with  dot.
    """
    global pagesize, dot
    if nlines is None: nlines = pagesize
    pagesize = nlines
    start, end = max(dot-pagesize, 1), dot
    p(start, end)
    dot = start # p puts dot at end

def s(target=None, forward=True):
    """
    Search to end of buffer for next line containing target string.
    Default searches forward, set forward=False to search backward.
    If target found, print line and assign to dot.
    If target not found, leave dot unchanged and print '? <target> not found'
    Assign target to searchstring for use in future searches.
    If target is omitted, use stored searchstring.  
    """
    global dot, searchstring
    found = False
    if not target: target = searchstring
    searchstring = target
    for iline in range(dot+1,S()+1) if forward else range(dot-1,0,-1):
        if target in buffer[iline]:
            found = True
            print(buffer[iline], end='') # line already ends with \n
            dot = iline
            break
    if not found:
        print(f"? '{searchstring}' not found")

def r(target=None):
    'Search backward to start of buffer for next line containing target string'
    s(target, forward=False)

def tail(nlines=None):
    """
    tail: print the last nlines lines of the buffer, leave dot at the end.
    Default nlines is pagesize, if nlines present assign to pagesize.
    """
    global pagesize
    if not nlines: nlines = pagesize
    pagesize = nlines
    p(S()-pagesize,S())

# Editing functions

def a(iline=None):
    'a(ppend) lines after iline (default dot), type just . on a line to exit'
    global buffer, dot, saved
    if iline is None: iline = dot
    if not line_valid(iline):
        return
    dot = iline
    while True:
        success = False
        line = input()  # Can this fail?  Yes, by ^C for example
        success = True
        if success:
            if line == '.':
                return
            buffer[dot+1:dot+1] = [line + '\n'] # sic, append line after dot
            dot += 1
            saved = False

def d(start=None, end=None):
    """
    d(elete) lines start through end *inclusive*.
    Save deleted lines in yank (paste) buffer.
    Set dot to last line *preceding* deletion, 
    so we can then use y(ank) to replace the deletion.
    """
    global buffer, yank, dot, saved
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    yank = buffer[start:end+1] # range includes end, unlike Python slices
    buffer[start:end+1] = [] 
    dot = start-1
    saved = False

def y(iline=None):
    'Append yank buffer contents after iline (defalt dot)'
    global buffer, dot, saved
    if not iline: iline = dot
    if not line_valid(iline):
        return
    buffer[iline+1:iline+1] = yank # append yank buffer contents after iline
    dot = iline + len(yank)
    saved = False

def c(old=None, new=None, start=None, end=None, count=-1):
    """
    Replace old string with new string on each line in range.
    Replace in lines start through end, default just replaces in current line.
    If old is None or '', use stored searchstring
     otherwise assign old to searchstring
     Can use '' as placeholder for default old
    If new is None, use stored replacestring.
     Can use '' in new to delete old, but can't use '' as placeholder.
    If new is not None, assign new to replacestring.
    Default count=-1 replaces all occurences on each line.
    Assign count to n to replace first n occurrences on each line.
    """
    global searchstring, replacestring, dot
    if not start: start = dot
    if not end: end = start
    if not range_valid(start, end):
        return
    if not old: old = searchstring
    searchstring = old
    if new is None: new = replacestring
    if new is not None: replacestring = new
    for iline in range(start, end+1): # range is not inclusive so +1
        buffer[iline] = buffer[iline].replace(old, new, count)
    dot = end

def cp(old=None, new=None, start=None, end=None, count=-1):
    'change line and print.  Call c above, then p'
    c(old, new, start, end, count)
    p()
