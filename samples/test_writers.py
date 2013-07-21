"""
test_writers.py - demonstrate Peity scheduler with concurrent writer tasks

Import this module into a Python session, then type wtest(30) -- or
any other integer argument -- to write that many lines in w0 and half
as many in w1.  Use tail -f w0.txt and w1.txt in separate terminal
windows to view concurrent output,
"""

from writer import Writer
import piety

w0,w1 = Writer(fname='w0.txt'),Writer('w1.txt')

t0 = piety.Task(handler=w0.write,event=piety.timeout_event)

t1 = piety.Task(handler=w1.write,event=piety.timeout_event)
t1.guard = (lambda: bool(piety.ievent%2)) # every other event

def wtest(n):
    """ wtest(n) calls piety.run(nevents=n)
    """
    piety.run(nevents=n)
    return n








