"""
ed.py - Line editor inspired by the classic Unix ed, but even simpler

There is no main function - just call these functions from Python REPL.
"""

from pycall import pycall

# buffer is zero indexed, but we want first line of file to be at index 1
# so first entry in buffer list is never used - it's always just '\n'
buffer = ['\n']  # '\n' at index 0 is never used
o = 0            # dot, index of current line in buffer.  o looks like ed .

filename = 'main'     # default, reassigned by e command
searchstring = 'main' # default, reassigned by s(earch) and r(everse) commands
pagesize = 12         # default, reassigned by z command

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

def z(nlines=None):
    """
    Scroll, print next nlines lines starting with the line after dot.
    Default nlines is pagesize, if nlines present assign to nlines.
    Set dot to last line printed, print error message if we reach end of buf.
    """
    global pagesize
    nlines = nlines if nlines else pagesize
    pagesize = nlines
    p(o+1, o+pagesize)

# We almost don't need a main method.
# Why not just call all the functions from the regular Python prompt?
# BUT we do need this for a few special cases:
# 1. Empty line calls advance() to go to advance to next line and print
# 2. q to exit
def main():
    """
    The ed command interpreter is just a home-made Python REPL 
    copied from shells/pycall.py main()
    """
    ps1 = '>> '  # first line prompt, different from CPython >>>
    ps2 = '.. '  # continuation line prompt
    continuation = False # True when continuation line expected

    while True:
        prompt = ps2 if continuation else ps1
        cmd = input(prompt)  # python -i makes readline editing work here.
        # Must trap exit() here, do *not* exit calling Python session.
        if cmd in ('exit()','q'): # q is standard ed quit command.
            break
        elif cmd == '':  # if no command, advance line and print
            advance()
        else:
            continuation = pycall(cmd)

if __name__ == '__main__':
    main()
