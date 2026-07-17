# aiotimers.py,  async timers demos

import sked as ed

from edsel import e, b, o2, on
from viewer import oe
from apmacs import apm

from atimers import ATimer
from writer import Writer
from eventloop import piety

# Assigned by starttimer, below.  Can handle any number of timers.
timer = dict()
buf = dict()
ttask = dict()

def starttimer(label, n, delay):
    # Start a timer in current window, in the buffer named label + '.txt'
    global t, buf, ttask
    bufname = label + '.txt'
    if bufname == ed.bufname:
        pass # buffer already displayed in current window
    elif bufname in ed.buffers:
        b(bufname) # buffer already created, load into current window
    else:
        e(bufname) # create buffer in window
    timer[label] = ATimer()
    buf[label] = Writer(bufname)
    ttask[label] = \
        piety.create_task(timer[label].atimer(n, delay, label.upper(), 
                            buf[label]))
        
def stoptimer():
    # Stop the timer running in the current window, if there is one
    global timer
    label = ed.bufname.removesuffix('.txt')
    if label in timer:
        timer[label].exit = True
 
def onetimer():
    """
    async timer task demo: run timer in one editor window, edit in the other.
    Based on standalone demo pmacs_script.py.
    """
    oe() # put cursor in editor window
    o2() # split editor window
    e('a.txt')
    starttimer('a',1000,1)
    on() # put cursor in other window so we can edit
    apm() # resume display editing in windows
         
def twotimers():
    """
    async timer task demo: run timers in two editor windows.
    Based on standalone demo edsel_script.py, supercedes vedsel_script.py
    """
    oe() # put cursor in editor window
    o2() # split editor window
    e('a.txt')
    starttimer('a',1000,1)
    on() # put cursor in other window so we can open b.txt
    e('b.txt')
    starttimer('b',1000,0.5)
    apm() # resume display editing in windows
          
