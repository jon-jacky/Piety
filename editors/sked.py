"""
sked.py - Stone Knife Editor, minimal line editor inspired by classic Unix ed,
           but even simpler.

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
    _ = o
except:
    exec(open("skedinit.py").read())

# utility functions

def S():
    'Return index of last line in buffer.  S looks a bit like classic ed $'
    return len(buffer)-1  # -1 because of zero based index

def status():
    'status: return string of information about editing session'
    return ('%s, at line %d of %d, file %s, %s' %
            (bufname, o, S(), filename, 
             'saved' if saved else 'unsaved changes'))

def st():
    'st(atus), print line of information about editing session'
    print(status())

# File and buffer functions

def save_buffer():
    'Save state of current buffer including text, dot etc.'
    global buffers
    # index        0  1         2        3             4         5      6
    bstate = (buffer, o, filename, bufname, searchstring, pagesize, saved,
              #  7
              yank)
    buffers[bufname] = bstate

def restore_buffer(bname):
    'Restore state of buffer bname to current buffer'
    global buffer, o, filename, bufname, searchstring, pagesize, saved, yank
    buffer, o, filename, bufname, searchstring, pagesize, saved, yank \
        = buffers[bname]

def bname(filename):
    'Generate buffer name from filename'
    basename = os.path.basename(filename)
    # Make unique bufname for example for both README.md and editors/README.md 
    bufname = basename
    suffix = 1
    while bufname in buffers and filename != buffers[bufname][2]:
        suffix += 1
        bufname = basename + '<%d>' % suffix
    return bufname

def e(fname): 
    """
    Load named file into buffer, replacing previous contents.
    But first save buffer state so it can be restored on command.
    """
    global filename, buffer, o, saved, bufname
    if S() > 0: save_buffer()
    try:
        with open(fname, mode='r') as fd:
            # fd.readlines reads file into a list of strings, one per line
            # First line of file is at index 1 not 0
            buffer = ['\n'] + fd.readlines() # each line in buffer ends with \n
    except FileNotFoundError:
        buffer = ['\n'] # start new file
    filename = fname
    bufname = bname(filename)
    o = S() # index of last line 
    saved = True
    print('%s, %d lines' % (filename, o))

def w(fname=None):
    """
    Write buffer to file, default fname is in filename.
    If fname is given, assign it to filename to be used for future writes.
    """
    global filename, bufname
    fname = fname if fname else filename
    success = False # Might fail if path doesn't exist, no permission etc.
    with open(fname, 'w') as fd:
        fd.writelines(buffer[1:]) # first line of file is at index 1 not 0
        success = True
    if success:
        filename = fname
        bufname = bname(filename)
        saved = True
        print('%s, %d lines' % (filename, S()))

def b(bname=None):
    """
    Save current buffer and restore named buffer.
    If buffer name not given, switch back to previous buffer
    """
    global prev_bufname
    if S() > 0: save_buffer()
    if not bname: bname = prev_bufname
    if bname == bufname:
        print('? buffer %s is already the current buffer' % bufname)
        return
    if bname in buffers:
        prev_bufname = bufname
        restore_buffer(bname)
        st()
    else:
        print('? no buffer %s' % bname)

def bstatus(bname):
    'Return string of information about named stored buffer'
    if bname in buffers:
        buf = buffers[bname]
        status = ('%s%-15s %7d   %-30s  %s' % 
                  ('*' if bufname == buf[3] else ' ', 
                   buf[3], len(buf[0])-1, buf[2], 
                   'saved' if buf[6] else 'unsaved changes'))
    else:
        status = '%s not in stored buffers' % bname
    return status

def n():
    'Print information about stored buffers'
    for bname in buffers: print(bstatus(bname))

# File viewer functions
            
def printline(iline):
    """
    Check iline within buffer, then print line or error message.
    Assign dot and return True if line printed, False if iline not in buffer.
    """
    global o
    if iline > 0 and iline <= S():
        print(buffer[iline], end='') # line already ends with \n
        o = iline
        return True
    else:
        print('? end of buffer')
        return False

def p(start=None, end=None):
    """
    Print lines start through end, *inclusive*.
    Default with no arguments prints the line at dot.
    With no end argument, just print the one line at start.
    Set dot to the last line printed.
    If start is 0 -- or anything less than 1 -- set start to 1.
    If end is past end of buffer, print through end then print '? eob'
    """
    if isinstance(start, int) and start < 1: start = 1 # guard next statement
    start = start if start else o # None, 0 are both False, guard above needed
    start = start if start > 0 else 1
    end = end if end else start
    for iline in range(start, end+1):
        if not printline(iline):  # False if we reached end of buffer
            break

def v(nlines=None):
    """
    Page down, print next nlines lines starting with the line after dot.
    Default nlines is pagesize, if nlines present assign to nlines.
    Set dot to last line printed, print error message if we reach end of buf.
    This is z command in classic ed, but name here is from emacs C-v command.
    """
    global pagesize
    nlines = nlines if nlines else pagesize
    pagesize = nlines
    p(o+1, o+pagesize)

def mv(nlines=None):
    """
    Page up, print previous nlines lines ending with the line before dot.
    Name is from emacs M-v command.
    """
    global pagesize, o
    nlines = nlines if nlines else pagesize
    pagesize = nlines
    start, end = o-(pagesize+1), o-1
    p(start, end)
    o = start # p puts dot at end

def s(target=None, forward=True):
    """
    Search to end of buffer for next line containing target string.
    Default searches forward, set forward=False to search backward.
    If target found, print line and assign to dot.
    If target not found, leave dot unchanged and print '? <target> not found'
    Assign target to searchstring for use in future searches.
    If target is omitted, use stored searchstring.  
    """
    global o, searchstring
    found = False
    target = target if target else searchstring
    searchstring = target
    for iline in range(o+1,S()+1) if forward else range(o-1,0,-1):
        if target in buffer[iline]:
            found = True
            print(buffer[iline], end='') # line already ends with \n
            o = iline
            break
    if not found:
        print("? '%s' not found" % searchstring)

def r(target=None):
    'Search backward to start of buffer for next line containing target string'
    s(target, forward=False)

# Editing functions

def a(iline=None):
    'a(ppend) lines after iline (default dot), type just . on a line to exit'
    global buffer, o, saved
    iline = iline if iline else o
    if iline < 0 or iline > S():
        print('? %d out of range, last line is %d' % (iline, S()))
        return
    o = iline
    while True:
        success = False
        line = input()  # Can this fail?  Yes, by ^C for example
        success = True
        if success:
            if line == '.':
                return
            buffer[o+1:o+1] = [line + '\n'] # sic, append line after dot
            o +=1
            saved = False

def d(start=None, end=None):
    """
    d(elete) lines start through end *inclusive*.
    Save deleted lines in yank (paste) buffer.
    Set dot to last line *preceding* deletion, 
    so we can then use y(ank) to replace the deletion.
    """
    global buffer, yank, o, saved
    start = start if start else o
    end = end if end else start
    if start < 1 or start > S():
        print('? start %d out of range, last line is %d' % (start, S()))
        return
    if end != start and (end < 1 or end > S()):
        print('? end %d out of range, last line is %d' % (start, S()))
        return
    if start > end:
        print('? start %d follows end %d' % (start, end))
        return
    yank = buffer[start:end+1] # range includes end, unlike Python slices
    buffer[start:end+1] = [] 
    o = start-1
    saved = False

def y(iline=None):
    'Append yank buffer contents after iline (defalt dot)'
    global buffer, o, saved
    iline = iline if iline else o
    if iline < 0 or iline > S():
        print('? %d out of range, last line is %d' % (iline, S()))
        return
    buffer[iline+1:iline+1] = yank # append yank buffer contents after iline
    o = iline + len(yank)
    saved = False
