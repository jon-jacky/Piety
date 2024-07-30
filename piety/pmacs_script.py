# pmacs_script.py   Edit in one window while timer task updates the other:
#
# ...$ python3 -m piety
# >>>> run('pmacs_script.py')
# ... windows appear, you can start typing in scratch.txt window ...

import sked
from sked import *
import edsel  
from edsel import *
from atimers import ATimer
from writer import Writer
from apmacs import apm

win(22)
o2()
e('a.txt')
ta = ATimer()
abuf = Writer('a.txt')
piety.create_task(ta.atimer(1000,1,'A',abuf))
on()
apm()

