"""
test_writers.py - demonstrate Peity scheduler with concurrent writer tasks
                  BUT no console task, no Python shell

Import this module into a Python session, then type wtest(30) -- or
any other integer argument -- to write that many lines in w0.txt and half
as many in w1.txt:

 $ python -i path.py                                                             
 >>> import test_writers                                      
 >>> test_writers.test(30)
 ... 30 lines are added to w0.txt and 15 to w1.txt ...
 30
 >>>

Use tail -f w0.txt and w1.txt in separate terminal windows to view
concurrent output.

"""

from writer import Writer
import piety

w0,w1 = Writer(fname='w0.txt'),Writer(fname='w1.txt')

t0 = piety.Task(handler=w0.write,event=piety.timeout)

t1 = piety.Task(handler=w1.write,event=piety.timeout)
t1.enabled = (lambda: bool(piety.ievent[piety.timeout]%2)) # every other event

def test(n):
    """ test(n) calls piety.run(nevents=n)
    """
    piety.run(nevents=n)
    return n








