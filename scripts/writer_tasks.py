"""
writer_tasks.py - Create Piety Writer tasks used by embedded and embedded.twisted
"""

import piety # for Piety Task class, schedule data structure etc.
from writer import Writer # applications

w0,w1 = Writer(fname='w0.txt'),Writer(fname='w1.txt')

# use this for t1.guard
def alternate():
    'Return True on every other timeout event.'
    return bool(piety.ievent[piety.timeout]%2)

# writer tasks assigned guard=(lambda:False) so they don't start running
t0 = piety.Task(handler=w0.write,event=piety.timeout,enabled=piety.true)
t1 = piety.Task(handler=w1.write,event=piety.timeout,enabled=alternate)
