"""
Like run_piety but include writer tasks also for convenience

 python -i run_piety_writers

But then both writers are started with guard=(lambda:False) so
they won't run until you revise guard.

"""

import sys
from writer import Writer

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
    piety.done = False # reset, might be resuming after piety.exit() 
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

r = run_piety # abbreviation, 'resume'

w0,w1 = Writer(fname='w0.txt'),Writer('w1.txt')

# writer tasks assigned guard=(lambda:False) so they don't start running
t0 = piety.Task(handler=w0.write,event=piety.timeout,guard=(lambda:False))
t1 = piety.Task(handler=w1.write,event=piety.timeout,guard=(lambda:False))

# use this for t1.guard
alternate = (lambda: bool(piety.ievent%2)) # every other event

# default guard=(lambda:True) so start running immediately
shell = console.Console(command=pysht.mk_shell(), exiter=piety.exit)
t2 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

run_piety()
