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

# File and buffer functions

def e(fname): 
    'Load file named fname into buffer, replacing any previous contents.'
    global filename, buffer, o, saved
    try:
        with open(fname, mode='r') as fd:
            # fd.readlines reads file into a list of strings, one per line
            # First line of file is at index 1 not 0
            buffer = ['\n'] + fd.readlines() # each line in buffer ends with \n
    except FileNotFoundError:
        buffer = ['\n'] # start new file
    filename = fname
    o = S() # index of last line 
    print('%s, %d lines' % (filename, o))
    saved = True

def w(fname=None):
    'Write buffer to file, default name is in filename.'
    global filename
    fname = fname if fname else filename
    success = False # Might fail if path doesn't exist, no permission etc.
    with open(fname, 'w') as fd:
        fd.writelines(buffer[1:]) # first line of file is at index 1 not 0
        success = True
    if success:
        filename = fname
        print('%s, %d lines' % (filename, S()))
        saved = True

# File viewing functions

def st():
    'status, print information about editing session'
    print('%s, %d lines, at line %d, %s' %  (filename, S(), o,
          'no changes need to be saved' if saved else 'unsaved changes'))

def s(target=None):
    """
    Search forward to end of buffer for next line containing target string.
    If target found, print line and assign to dot.
    If target not found, do not change dot.
    Assign target to searchstring for use in future searches.
    If target is omitted, use stored searchstring.  
    NOTE: In Unix ed, s is substitute not search. Our ed.py uses c for subst.
    There is no search command in Unix ed, it is implicit in line address.
    """
    global o, searchstring
    found = False
    target = target if target else searchstring
    searchstring = target
    for iline in range(o+1,S()+1):
        if target in buffer[iline]:
            found = True
            print(buffer[iline], end='') # line already ends with \n
            o = iline
            break
    if not found:
        print("? '%s' not found" % searchstring)

def r(target=None):
    """
    Search backward to start of buffer for next line containing target string.
    Other details like s, above.
    NOTE: in Unix ed, r is read file not reverse search.  Our ed.py just has e.
    """
    global o, searchstring
    found = False
    target = target if target else searchstring
    searchstring = target
    for iline in range(o-1,0,-1): # search backwards
        if target in buffer[iline]:
            found = True
            print(buffer[iline], end='') # line already ends with \n
            o = iline
            break
    if not found:
        print("? '%s' not found" % searchstring)
            
def printline(iline):
    """
    Check line number within buffer, then print line or error message
    Return True if line printed, False if reached end of buffer
    Advance dot if line printed.
    """
    global o
    if iline <= S():
        print(buffer[iline], end='') # line already ends with \n
        o = iline
        return True
    else:
        print('? end of buffer')
        return False

def p(start=None, end=None):
    """
    Print range of lines from buffer, from index start through end.
    Default with no arguments prints the line at dot.
    With no end arg, just print the line at start.
    Set dot to index of last line printed.
    Print error message and return if we reach end of buffer
    """
    start = start if start else o
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
    d(elete) lines from buffer and save in yank (paste) buffer
    set dot to line preceding deletion, can use a(ppend) to replace deletion
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
