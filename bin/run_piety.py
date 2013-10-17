"""
Start piety at the command line:

 python -i run_piety.py  

Run Piety in an interactive Python session
If you exit from Piety or interrupt it, you will still be in Python
and can resume Piety with r()

"""

import sys

import console
import pysht
import piety

def run_piety():
    """ 
    setup terminal and (re)start piety
    must be one command at the python prompt
    """
    piety.done = False # reset, might be resuming after piety.exit() 
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

r = run_piety # abbreviation, 'resume'

shell = console.Console(command=pysht.mk_shell(), exiter=piety.exit)
t0 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

run_piety()
