"""
Like run_piety but include writer tasks also for convenience

 $ python -i run_piety_writers.py
... only t1 is writing ...
piety> t0.enabled=piety.true
... now t0 is writing also ...

"""

import sys
from writer import Writer

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

w0,w1 = Writer(fname='w0.txt'),Writer(fname='w1.txt')

# use this for t1.guard
def alternate():
    """
    Returns True on every other timeout event
    """
    return bool(piety.ievent[piety.timeout]%2)

# writer tasks assigned guard=(lambda:False) so they don't start running
t0 = piety.Task(handler=w0.write,event=piety.timeout,enabled=piety.false)
t1 = piety.Task(handler=w1.write,event=piety.timeout,enabled=alternate)

# default guard=(lambda:True) so start running immediately
shell = console.Console(command=pysht.mk_shell(), exiter=piety.exit)
t2 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

run_piety()
