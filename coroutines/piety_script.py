"""
piety_script.py - Start the asyncio event loop, here named piety, 
                 for running demo and test scripts:

          $ python3 -i
          ...
          >>> import piety_script
          >>> piety_script.start() 
          ... You must type RET once to get the piety >>>> prompt ...
          >>>> piety # For example, to confirm the event loop is running
          <_UnixSelectorEventLoop running=True closed=False debug=False>
          ... etc., any Python statements, including import atimer_script etc.
          >>>> import atimer_script
          >>>>  1 2024-07-02 17:46:43.141700
          2 2024-07-02 17:46:44.144011
          ....
          >>>> ^D
          >>> ^D
          ... You must type ^D twice, first to exit from the event loop
          ... and then to exit from standard Python. exit() also exits from both.
          $

Here are the contents of the test script.   All test scripts that are run
from piety_script must begin with the same import statement, in order to use
the unqualified piety identifier as you would at the interactive >>>> prompt:

          # atimer_script.py - demonstrate atimer task in the piety event loop.
          from piety_script import piety
    
          from atimers import atimer
          piety.create_task(atimer(10,1,'A')) 
          piety.create_task(atimer(20,0.5,'B'))
"""

import sys, asyncio
from apyshell import apysh # Custom Python shell that runs in the event loop.

def start():
    global piety
    piety = asyncio.get_event_loop()
    piety.add_reader(sys.stdin, apysh)
    piety.run_forever()
 

