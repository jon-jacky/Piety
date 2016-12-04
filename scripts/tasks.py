"""
tasks.py - Creates a Session instance with three console jobs:
            a shell, a line editor, and a display editor.

Each job is a Job instance that supervises a Console instance
that wraps its application.

This module has a main function that runs the session in a while loop,
without the Piety scheduler.
"""

import piety, pyshc, edc, eden

session = piety.Session(name='session', input=sys.stdin)

# Python shell

# assign reader=key.Key that handles some multicharacter control sequences
job.pysh, cmd.pysh = console_job(controller=console, prompt='>> ', reader=key.Key(),  
                                 do_command=pysh.mk_shell(), startup=pysh.start, 
                                 stopped=(lambda command: not pysh.running), # after exit()
                                 cleanup=piety.stop) # sets piety.cycle.running = False

# line editor, : prompt to show ed is running

# startup function handles optional filename argument and optional keyword arg.
def ed_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        job.ed.prompt = options['p']  # ed.prompt is not used by Piety
    ed.quit = False # enable event loop, compare to Job( stopped=...) arg below
    # The following two commands are initialized in ed but might be reassigned by edsel
    ed.print_lz_destination = sys.stdout # restore ed output from p l z commands
    ed.x_cmd_fcn = ed.cmd # not edsel.cmd which calls update_display

job.ed, cmd.ed = console_job(controller=console,
                             prompt=': ', reader=key.Key(),  
                             do_command=ed.cmd, startup=ed_startup, 
                             stopped=(lambda command: ed.quit)) # after q command

# display editor, % prompt to show edsel is running

# startup function handles optional filename argument and optional keyword arg.
def edsel_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        job.edsel.prompt = options['p'] # edsel.prompt is not used by Piety
    ed.quit = False # enable event loop, compare to Job( stopped=..) arg below
    ed.print_lz_destination = open(os.devnull, 'w') # discard output
    ed.x_cmd_fcn = edsel.cmd  # calls update_display
    edsel.init_session(*filename, **options)

job.edsel, cmd.edsel = console_job(controller=console, 
                                   prompt='% ', reader=key.Key(), 
                                   do_command=edsel.cmd, startup=edsel_startup,
                                   stopped=(lambda command: ed.quit), # after q cmd
                                   cleanup=edsel.restore_display)

# main method for test and demonstration

def main():
    """
    Run the session without the Piety scheduler.
    Instead just use an ordinary while loop as a simple blocking event loop.
    """
    piety.cycle.running = True # not using Piety scheduler, just this flag
    job.pysh() # start the first job, which can start others
    while piety.cycle.running: # job.pysh.cleanup sets this False
        session.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
