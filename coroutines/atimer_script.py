"""
atimer_script.py - Demonstrate the Python shell and timer tasks interleaving
                   in the Piety event loop.

atimer_script requires the running piety event loop, so it must be started
from the Piety shell with the run function.  See atimer_script.txt. 
"""

from atimers import atimer
piety.create_task(atimer(10,1,'A'))
piety.create_task(atimer(20,0.5,'B'))

