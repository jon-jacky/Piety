# MODIFIED FROM pmacs_script.py - this version assumes vpm.py has already run
# vpmacs_script.py   Edit in one window while timer task updates the other:
#
# ...$ cd Piety/piety  # so run(...) works without directory prefix
# ...$ python3 -im vpm
# >>> from runner import run
# >>> run('piety.py')
# Now event loop should be running, with async shell indicated by 4 >>>>
# >>>> piety
# ... EventLoop running=True ...
# >>>> run('vpmacs_script.py')
# ... windows appear, you can start typing in scratch.txt window ...

# Comment out redundant imports, vpm already imported these
#import sked
#from sked import *
#import edsel  
#from edsel import *

# Imports needed for timer demo
from atimers import ATimer
from writer import Writer
from apmacs import apm

# vpm already called win()
#win(22)

# Timer demo
o2()
e('a.txt')
ta = ATimer()
abuf = Writer('a.txt')
ta_task = piety.create_task(ta.atimer(1000,1,'A',abuf))
on() # next window
# apm() # begin display editing # DEBUG - type this at command line.

