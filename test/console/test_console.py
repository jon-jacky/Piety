"""
test_console.py - demonstrate Peity scheduler with one console task

 $ python -i test_console.py
piety> abcdefgh\h\g\f^L
piety> abcde
abcde
piety> ^C
...
KeyboardInterrupt
>>> c0.command = print_3times
>>> test()
piety> efghi
efghi
output line 0 ...
output line 1 ...
output line 2 ...
 
"""

from console import Console
import piety

c0 = Console()

t0 = piety.Task(handler=c0.getchar, event=piety.sys.stdin)

def test():
    """ test() calls piety.run(nevents=0)
    """
    c0.restart() # clear buffer, print prompt
    piety.run(nevents=0) # loop forever, don't return

# Some sample command functions to try

line = 0

def print_3times(cmdline):
    global line
    print cmdline
    print 'output line %d ...' % line
    print 'output line %d ...' % (line + 1)
    print 'output line %d ...' % (line + 2)
    line += 3

def print_3lines(cmdline):
    global line
    print cmdline
    print """string line %d ....
string line %d ...
string line %d...
""" % (line, line + 1, line + 2)
    line += 3

if __name__ == '__main__':
    test()

