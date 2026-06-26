# atimer_demo.py
# async demo - You can edit in one window while a timer task updates the other.
# This version runs in the Piety desktop, based on  vpmacs_script.py
# 
# Must already be running event loop to run this demo, for example by:
#   import piety
# >>>> piety.piety_start()
# Importing this module loads the necessaries but does not start the demo.
#   import atimer_demo
#   from atimer_demo import onetimer
# To start the demo, call this function:
# >>>> onetimer()
# Some interesting things to try:
# >>>> piety.piety # confirm eventloop is running
# < ...EventLoop running=True ...>
# >>>> asyncio.all_tasks(piety)
# .... ATimer.atimer() ...
# >>>> from atimer_demo import ta # must do this each time after onetimer()
# >>>> ta.delay
# >>>> 1
# >>>> ta.delay = 0.1  # speed up timer
# >>>> ta.run
# True
# >>>> ta.run = False # Stop running timer
# >>>> asyncio.all_tasks(piety)
# set()
# >>>> k() # remove a.txt buffer
# >>>> onetimer()  # open new a.txt buffer and start a new timer
# ...

from edsel import e, o2, on
from viewer import oe
from apmacs import apm

from atimers import ATimer
from writer import Writer
from eventloop import piety

# So we can call it repeatedly at the REPL
# BUT actually that's not useful, we just call onetimer again.
def ttask(ta, abuf):
    return piety.create_task(ta.atimer(1000, 1, 'A', abuf))

# Assigned by demo onetimer() below
# Make these global so they don't vainsh when onetimer exits
ta = None
abuf = None
ta_task = None
 
# Call this to start demo 
def onetimer():
    global ta, abuf, ta_task
    oe() # put cursor in editor window
    o2() # split editor window
    e('a.txt')
    ta = ATimer()  
    abuf = Writer('a.txt')
    ta_task = ttask(ta, abuf)
    on() # put cursor in other window so we can edit
    apm() # resume display editing in windows




