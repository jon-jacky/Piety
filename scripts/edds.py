"""
edds.py - Run a pysh Python shell, ed and edd editors in a Session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler - just use loop
 Based on pyshs.py, edc.py
"""

import sys
import pysh, ed, edd, command, key, session
import terminal # for main loop only

quit = False

def pexit():
    global quit
    quit = True
    console.stop()

def banner():
    print "pysh shell, type any Python statement, exit() or Ctrl-D to exit"

# Note here we assign pexit to job control suspend arg
pyshc = command.Command(startup=banner, prompt='>> ', handler=pysh.mk_shell(), 
                        stopcmd='exit()', suspend=pexit)

console = session.Session(name='console', event=sys.stdin, job=pyshc)

# here we leave default cleanup arg None, but assign callback to suspend arg
edc = command.Command(prompt='', handler=ed.cmd, 
                      stopcmd='q', suspend=console.stop) 

eddc = command.Command(prompt='', startup=edd.init_display, handler=edd.cmd, 
                       stopcmd='q', cleanup=edd.restore_display,
                       suspend=console.stop) 


# FIXME - doesn't reassign k.handler when foreground is reassigned by session
# k = key.Key(console.foreground.handle_key)

def main():
    """
    Python REPL using home-made pysh shell in a Session
    """
    global quit
    quit = False  # enable main loop, previous exit may have set this True
    console.foreground()
    while not quit:
        # for now skip Key, call console directly
        # only single-char keys work here, not keyboard arrow keys
        ch = terminal.getchar()
        console.handle_key(ch)
    
if __name__ == '__main__':
    main()
