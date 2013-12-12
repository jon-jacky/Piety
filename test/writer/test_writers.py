"""
test_writers.py - demonstrate Peity scheduler with concurrent writer tasks
                  BUT no console task, no Python shell

 python -i test_writers.py
... writes 20 lines to w0.txt and 10 to w1.txt...
>>> test(20)
... or any other integer argument -- writes that many lines
in w0.txt and half as many in w1.txt. ...
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

if __name__ == '__main__':
    test(20)
