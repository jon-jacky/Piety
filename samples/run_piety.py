"""
Start piety at the command line:

 python -i run_piety.py  

"""

import sys

# for now assume we're running in Piety/samples 
# put Piety/piety on the path so we can import those modules
sys.path.append('../piety') 

import console
import pysht
import piety

def run_piety():
    """ 
    setup terminal and (re)start piety
    must be one command at the python prompt
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

shell = console.Console(command=pysht.mk_shell(), exiter=piety.exit)
t0 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

run_piety()
