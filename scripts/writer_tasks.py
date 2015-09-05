"""
writer_tasks.py - Create Piety Writer tasks used by embedded and embedded.twisted

When the Piety scheduler is running, task t0 writes to file w0.txt on
every timeout, and task t1 writes to w1.txt on every other timeout.

The shell command: tail -f w0.txt shows the t0 task in action.
"""

import piety # for Piety Task class, schedule data structure etc.
from writer import Writer # applications

w0,w1 = Writer(fname='w0.txt'),Writer(fname='w1.txt')

# use this for t1.guard
def alternate():
    'Return True on every other timeout event.'
    return bool(piety.ievent[piety.timer]%2)

t0 = piety.Task(handler=w0.write,input=piety.timer,enabled=piety.true)
t1 = piety.Task(handler=w1.write,input=piety.timer,enabled=alternate)
