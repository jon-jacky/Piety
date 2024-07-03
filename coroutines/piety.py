"""
piety.py - Start the asyncio event loop, here named piety, for interactive use:

          $ python3 -m piety 
          ... type RET once to get prompt ...
          >>>> piety # Just for example, confirm the event loop is running
          <_UnixSelectorEventLoop running=True closed=False debug=False>
          ... etc., any Python statements, including piety.create_task(...) ...
          >>>> ^D
          $
          ... exit() also exits ... 

Statements in this script that follow run_forever() are not executed.
At the >>>> prompt, you cannot import scripts that import this module
(to get the piety identifier for example)  because this module already
starts the asyncio event loop.

For running demo and test scripts, use the piety_script.py module instead.
"""

import sys, asyncio
from apyshell import apysh # Custom Python shell that runs in the event loop.

piety = asyncio.get_event_loop()
piety.add_reader(sys.stdin, apysh)
piety.run_forever()

# Statements in this script that follow run_forever() are not executed.
# For example these are NOT executed:
 
from atimers import atimer
piety.create_task(atimer(5,1))

