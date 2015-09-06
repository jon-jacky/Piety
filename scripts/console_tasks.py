"""
console_tasks.py - Creates a console Session instance with three Job instances

The three jobs are the pysh shell, the ed line editor, and the edd display
editor.  

The application in each job is a Command instance, each with its own
reader method, that reads and possibly preprocesses its input.  The
Command instance also provides in-line editing, and command history.

This module has a main function that runs the session in a simple
blocking event loop, without the Piety scheduler.

This script starts the non-blocking pysh Python shell, with the prompt
>> (two not three >).  When editing the pysh command line, control
keys and arrow keys work.  Exit the pysh shell with exit() or ^D.

To start the ed line editor: ed(), ed('README.md'), ed('README.md',
p=':') etc.  Both command arguments, the file name and the ed command
prompt character, are optional.  You can also use ed.main() etc.

To start the edd display editor: edd(), edd('README.md',h=12,p=':')
etc.  All three command arguments, the file name, the edd command
prompt character, and the scrolling command region height in lines,
are optional.  You can also use edd.main() etc.

Exit ed or edd with the q command or ^D.

When editing the ed or edd command line, control keys and arrow keys work,
see console/command.txt

"""

import sys
import piety, command, keyboard, key
import pysh, ed, edd

class Namespace(object): pass 
job = Namespace() # avoid name clashes between job names and  module names
cmd = Namespace() # ditto for command names

# Session, a terminal task
console = piety.Session(name='console', input=sys.stdin)

# Python shell

# Put pysh command in cmd namespace to avoid name clash with pysh module
# here assign reader=key.Key that handles some multicharacter control sequences
cmd.pysh = command.Command(prompt='>> ', reader=key.Key(),  
                           handler=pysh.mk_shell())

# Put pysh job in the jobs namespace to avoid name clash with pysh module
# stopped=... enables exit on exit() command or ^D
job.pysh = piety.Job(session=console, application=cmd.pysh, startup=pysh.start,
                      stopped=(lambda: not pysh.running 
                               or cmd.pysh.command == keyboard.C_d), 
                      cleanup=piety.stop)

# line editor

cmd.ed = command.Command(prompt='', reader=key.Key(),  handler=ed.cmd)

# startup function handles optional filename argument and optional keyword arg.
def ed_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        cmd.ed.prompt = options['p']  # ed.prompt is not used by Piety
    ed.quit = False # enable event loop, compare to Job( stopped=...) arg below

job.ed = piety.Job(session=console, application=cmd.ed, startup=ed_startup, 
                   stopped=(lambda: ed.quit or cmd.ed.command == keyboard.C_d))
              
# display editor

cmd.edd = command.Command(prompt='', reader=key.Key(), handler=edd.cmd)

# startup function handles optional filename argument and optional keyword arg.
def edd_startup(*filename, **options):
    if 'p' in options:
        cmd.edd.prompt = options['p'] # edd.prompt is not used by Piety
    edd.init_display(*filename, **options)
    ed.quit = False # enable event loop, compare to Job( stopped=..) arg below

job.edd = piety.Job(session=console, application=cmd.edd, startup=edd_startup, 
                    stopped=(lambda: ed.quit or cmd.edd.command == keyboard.C_d),
                    cleanup=edd.restore_display)

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
