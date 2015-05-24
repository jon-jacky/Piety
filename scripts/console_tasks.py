"""
console_tasks.py - Creates a console Session instance with three Job instances

The three jobs are the pysh shell, the ed line editor, and the edd display
editor.  

The application in each job is a Command instance, each with its own
reader method, that reads and possibly preprocesses its input.  The
Command instance also provides in-line editing, and command history.

This module has a main function that runs the session in a simple
blocking event loop, without the Piety scheduler.

This script start the pysh Python shell, with the prompt >> (two not
three >).  When editing the pysh command line, control keys and arrow
keys work.  Exit the pysh shell with exit() or ^D.

To start ed line editor, use edc not ed: edc() or edc('README.md') etc., 
When editing the ed command line, control keys work but and arrow keys do not work.
Exit ed with the q command, ^D does not work.

To start edd display editor: edd() or edd('README.md') or main.edd('README.md') ...
When editing the edd command line, control keys and arrow keys work.
Exit edd with the q command or ^D.
"""

import sys
import piety, command, keyboard, key
import pysh, ed, edd as _edd # rename edd module so we can use edd as job name

class Namespace(object): pass # another way to avoid name clashes
jobs = Namespace()

# Session, a terminal task
console = piety.Session(name='console', input=sys.stdin)

# Python shell

def pysh_startup():
    pysh.pexit = False # enable pysh event loop, compare to Job stopped= below

# Name the command pyshc to avoid name clash with pysh module
# Assign reader=key.Key that handles some multicharacter control sequences
pyshc = command.Command(prompt='>> ', reader=key.Key(),  handler=pysh.mk_shell())

# Put pysh job in the jobs namespace to avoid name clash with pysh module
# stopped=... enables exit on exit() command or ^D
jobs.pysh = piety.Job(session=console, application=pyshc, startup=pysh_startup, 
                      stopped=(lambda: pysh.pexit or pyshc.command == keyboard.C_d), 
                      cleanup=piety.quit)

# line editor

# startup function handles optional filename argument and optional keyword arg.
def ed_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        edc.application.prompt = options['p'] 
    ed.quit = False # enable event loop, compare to Job( stopped=...) arg below

# Name the job edc to avoid name clash with ed module.
# Use default reader, not key.Key, so multicharacter control sequences
#  (such as keyboard arrow keys) will not work.
# Exit with q only, ^D exit is not enabled
edc = piety.Job(session=console,
                application=command.Command(prompt='', handler=ed.cmd),
                startup=ed_startup, stopped=(lambda: ed.quit))
              
# display editor

# startup function handles optional filename argument and optional keyword arg.
def edd_startup(*filename, **options):
    _edd.ed.quit = False # enable event loop, compare to Job( stopped=..) arg below
    if 'p' in options:
        edd.application.prompt = options['p'] #edd *not* _edd, Piety command object
    _edd.init_display(*filename, **options) # _ed.prompt is not used by Piety

# edd module was imported as _edd so we can call the job edd without name clash
edd = piety.Job(session=console, 
                application=
                command.Command(prompt='', reader=key.Key(), handler=_edd.cmd),
                startup=edd_startup, 
                cleanup=_edd.restore_display)

# Enable exit with q or ^D, must use separate statement so application has a name
edd.stopped=(lambda: _edd.ed.quit or edd.application.command == keyboard.C_d)

# Make edd.main an alias for edd.__call__ so we can call edd.main(...) using
#  exactly the same syntax as when we import edd.py into Python without Piety
edd.main = edd.__call__


# main method for test and demonstration

def main():
    """
    Run the console session without the Piety scheduler.
    Instead just use an ordinary while loop as a simple blocking event loop.
    """
    jobs.pysh() # start the first job
    while not pysh.pexit: # pysh module here, different from jobs.pysh 
        console.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
