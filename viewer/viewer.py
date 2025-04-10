"""
viewer.py  - Experiments with a viewer window beside the editor windows
"""

import display
import sked as ed, edsel as fr # fr for frame

def update(bstart):
    """
    Update entire viewer window from sked current buffer, 
    starting at buffer line bstart.
    """
    fr.tcols = min(fr.tcols, 80) # make room for viewer
    ledge = fr.tcols + 1  # Left edge of viewer
    start_col = ledge + 2  
    width = fr.termcols - start_col
    display.put_cursor(1,ledge)
    for iline in range(fr.flines - 1): # 0 indexed, preserve status line
         display.put_cursor(iline + 1, ledge) # terminal lines 1 indexed
         display.render('|', display.reverse) # L edge window border
         display.putstr(' ') # L edge space before text
         if iline < len(ed.buffer) - 1:
             display.putstr(ed.buffer[bstart+iline].rstrip('\n')[:width])
         display.kill_line() # end of line to window R edge
         # display.next_line() # not needed, we put_cursor each time
    display.put_cursor(fr.flines, ledge)  # status line
    display.render('| ' + ed.bufname + (width-2-len(ed.bufname))*' ', display.reverse)
    display.put_cursor(fr.tlines, 1) # return cursor to command line
    
