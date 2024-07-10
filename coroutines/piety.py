"""
piety.py - Start an interactive Python shell running in an asyncio event loop 
            named piety.  Import a function named run to run scripts from that 
            shell, which can use that piety event loop.   See piety.txt.
"""

import sys, asyncio
from apyshell import apysh # Custom Python shell that runs in the event loop.

# So we can run scripts that name piety from the apysh >>>> prompt
# Identifiers assigned in the script remain in the session.
from runner import run

piety = asyncio.get_event_loop()
piety.add_reader(sys.stdin, apysh)

print('Type RETURN (or ENTER) once to get the interactive Piety prompt >>>> ')
piety.run_forever()

# Statements in this script that follow run_forever() are not executed.
# For example these are NOT executed:  
from atimers import atimer
piety.create_task(atimer(5,1))

