"""
console_tasks.py - Creates a console Session instance with three Job instances

The three jobs are the pysh shell, the ed line editor, and the edsel display
editor.  

The application in each job is a Command instance, each with its own
reader method, that reads and possibly preprocesses its input.  The
Command instance also provides in-line editing, and command history.

This module has a main function that runs the session in a simple
blocking event loop, without the Piety scheduler.

This script starts the non-blocking pysh Python shell, with the prompt
>> (two not three >).  When editing the pysh command line, control
keys and arrow keys work.  Exit the pysh shell with exit() or ^D.

To start the ed line editor: job.ed(), job.ed('README.md'), job.ed('README.md',
p=':') etc.  Both command arguments, the file name and the ed command
prompt character, are optional.

To start the edsel display editor: job.edsel(), job.edsel('README.md',h=12,p=':')
etc.  All three command arguments, the file name, the edsel command
prompt character, and the scrolling command region height in lines,
are optional.

Exit ed or edsel with the q command or ^D.

When editing the ed or edsel command line, control keys and arrow keys work,
see console/command.txt
"""

import os, sys
import piety, command, keyboard, key
import pysh, ed, edsel

class Namespace(object): pass 
job = Namespace() # avoid name clashes between job names and  module names
cmd = Namespace() # ditto for command names

# Session, a terminal task
console = piety.Session(name='console', input=sys.stdin)

# Python shell

# Put pysh command in cmd namespace to avoid name clash with pysh module
# here assign handler=key.Key that handles some multicharacter control sequences
cmd.pysh = command.Command(prompt='>> ', handler=key.Key(),  
                           do_command=pysh.mk_shell(),
                           stopped=(lambda command: 
                                    not pysh.running or command == keyboard.C_d))

# Put pysh job in the jobs namespace to avoid name clash with pysh module
# stopped=... enables exit on exit() command or ^D
job.pysh = piety.Job(application=cmd.pysh, controller=console, 
                     startup=pysh.start, cleanup=piety.stop)

# line editor

cmd.ed = command.Command(handler=key.Key(),  do_command=ed.cmd,
                         stopped=(lambda command: 
                                  ed.quit or command == keyboard.C_d))


# startup function handles optional filename argument and optional keyword arg.
def ed_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        cmd.ed.prompt = options['p']  # ed.prompt is not used by Piety
    # The following two commands are initialized in ed but might be reassigned by edsel
    ed.print_lz_destination = sys.stdout # restore ed output from p l z commands
    ed.x_cmd_fcn = ed.cmd # not edsel.cmd which calls update_display
    ed.quit = False # enable event loop, compare to Job( stopped=...) arg below

job.ed = piety.Job(application=cmd.ed, controller=console, startup=ed_startup)
              
# display editor

cmd.edsel = command.Command(handler=key.Key(), do_command=edsel.cmd,
                            stopped=(lambda command: 
                                     ed.quit or command == keyboard.C_d))

# startup function handles optional filename argument and optional keyword arg.
def edsel_startup(*filename, **options):
    if 'p' in options:
        cmd.edsel.prompt = options['p'] # edsel.prompt is not used by Piety
    ed.quit = False # enable event loop, compare to Job( stopped=..) arg below
    ed.print_lz_destination = open(os.devnull, 'w') # discard output
    ed.x_cmd_fcn = edsel.cmd  # calls update_display
    edsel.init_session(*filename, **options)

job.edsel = piety.Job(application=cmd.edsel, controller=console, 
                      startup=edsel_startup, cleanup=edsel.restore_display)

# main method for test and demonstration

def main():
    """
    Run the console session without the Piety scheduler.
    Instead just use an ordinary while loop as a simple blocking event loop.
    """
    job.pysh() # start the first job
    while pysh.running: # pysh module here, different from job.pysh 
        console.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
