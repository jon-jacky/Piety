"""
edsel_script.py - Display interleaving timer tasks in two editor windows.

edsel_script requires the running piety event loop, so it must be started
from the Piety shell with the run function.   See edsel_script.txt.
"""

from atimers import atimer
from writer import Writer
import sked
from sked import *
import edsel 
from edsel import *
win(22)
o2()
e('a.txt')
abuf = Writer('a.txt')
piety.create_task(atimer(10,1,'A',abuf))
on() 
e('b.txt')
bbuf = Writer('b.txt')
piety.create_task(atimer(20,0.5,'B',bbuf))
  
