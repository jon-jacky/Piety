"""
console.py - The functions here call each of the functions in the shell
and pyhelp modules and redirect their output to an editor buffer.

Those editor buffers can be used much like terminal windows with scroll
back, so you can use system commands without exiting the Python session, or
resorting to the host desktop.

Shell command output is appended to the *Console* buffer, except
man("topic") output is redirected to a new buffer named topic.man.
help(topic) output is redirected to a new buffer named topic.help.
              
Each of the functions here has the same name as the function it calls in
the shell or pyhelp module, so in an interactive session, 'from shell
import *' then 'from console import *' will write over the names of the
functions in the shell module.
"""

from contextlib import redirect_stdout

from redirect import redirect
import shell, pyhelp
import sked as ed
import edsel as fr # frame
 
def sh(cmd):
    'Runs the shell in a subprocess, shell executes cmd'
    redirect('*Console*', lambda: shell.sh(cmd), f"sh('{cmd}')")

def cd(path):
    'Change directory, calls os.chdir'
    redirect('*Console*', lambda: shell.cd(path), f"cd('{path}')")    

def pwd():
    'Print working directory, calls os.cwd'
    redirect('*Console*', lambda: shell.pwd(), f"pwd()")
    
def ls(path='.'):
    'Runs ls -C for compact directory listing'
    redirect('*Console*', lambda: shell.ls(path), f"ls('{path}')")    

def lsl(path='.'):
    'Runs ls -l for long form directory listing in alphabetic order'
    redirect('*Console*', lambda: shell.lsl(path), f"lsl('{path}')")    

def lslt(path='.'):
    'Runs ls -lt for long form directory listing in chronological order'     
    redirect('*Console*', lambda: shell.lslt(path), f"lslt('{path}')")    

def man(topic):
    'Show man page on topic, a string.  Save in new buffer named topic.man'
    bufname = topic + '.man'
    fr.e(bufname)
    with redirect_stdout(ed): 
        shell.man(topic)
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
        pyhelp.help(topic)
    fr.p(1) # put the cursor at the top of the buffer
    fr.refresh()

