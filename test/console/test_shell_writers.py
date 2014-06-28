"""
test_shell_writers.py - demonstrate Peity scheduler with Python shell and writers

 $ python -i test_shell_writers.py
pysh>> x  \ =^U
pysh>> 'Both writers are writing!'
'Both writers are writing!'
pysh>> x = 42
pysh>> ^C
...
KeyboardInterrupt
>>> x
42
>>> test()
pysh>> 'Both writers have resumes\sd!'
'Both writers have resumed!'
pysh>>

"""

import sys
import console
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
shell = console.Console(prompt='pysh>> ', command=pysht.mk_shell(main_gbls),
                        exiter=piety.exit)

console.focus = shell

pysh = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def test():
    """ call piety.run()
    """
    shell.restart() # clear buffer, print prompt
    piety.run() # loop forever, don't return

if __name__ == '__main__':
    test()
