"""
atimer_script.py - demonstrate atimer task in the piety event loop.

atimer_script requires the running piety event loop, so it must be started
from piety_script:

   $ python -i
   >>> import piety_script
   >>> piety_script.start()
   ... You must type RET once to get the Piety >>>> prompt ...
   >>>> import atimer_script
   >>>>  1 2024-07-02 17:46:43.141700
   2 2024-07-02 17:46:44.144011
   ...
   >>>> ^D
   >>> ^D
   ... You must type ^D twice, first to exit from the event loop
   ... and then to exit from standard Python. exit() also exits from both.
   $
     
""" 

from piety_script import piety

from atimers import atimer
piety.create_task(atimer(5,1))

