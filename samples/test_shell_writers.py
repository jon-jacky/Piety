"""
test_shell_writers.py - demonstrate Peity scheduler with Python shell and writers

 $ python -i path.py
>>> import test_shell_writers
>>> x = 42
>>> __name__
'__main__'
>>> test_shell_writers.run(100)
piety>>> 
piety>>> 'Both writers are wriring^H^H^H^L
piety>>> 'Both writers are wrir^Hting!'
'Both writers are writing!'
piety>>> x
42
piety>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys', 'test_shell_writers', 'x']
piety>>> 1+1
2
piety>>> x = 666
piety>>> 100
            >>> x
666
>>> __name__
'__main__'

"""

import sys
from console import Console
from writer import Writer
import pysht
import piety

w0,w1 = Writer(fname='w0.txt'),Writer('w1.txt')

t0 = piety.Task(handler=w0.write,event=piety.timeout)

t1 = piety.Task(handler=w1.write,event=piety.timeout)
t1.guard = (lambda: bool(piety.ievent%2)) # every other event

# create shell here not in pysht module
#  so we can have multiple shell instances
main_gbls = sys.modules['__main__'].__dict__
shell = Console(prompt='piety>>> ', command=pysht.mk_shell(main_gbls))

t2 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def run(n):
    """ call piety.run(nevents=n)
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=n) # loop forever, don't return
    return n
