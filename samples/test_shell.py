"""
test_shell.py - demonstrate Peity scheduler with one task: Python shell

Piety shell uses the __main__ namespace to find, store variables

Import this module into a Python session, then type run() to begin
handling console input:

 $ python -i path.py
>>> __name__
'__main__'
>>> x = 42
>>> x
42
>>> import test_shell
>>> test_shell.run()
piety>>> x
42
piety>>> x = 666
piety>>> x
666
piety>>> 1+1
2
piety>>> "Hello world"
'Hello world'
piety>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys', 'test_shell', 'x']
piety>>> __name__
'__main__'
piety>>> ^C
...
KeyboardInterrupt
>>> x
666
>>> __name__
'__main__'


"""

import sys
from console import Console
import pysht
import piety

# create shell here not in pysht module
#  so we can have multiple shell instances
main_gbls = sys.modules['__main__'].__dict__
shell = Console(prompt='piety>>> ', command=pysht.mk_shell(main_gbls))

t0 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def run():
    """ call piety.run(nevents=0)
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return
