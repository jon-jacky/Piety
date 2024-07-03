"""
atimer_script.py - Demonstrate atimer tasks interleaving in the piety event loop.

atimer_script requires the running piety event loop, so it must be started
from piety_script:

   $ python3 -i
   >>> import piety_script
   >>> piety_script.start()
   ... You must type RET once to get the Piety >>>> prompt ...
   >>>> import atimer_script
   >>>> B 1 2024-07-03 10:13:03.997791
   A 1 2024-07-03 10:13:04.498137
   B 2 2024-07-03 10:13:04.498673
   B 3 2024-07-03 10:13:05.002520
   A 2 2024-07-03 10:13:05.500561
   ...
   >>>> ^D
   >>> ^D
   ... You must type ^D twice, first to exit from the event loop
   ... and then to exit from standard Python. exit() also exits from both.
   $
     
""" 

from piety_script import piety

from atimers import atimer
piety.create_task(atimer(10,1,'A'))
piety.create_task(atimer(20,0.5,'B'))

