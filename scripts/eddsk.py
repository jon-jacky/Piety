"""
eddsk.py - Run a pysh Python shell, ed and edd editors in a Session.
 Use command and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler yet - just use loop.

  $ python -i eddsk.py
 pysh shell, type any Python statement, exit() or Ctrl-D to exit
 >> console.run(edc)   # run the ed line editor
 ...
 q                     # exit ed, return to pysh Python shell
 >> console.run(eddc)  # run the edd display editor
 ...
 q
 >> exit()             # exit from pysh Python shell
 >>>                   # Back to regular Python shell

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

# Python shell
pyshc = command.Command(startup=banner, prompt='>> ', 
                        reader=key.Key(), handler=pysh.mk_shell(), 
                        stopcmd='exit()', suspend=pexit)

# console session, initially runs Python shell
# Then use console to run other commands from shell: console.run(edc) etc.
console = session.Session(name='console', event=sys.stdin, job=pyshc)

# line editor
edc = command.Command(prompt='', handler=ed.cmd, reader=key.Key(),
                      stopcmd='q', suspend=console.stop) 

# display editor
eddc = command.Command(prompt='', startup=edd.init_display, 
                       handler=edd.cmd, reader=key.Key(),
                       stopcmd='q', cleanup=edd.restore_display,
                       suspend=console.stop) 

def main():
    """
    Run Python REPL and applications using pysh shell in a Session
    """
    global quit
    quit = False  # enable main loop, previous exit may have set this True
    console.foreground()
    while not quit:
        console.handler()

if __name__ == '__main__':
    main()
