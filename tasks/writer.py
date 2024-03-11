"""
writer.py - Functions that put text into sked buffers and edsel windows,
             intended to be called from background tasks.

See writer.txt for more notes and explanation. 
"""

import display
import sked as ed
import edsel as fr  # short for 'frame'

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
            fr.restore_cursor_to_cmdline()
        else:
            fr.recenter()

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
                    fr.restore_cursor_to_cmdline()
                else:
                    fr.recenter()
    
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
    wk = -1  # can't be a window key
    # search for key of window that shows buffer bname
    for wk in fr.windows: # wk is integer window key
        if fr.windows[wk]['bufname'] == bname:
            break
    if wk in fr.wkeys and wk != fr.focus:  # if not found, wk is still -1
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


