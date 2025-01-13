"""
redirect.py - Redirect command output to editor buffers,
              so the buffers can act much like terminal windows.
"""

from contextlib import redirect_stdout

# sked has module-level write function that writes to the current buffer.
import sked as ed  
import edsel as fr # fr for frame
import host
 
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
    
def sh(cmd):
    redirect('*Console*', lambda: host.sh(cmd), f"sh('{cmd}')")

def cd(path):
    redirect('*Console*', lambda: host.cd(path), f"cd('{path}')")    

def pwd():
    redirect('*Console*', lambda: host.pwd(), f"pwd()")
    
def ls(path='.'):
    'host.ls() calls ls -C for compact listing'
    redirect('*Console*', lambda: host.ls(path), f"ls('{path}')")    

def lsl(path='.'):
    'host.lsl() calls ls -l for long form listing in alphabetic order'
    redirect('*Console*', lambda: host.lsl(path), f"lsl('{path}')")    

def lslt(path='.'):
    'host.lslt() calls ls -l for long form listing in chronological order'     
    redirect('*Console*', lambda: host.lslt(path), f"lslt('{path}')")    

def man(topic):
    'Show man page on topic, a string.  Save in new buffer named topic.man'
    bufname = topic + '.man'
    fr.e(bufname)
    with redirect_stdout(ed): 
        host.man(topic)
    fr.p(1) # put the cursor at the top of the buffer
    fr.refresh()

def help(topic):
    """
    Show help on topic, a Python object - module, function etc.
    Save in a new buffer named topic.help
    """
    bufname = topic.__name__ + '.help'
    fr.e(bufname)
    with redirect_stdout(ed):
        host.help(topic)
    fr.p(1) # put the cursor at the top of the buffer
    fr.refresh()

