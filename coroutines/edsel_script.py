"""
edsel_script.py - Display interleaving timer tasks in two editor windows.
You can set the timer intervals and stop the tasks from the Python REPL.

edsel_script requires the running piety event loop, so it must be started
from the Piety shell with the run function.   See edsel_script.txt.
"""

from atimers import ATimer
from writer import Writer
import sked
from sked import *
import edsel 
from edsel import *
win(22)
o2()
e('a.txt')
abuf = Writer('a.txt')
ta = ATimer()
piety.create_task(ta.atimer(10,1,'A',abuf))
on() 
e('b.txt')
bbuf = Writer('b.txt')
tb = ATimer()
piety.create_task(tb.atimer(20,0.5,'B',bbuf))
  
