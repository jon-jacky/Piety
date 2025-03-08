"""
redirect.py - The redirect() function here redirects command output to
              editor buffers, so the buffers can act much like terminal windows
              with scroll back.               
"""

from contextlib import redirect_stdout

# sked has module-level write function that writes to the current buffer.
import sked as ed  
import edsel as fr # fr for frame
 
def redirect(bufname, command, command_string):
    """
    Redirect stdout from command to the editor buffer named bufname.
    command must be a callable without arguments that writes to stdout.
    command_string is the string that labels the command output in the buffer.
    If the bufname buffer does not exist, create it and make it current.
    If bufname already exists, make it the current buffer.     
    """
    # bufnames are the names of the buffers currently displayed in windows
    bufnames = { fr.windows[k]['bufname'] for k in fr.windows }  
    # bufname buffer does not yet exist
    if not bufname in ed.buffers: 
        fr.e(bufname) # create bufname buffer in the current window
    # bufname buffer exists but is not in any windows:
    elif bufname in ed.buffers and not bufname in bufnames:
        ed.b(bufname) # make bufname the current buffer in the current window    
    # bufname buffer exists and is in  a window but is not the current buffer        
    elif (bufname in ed.buffers and bufname in bufnames 
          and not bufname == ed.bufname): 
        fr.on() # switch to other window - only works when there are just two
    # bufname buffer exists and is in a windows and is the current buffer.
    elif (bufname in ed.buffers and bufname in bufnames 
          and bufname == ed.bufname): 
         pass # we don't have to select buffer or switch window.
    else: # we never get here - all possibilities already covered
        pass # bufname is already the current buffer
    with redirect_stdout(ed): # output goes to write fcn in sked module
        print('>>> ' + command_string) # print command to label its output
        command()
    fr.scroll() # last line printed by command is at bottom of window
