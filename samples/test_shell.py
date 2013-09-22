"""
test_shell.py - demonstrate Peity scheduler with one task: Python shell

To create an interactive Python shell, just pass Python's eval function
to the Console constructor.

Import this module into a Python session, then type test() to begin
handling console input:

Jonathans-MacBook-Pro:samples jon$ python -i path.py
>>> import test_shell
>>> test_shell.run()
piety>>> 1=1^H^H^H^L
piety>>> 1 + 1
2
piety>>> dir()
['__builtins__', '__doc__', '__file__', '__name__', '__package__', 'python']
piety>>> x = 42
piety>>> x
42

BUT 

piety>>> ^C
...
KeyboardInterrupt
>>> x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined

Oh dear.
 
"""

from console import Console
import pysht
import piety

# create shell here not in pysht module
#  so we can have multiple shell instances
shell = Console(prompt='piety>>> ', command=pysht.python)

t0 = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def run():
    """ call piety.run(nevents=0)
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return
