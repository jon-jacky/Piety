"""
viewer.py  - Experiments with a viewer window beside the editor windows

The viewer has its own current buffer and its own window that are always
displayed and always available, which are implicitly selected by the 
commands (functions) defined in this module.

The editor current buffer and windows managed by the sked and edsel
modules, and the commands that use them, are unchanged, always
available, and work just as before.

Most of the code in this module is copied and just slightly edited from
sked and edsel, without apology. It's just a quick experiment.
"""

import sys # needed for sys.modules[__name__], this module 
from contextlib import redirect_stdout  # for console functions

import shell, pyhelp # fcns that are redirected to viewer window
import display, sked as ed, edsel as fr # frame
 
# Define and initialize global variables
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables,
# so we retain buffer contents and other state when we reload.
 
try:
    _ = dot # If dot is already defined, then this module was already imported.
except:
    # Variables copied from sked.
    # but viewer.buffer here is different from editor buffer sked.buffer - etc.
    # buffer is zero indexed, but we want first line of file to be at index 1
    # so first entry in buffer list is never used - it's always just '\n'
    buffer = ['\n']  # '\n' at index 0 is never used
    dot = 0   # dot, index of current line in buffer
    point = 0 # point, index of current column in dot. Not used here, for future  
    filename = 'scratch.txt' # reassigned by e(dit) and w(rite) commands
    bufname = filename  # Basename of filename, reassigned by e and w
    pagesize = 24         # reassigned by vv and vrv page up/down commands
    saved = True          # True when no unsaved changes, safe to run e(dit).
    
    # Variables copied from edsel
    # but single viewer window here is different from editor windows in edsel.
    wintop = 1 # index in frame of top line of focus window
    wheight = fr.flines # N of lines in focus window, including status line.
    buftop = 1 # index in buffer of line at the wintop, top of the window.

    # Variables not copied from sked or edsel
    ledge = 81 # left edge, viewer border
    start_col = 83 # starting column of viewer text
    width = 67 # width of viewer text
    saved_tcols = 150 # editor window columns, saved so vclr() can restore it.

# New functions, not based on sked or edsel, despite similar names

def vwin(vwidth=None):
    """
    Create empty viewer window to the right of the editor windows.
    Limit editor windows fr.tcols to 80, viewer window gets the rest
    """
    global ledge, start_col, width, saved_tcols, vcols
    if not vwidth: vwidth = 70 # assumes fr.termcols >= 140
    width = vwidth # width of viewer window inclding border
    saved_tcols = fr.tcols # so clr() can restore it
    fr.tcols = fr.termcols - width
    ledge = fr.tcols + 1  # Left edge of viewer
    start_col = ledge + 2  # Where text content begins 
    vcols = width - 2 # width of viewer content not counting border
    display.put_cursor(1,ledge)
    for iline in range(fr.flines - 1): # 0 indexed, preserve status line
        display.put_cursor(iline + 1, ledge) # terminal lines 1 indexed
        display.render('|', display.reverse) # L edge window border
        display.kill_line() # end of line to window R edge
    display.put_cursor(fr.flines, ledge)  # status line
    display.render('|' + (width-1)*' ', display.reverse)
    display.put_cursor(fr.tlines, 1) # return cursor to command line    
     
def vclr():
    """
    Clear viewer window.
    Restore fr.tcols, then can refresh editor windows to full width
    """
    for iline in range(fr.flines): # 0 indexed, clear status line also
        display.put_cursor(iline + 1, ledge) # terminal lines 1 indexed
        display.kill_line()
    fr.tcols = saved_tcols
    display.put_cursor(fr.tlines, 1) 

# Functions based on sked, copied from sked and edited
 
def o():
    # Copied from sked, not even edited, but uses viewer dot not sked.dot
    'Return dot, index of current line.  o looks a bit like classic ed .'
    return dot

def S():
    # Copied from sked, not edited, but uses viewer.buffer not sked.buffer
    'Return index of last line in buffer.  S looks a bit like classic ed $'
    return len(buffer)-1  # -1 because of zero based index


def status():
    # Copied from sked, not edited, uses viewer.S() etc. not sked.S() etc.
    'status: return string of information about editing session'
    return (f'{bufname}, at line {dot} of {S()}, file {filename}, ' 
            f"{'saved' if saved else 'unsaved changes'}")

def move_dot(iline):
    # Copied from sked, not edited, but uses viewer dot and point, not sked.dot
    'Assign iline to dot. Replacement function can then move display cursor'
    global dot, point
    dot = iline
    point = 0 # point on current line might be past end of destination line.

def restore_buffer(bname, printline=print):
    # Copied from sked, restores from sked.buffers,
    # but updates individual buffer variables in this viewer module.
    # BUT restores variables from the editors saved sked.buffers.
    'Restore state of saved buffer bname to current saved buffer'
    global bufname, filename, buffer, dot, point, saved
    # display.putstr(f'From {bufname} restore {bname}\n\r') # DEBUG
    bufname = ed.buffers[bname].get('bufname', 'no name')
    filename = ed.buffers[bname].get('filename', 'no filename')
    buffer = ed.buffers[bname].get('buffer', ['\n'])
    dot = ed.buffers[bname].get('dot', 0)
    point = ed.buffers[bname].get('point', 0)
    saved = ed.buffers[bname].get('saved', True)
    printline(status()) # print the new buffer name

def save_buffer():
    # Copied from sked, saves to sked.buffers, 
    # but saves individual variables in this viewer module.
    'Save state of current buffer including text, dot etc.'
    # global buffers
    ed.buffers[bufname] = {'bufname': bufname, 'filename': filename, 
                        'buffer': buffer, 'dot': dot, 'point': point,
                        'saved': saved }

def e(fname, move_dot=move_dot, restore_buffer=restore_buffer):
    # Copied from sked, but updates viewer buffer here not sked.buffer 
    """
    e(dit), load named file into buffer, replacing previous contents.
    But first save buffer state so it can be restored on command.
    """
    global filename, buffer, saved, bufname, prev_bufname
    if fname == filename:
        print(f'? file {fname} is already in the viewer buffer\r\n', end='')
        return
    for buffername in ed.buffers: # can't use bufname here - shadows sked.bufname
        bfname = ed.buffers[buffername].get('filename','no filename')
        if fname == bfname:
            b(buffername, restore_buffer) # visit existing buffer 
            return
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
    bufname = ed.bname(filename) # creates new buffer if e() on same file
    saved = True # put this *before* move_dot for display code
    move_dot(min(S(),1)) # start of buffer, empty buffer S() is 0
    save_buffer() # the new current buffer is also in the saved buffers
    print(f'{filename}, {S()} lines\n\r', end='')

def b(bname=None, restore_buffer=restore_buffer):
    # Copied from sked, but updates viewer buffer here not sked.buffer
    """
    b(uffer), save current buffer and restore named buffer.
    If buffer name not given, switch back to previous buffer
    If buffer name ends with ?, invoke poor person's tab completion:
    Treat that buffer name as a prefix and try to match with a real buffer name
    """
    global prev_bufname
    if bname and bname.endswith('?'): bname = ed.match_bufname(bname[:-1])
    if not bname: bname = prev_bufname
    if bname == bufname:
        print(f'? buffer {bufname} is already the viewer buffer\r\n', end='')
        return
    if bname in ed.buffers:
        prev_bufname = bufname
        if S() > 0: save_buffer()
        restore_buffer(bname)
    else:
        print(f'? no buffer {bname}\n\r', end='')

# Functions based on edsel, copied from edsel and edited.

def wbottom():
    # Copied from edsel, not even edited.
    # viewer wheight here can differ from split window edsel.wheight
    """
    Return index of line in frame that displays the last line in window.
    Usually this is the window's status line.
    """
    return wintop + wheight - 1

def locate_segment(iline):
    # Copied from edsel, not even edited.
    # viewer wheight here can differ from split window edsel.wheight
    """
    iline is line in the buffer.
    Select segment to put in window, that centers iline in the window.
    Return buftop, line in current buffer to put at top line in window
    """
    if iline < wheight - 1: # iline is near top of buffer, show first page
        return 1
    else: 
        return iline - (wheight // 2) # put iline near center of window

def update_status():
    # Copied from edsel, edited
    # Put cursor at viewer left edge, use viewer status not sked.status.
    'Update status line at the bottom of the window'
    display.put_cursor(wbottom(), ledge) # NB viewer left edge
    display.move_to_column(ledge) # added to viewer, not in edsel
    display.render(('| ' + status()).ljust(width)[:width],display.reverse)  
    fr.restore_cursor_to_cmdline()

def update_lines(bstart, wstart, nlines):
    # Copied from edsel, edited to use viewer buffer not ed.buffer
    # and also to put cursor at viewer window left edge.
    # Render the viewer window border each time to simplify refresh()
    """
    Display consecutive lines (a 'segment') from the buffer in the window.
    Display nlines, starting at bstart in buffer, starting at wstart in window.
    Clip nlines if needed, to fit in window, and not run past end of buffer.
    Leave cursor after the last line displayed, but do not update any globals.
    """
    nlines = min(nlines, wbottom()-wstart+1) # n of lines at end of window
    nlines = min(nlines, len(buffer)-bstart+1) # n of lines at e.o. buffer
    display.put_cursor(wstart, ledge) # NB viewer window left edge
    for line in buffer[bstart:bstart+nlines]:
        display.move_to_column(ledge) # added to viewer, not in edsel
        display.render('|', display.reverse) # ditto, L edge window border
        # must expand tabs so [:width-1] clips properly
        display.putstr((' ' + line.expandtabs().rstrip('\n'))[:width-1])
        display.kill_line() # end of buffer line to window edge
        display.next_line()

def update_window():
    # Copied from edsel, not edited.
    # Use viewer wheight, can differ from sked wheight in split window
    'Update entire window up to status line, starting at line buftop in buffer'
    update_lines(buftop, wintop, wheight-1)

def erase_lines(nlines):
    # Copied from edsel, edited
    # Do not kill_whole_line, put cursor at viewer window left edge firs.
    # Do not erase window left border
    """
    Completely erase nlines lines starting at current cursor position.
    Leave cursor at line after last line erased.  Do not update any globals.
    """
    for iline in range(nlines):
        #ndisplay.kill_whole_line()
        #FIXME wstart
        display.move_to_column(ledge+1) # added to viewer, not in edsel.
        display.kill_line()
        display.next_line()

def refresh():
    # Copied from edsel, no edits - but now its using viewer wintop etc.
    """
    Refresh the focus window.
    (Re)Display lines from segment, marker, status without moving segment.
    """
    display.put_cursor(wintop, 1) # top line in window
    erase_lines(wheight-1) # erase entire window contents above status line
    update_window() # FIXME did we really have to erase_lines before this?
    # put_marker(ed.dot, display.white_bg) # No marker in viewer window for now
    update_status()
     
def recenter():
    # Copied from edsel, change ed.do to viewer dot
    'Move buffer segment to put dot in center, display segment, marker, status'
    global buftop
    buftop = locate_segment(dot)
    refresh()

def display_e(iline):
    # Copied from edsel, comment out save_window_bufinfo, move_dot not ed.move
    'Display effect of ed e(dit) fcn: display new buffer contents around iline'
    move_dot(iline)
    # save_window_bufinfo() # NB commented out, only one viewer window
    recenter()

def display_restore_buffer(bname):
    # Copied from edsel, edited: use restore_buffer not ed.restore...
    # comment out save_window_bufinfo
    'Display effect of restore_buffer function, fill entire window'
    restore_buffer(bname, fr.print_nothing)
    # save_window_bufinfo() # NB commented out, only one viewer window
    recenter()

def scroll_segment(iline):
    # Copied from edsel, not edited, but now wheight is viewer not edsel
    """
    iline is line in the buffer.
    Select segment to put in window, that puts iline at last line in window.
    Return buftop, line in current buffer to put at top line in window
    """
    if iline < wheight - 1: # iline is near top of buffer, show first page
        return 1
    else: 
        return iline - (wheight - 2) # put iline at bottom of window

def scroll():
    # Copied from edsel, change ed.dot to dot
    'Move buffer segment to put dot at bottom, display segment, marker, status'
    global buftop
    buftop = scroll_segment(dot)
    refresh()

def line_valid(iline):
    # Copied from sked,  no edits but uses viewer S() not sked.S()
    """
    If iline is within buffer return True,
    otherwise print error message and return False.
    """
    if 0 < iline <= S():
        return True
    else:
        print(f'? line {iline} out of range 1 .. {S()}\n\r', end='')
        return False

def range_valid(start, end):
    # Copied from sked, no edits but uses viewer line_valid
    """
    If start .. end is within buffer return True,
    otherwise print error message(s) and return false.
    """
    return line_valid(start) and ((start == end) or line_valid(end)) 
 
def p(start=None, end=None, printline=fr.print_nothing, move_dot=move_dot):
    # Copied from sked, but uses viewer range_valid
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

def nodisplay_p(start=None, end=None):
    # Copied from edsel, edit to use viewer p and move_dot 
    # Move dot from start to end without displaying anything.
    # We need this because ed.v() requires it, see below.
    p(start, end, fr.print_nothing, move_dot)
 
def v(nlines=None, p=p):  # p is hook for display code
    # Copied from sked, no edits, but now uses viewer pagesize dot S()
    """
    v, page down, print next nlines lines starting with dot.
    Default nlines is pagesize, if nlines present assign to pagesize.
    Stop at end of buffer if we reach it.  Set dot to last line printed.
    """
    global pagesize
    if dot == S():
        print('? end of buffer\r\n', end='')
        return
    if nlines is None: nlines = pagesize
    pagesize = nlines
    p(dot, min(dot+pagesize-1, S()))

def rv(nlines=None, p=p, move_dot=move_dot):  # with hooks for display code
    # Copied from sked, no edits, but now uses viewer pagesize dot
    'r(everse) v, page up, print previous nlines lines ending with dot.'
    global pagesize
    if dot == 1:
        print('? start of buffer\r\n', end='')
        return
    if nlines is None: nlines = pagesize
    pagesize = nlines
    start = max(dot-pagesize, 1)
    p(start, dot)
    move_dot(start) # p puts dot at end

# New functions in viewer.  
# These are viewer e and b here, not sked e and b
def ve(fname):
    e(fname, display_e, display_restore_buffer)

def vb(bname=None):
    b(bname, display_restore_buffer)

def vv(nlines=None):
    # Copied from edsel.v(), rename to vv, call local v() not ed.v()
    # Call v() to move dot with error and range checking,
    #  but don't display from ed.v, instead call scroll().
    v(nlines, nodisplay_p)
    scroll()
    
def vrv(nlines=None):
    # Copied from edsel.rv(), rename to vrv, call local rv not ed.rv()
    rv(nlines, nodisplay_p, move_dot)
    scroll()

# Console functions - sh() cd() pwd() ls() etc. 

# write function supports redirection to viewer current buffer

def write(line):
    # Copied from sket but not edited, just use viewer dot buffer S()
    """
    Append line to end of viewer buffer.
    To be used implicitly by redirect_stdout(viewer) or print(..., file=viewer)
    If line is a string that does not end with \n, this write() adds it.
    """
    global dot
    if line not in ('', '\n'): # redirect_stdout and file=... append extra \n
        buffer.append(line.rstrip('\n\r') + '\n') # line might have many \n
        dot = S()  # last line in buffer, which we just added.
        
def redirect(vbufname, command, command_string):
    # Copied from redirect.py and edited.  See comments inline.
    # parameter is vbufname not bufname, a module level var here.
    """
    Redirect stdout from command to the editor buffer named bufname.
    command must be a callable without arguments that writes to stdout.
    command_string is the string that labels the command output in the buffer.
    If the bufname buffer does not exist, create it and make it current.
    If bufname already exists, make it the current buffer.     
    """
    # bufnames are the names of the buffers currently displayed in windows
    # bufnames = { fr.windows[k]['bufname'] for k in fr.windows }  
    # NOT!  There is only one buffer displayed in viewer window, viewer.bufname.
    # bufname buffer does not yet exist
    if not bufname in ed.buffers: 
        e(bufname) # create bufname buffer in the viewer window
    # bufname buffer exists but is not in viewer window
    elif vbufname in ed.buffers and vbufname != bufname:
        b(vbufname) # make bufname the current buffer in the viewer window    
    # vbufname buffer exists and is in  a window but is not the current buffer        
    # NOT - viewer doesn't have this case,  there is just one window
    # elif (bufname in ed.buffers and bufname in bufnames 
    #      and not bufname == ed.bufname): 
    #    fr.on() # switch to other window - only works when there are just two
    # bufname buffer exists and is in a windows and is the current buffer.
    elif (vbufname in ed.buffers ### and bufname in bufnames 
          and vbufname == bufname): 
         pass # we don't have to select buffer or switch window.
    else: # we never get here - all possibilities already covered
        pass # bufname is already the current buffer
    # Can we redirect_stdout to this module, viewer?  
    # NO, because at this point 'viewer' is not defined.
    #with redirect_stdout(viewer): # output goes to write fcn in sked module
    with redirect_stdout(sys.modules[__name__]): # __name__ here is viewer
        print('>>> ' + command_string) # print command to label its output
        command()
    scroll() # last line printed by command is at bottom of window

# Console functtions, opied from console.py, code looks the same
# but calls viewer redirect that writes to *VConsole* buffer and window.

def vsh(cmd):
    # Copied from console.py
    # Rename sh to vsh but no edits necessary, calls viewer redirect
    'Runs shell in subprocess, shell runs cmd, displays in viewer'
    redirect('*Console*', lambda: shell.sh(cmd), f"sh('{cmd}')")

