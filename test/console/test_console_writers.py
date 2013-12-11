"""
test_console_writers.py - show that console does not block concurrent writers

 $ python -i test_console_writers.py
piety> abc
abc
piety> def
def
 ... lines are added to w0.txt and half as many to w1.txt ...
 ... meanwhile type at piety> prompts without blocking writers ...
 30
     >>>
>>> test(10)
piety> fjfjfj
fjfjfj
... again, lines appear in w0.txt and w1.txt as you type
piety> 10
      >>>

Use tail -f w0.txt and w1.txt in separate terminal windows to view
concurrent writers output.

"""

from writer import Writer
from console import Console
import piety

w0,w1 = Writer(fname='w0.txt'),Writer('w1.txt')

t0 = piety.Task(handler=w0.write,event=piety.timeout)

t1 = piety.Task(handler=w1.write,event=piety.timeout)
t1.guard = (lambda: bool(piety.ievent%2)) # every other event

c0 = Console()
t2 = piety.Task(handler=c0.getchar, event=piety.sys.stdin)

def test(n):
    """test(n) calls piety.run(nevents=n)
    """
    c0.restart() # clear buffer, print prompt
    piety.run(nevents=n)
    return n

if __name__ == '__main__':
    test(30)





