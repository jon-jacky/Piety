"""
writer.py - Functions that put text into editor buffers and windows,
             intended to be called from background tasks.

See writer.txt for more notes and explanation. 
"""

import display
import sked as ed
import edsel as fr  # short for 'frame'
import editline as el
import pmacs as pm
import pyshell as sh

# Redefine these functions from edsel to also restore cursor to point
 
def restore_cursor_to_cmdline():
    'Unlike version in edsel, this version also sets column to point'
    fr.restore_cursor_to_cmdline() # puts cursor in col 1
    el.move_to_point(sh.point, sh.start_col)    

saved_focus = -1 # index of focus window *before* we switch to print tick msg

def restore_cursor():
    ## sh.cmd_mode = False # DEBUG for testing n_windows() == 2 case from REPL
    if sh.cmd_mode: # editing/running Python commands at pysh REPL
        restore_cursor_to_cmdline() # redefined above, not the version in edsel
    # This next case assumes other window is tocus window that needs restoring
    # BUT if current window is intended focus window, this switches focus away
    elif fr.n_windows() == 2: # HACK only works in this n == 2 special case
        ## display.putstr(f'SWITCH WINDOW from {ed.bufname}') # DEBUG
        fr.save_window(fr.focus) 
        fr.focus = saved_focus
        fr.restore_window(saved_focus)
        pm.restore_cursor_to_window()
        ## display.putstr(f'AT POINT in {ed.bufname}') # DEBUG
    else: # There is no other window, cursor is already where it is needed.
        pass 

# Local refresh and recenter in this module are copied from edsel
# except here refresh does not call update_status 
# so it doesn't call restore_cursor_to_cmdline, which we don't want.

def refresh():
    """
    Refresh the focus window.
    (Re)Display lines from segment, marker, status without moving segment.
    """
    display.put_cursor(fr.wintop, 1) # top line in window
    fr.erase_lines(fr.wheight-1) # erase entire window contents above status line
    fr.update_window() # FIXME did we really have to erase_lines before this?
    fr.put_marker(ed.dot, display.white_bg)
    # fr.update_status() # NOT! we don't want restore_cursor_to_cmdline
    
def recenter():
    'Move buffer segment to put dot in center, display segment, marker, status'
    # global buftop # use edsel.buftop instead
    fr.buftop = fr.locate_segment(ed.dot)
    refresh() # redefined above, not the version in edsel

def write(line):
    """
    Append line to end of current sked buffer and display in edsel focus window.
    line is a string that does not end with \n, this write() adds it.
    """
    if line not in ('', '\n'): # redirect_stdout and file=... append extra \n
        ed.buffer.append(line.rstrip('\n\r') + '\n') # line might have many \n
        ed.dot = ed.S()  # last line in buffer, which we just added.
        if fr.in_window(ed.dot):
            display.put_cursor(fr.wline(ed.dot), 1)
            display.putstr(line[:fr.tcols])
        else:
            recenter() # redefined above, not the version in edsel
        restore_cursor()

def writebuf(bname, line):
    """
    Write to a buffer that might not be the current buffer.
    If the named buffer is present in saved buffers, append line to its end.
    If the named buffer is visible in the focus window, update that window.
    line is a string that does not end with \n, this function adds it.
    """
    if line not in ('', '\n'): # redirect_stdout and file=... append extra \n
        if bname in ed.buffers:
            # bname may not be ed.bufname, named buffer may not be current buffer
            ed.buffers[bname]['buffer'].append(line.rstrip('\n\r') + '\n')
            ed.buffers[bname]['dot'] = len(ed.buffers[bname]['buffer'])-1
            # Current buffer text lines are the same as text lines in saved buffers
            # BUT current buffer dot might not be the same, so must assign here
            if bname == ed.bufname: ed.dot = ed.S()
            # If the named buffer is visible in the focus window, update that window
            # Focus window dot might not be at the end of the buffer
            if bname == ed.bufname: # name of current buffer
                if fr.in_window(ed.dot): # assumes focus window shows current buffer
                    display.put_cursor(fr.wline(ed.dot), 1)
                    display.putstr(line[:fr.tcols])
                else:
                    recenter() # redefined above, not the version in edsel
                restore_cursor()
    
def writebuf_show(bname, line):
    """
    Call writebuf to update buffer bname with line.
    If buffer bname is in focus window, called writebuf will display it.
    If buffer bname is in a window that is not the focus window, first make
     that the focus window, then call writebuf to update buffer and display it.
    If buffer bname is not in a window on the display, writebuf will update
     it but not display it.
    If buffer bname is not in buffers, writebuf does not attempt to update it.
    """
    global saved_focus # index of focus window before weswitch to print tick msg
    wk = -1  # can't be a window key
    # search for key of window that shows buffer bname
    for wk in fr.windows: # wk is integer window key
        if fr.windows[wk]['bufname'] == bname:
            break
    # if window with named buffer found, change focus - based on fr.on code
    if wk in fr.wkeys and wk != fr.focus:  # if not found, wk is still -1
        fr.save_window(fr.focus) 
        saved_focus = fr.focus
        fr.focus = fr.wkeys[wk]
        fr.restore_window(wk)
    writebuf(bname, line)

class Writer():
    """
    Provide a method named write so we can redirect output to the named buffer.
    Our buffers are just dicts not objects so they have no write method.
    Usage:  abuf = Writer('a.txt')  then: with redirect_stdout(abuf) as buf: ...
    Recall that a is the name of the sked/edsel append fcn, can't use a = ..
    """
    def __init__(self, bufname): self.bufname = bufname
    def write(self, line): writebuf_show(self.bufname, line)
    
