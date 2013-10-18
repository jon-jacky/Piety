"""
test_shell.py - demonstrate Peity scheduler with one task: Python shell

Piety shell uses the __main__ namespace to find, store variables

$ python -i test_shell.py
piety> x = 42
piety> __name__
'__main__'
piety> dir()
['Console', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'main_gbls', 'piety', 'pysht', 'shell', 'sys', 't0', 'test', 'x']
piety> ^C
...
KeyboardInterrupt
>>> x
42
>>> __name__
'__main__'
>>> dir()
['Console', '__builtins__', '__doc__', '__name__', '__package__', 'main_gbls', 'piety', 'pysht', 'shell', 'sys', 't0', 'test', 'x']
>>> x = 666
>>> test()
piety> x
666
piety> 

"""

import sys
from console import Console
import pysht
import piety

# create shell here not in pysht module
#  so we can have multiple shell instances
main_gbls = sys.modules['__main__'].__dict__
shell = Console(command=pysht.mk_shell(main_gbls))

t0 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def test():
    """ call piety.run(nevents=0)
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

if __name__ == '__main__':
    test()
