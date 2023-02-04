"""
sked.py - Stone Knife Editor, minimal line editor inspired by classic Unix ed,
           but even simpler.

No main program!  Editor commands are just functions defined here, to
call from the Python REPL.

Global data used by these functions, includng the text buffer, are
defined and initialized elsewhere, in skedinit.py, so this sked module
can be reloaded into a running editor session after revising or adding
functions, without re-initializing variables and losing data.

skedinit is *conditionally* executed, only the first time this module
is imported in a Python session.  See code below.

The name sked is inspired by Kragen Sitaker's Stone Knife Forth.
"""

# Define and initialize global variables used by sked editing functions.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = o
except:
    exec(open("skedinit.py").read())

def S():
    'Return index of last line in buffer.  S looks a bit like classic ed $'
    return len(buffer)-1  # -1 because of zero based index

def e(fname): 
    'Load file named fname into buffer, replacing any previous contents.'
    global filename, buffer, o
    success = False # Might crash if fname doesn't exist etc.
    with open(fname, mode='r') as fd:
        # fd.readlines reads file into a list of strings, one per line
        # First line of file is at index 1 not 0
        buffer = ['\n'] + fd.readlines() # each string in buffer ends with \n
        success = True
    if success:
        filename = fname
        o = S() # index of last line 
        print('%s, %d lines' % (filename, o))

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

def advance():
    'Advance dot to next line and print'
    global o
    iline = o + 1
    printline(iline)

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
