# vpmacs_script.py
# async demo - You can edit in one window while a timer task updates the other.
# This version runs in the Piety desktop, modified from  pmacs_script.py
# Uses >>>> import vpmacs_script_import   not   >>>> run('vpmacs_script.py')
#
# ...$ python3 -im piety  # loads eventloop, defines piety and piety_start
# >>>> piety_start()
# >>>> import vpmacs_script
# ... windows appear, you can start typing in scratch.txt window ...

from edsel import e, o2, on
from viewer import oe
from apmacs import apm

from atimers import ATimer
from writer import Writer
from eventloop import piety

# So we can call it repeatedly at the REPL
def ttask():
    return piety.create_task(ta.atimer(1000, 1, 'A', abuf))

oe() # put cursor in editor window
o2() # split editor window
e('a.txt')
ta = ATimer()  
abuf = Writer('a.txt')
ta_task = ttask()
on() # put cursor in other window so we can edit
apm() # resume display editing in windows




