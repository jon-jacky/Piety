"""
test_plain.py - demonstrate Peity scheduler with one task: Python shell
                 with edit='plain', no ansi cursor control,
                 could work on a printing terminal

Piety shell uses the __main__ namespace to find, store variables

$ python -i test_plain.py
pysh>> x = 42
pysh>> __name__
'__main__'
pysh>> dir()
['Console', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'main_gbls', 'piety', 'pysht', 'shell', 'sys', 't0', 'test', 'x']
pysh>> ^C
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
pysh>> x
666
pysh>> 

"""

import sys
import console
import pysht
import piety

# create shell here not in pysht module
#  so we can have multiple shell instances
main_gbls = sys.modules['__main__'].__dict__
shell = console.Console(prompt="pysh>> ", command=pysht.mk_shell(main_gbls),
                        exiter=piety.exit, edit='plain') # override edit='ansi'
                        
console.focus = shell

pysh = piety.Task(handler=shell.getchar, event=piety.sys.stdin)

def test():
    """ call piety.run(nevents=0)
    """
    shell.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

if __name__ == '__main__':
    test()
