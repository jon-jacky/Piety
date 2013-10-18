"""
test_shell_writers.py - demonstrate Peity scheduler with Python shell and writers

 $ python -i test_shell_writers.py
piety> x  \ =^U
piety> 'Both writers are writing!'
'Both writers are writing!'
piety> x = 42
piety> ^C
...
KeyboardInterrupt
>>> x
42
>>> test()
piety> 'Both writers have resumes\sd!'
'Both writers have resumed!'
piety>

"""

import sys
from console import Console
from writer import Writer
import pysht
import piety

w0,w1 = Writer(fname='w0.txt'),Writer('w1.txt')

t0 = piety.Task(handler=w0.write,event=piety.timeout)

t1 = piety.Task(handler=w1.write,event=piety.timeout)
t1.enabled = (lambda: bool(piety.ievent[piety.timeout]%2)) # every other event

# create shell here not in pysht module
#  so we can have multiple shell instances
main_gbls = sys.modules['__main__'].__dict__
shell = Console(prompt='piety> ', command=pysht.mk_shell(main_gbls))

t2 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def test():
    """ call piety.run()
    """
    shell.restart() # clear buffer, print prompt
    piety.run() # loop forever, don't return
    return n

if __name__ == '__main__':
    test()
