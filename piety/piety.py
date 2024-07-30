"""
piety.py - Starts a Piety session.  Creates an event loop named
  *piety*, adds the readers for the shell and the editor, and starts the
  event loop with the shell running.  It also defines a funtion *run*
  which is needed to run other scripts in the event loop. 
"""

import sys, asyncio
import pyshell, apyshell, apmacs

# So we can run scripts that name piety from the apysh >>>> prompt
# Identifiers assigned in the script remain in the session.
from runner import run

# We could swap in in other shells and foreground jobs if we had them.
# Hard code these for now because we have no others - maybe more in the future.
shell = apyshell.apysh
fgjob = apmacs.apmrun # foreground job
 
def handler():
    if pyshell.cmd_mode:
        shell()
    else:
        fgjob()  

apyshell.running = True
apyshell.setup() # print >>>> prompt, etc.

piety = asyncio.get_event_loop()
piety.add_reader(sys.stdin, handler)
piety.run_forever()

# Statements in this script that follow run_forever() are not executed.
# For example these are NOT executed:  
from atimers import atimer
piety.create_task(atimer(5,1))

