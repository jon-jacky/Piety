# Piety/bin/statup.py  Startup file for micropython.  
# Start session from Piety.micro dir with: ...$ micropython -i bin/startup.py

import sys

# Set search path for importing Python modules
PIETY = '/home/jon/Piety.micro/'
sys.path += [ PIETY+'viewer', PIETY+'browser', PIETY+'console',
    PIETY+'python', PIETY+'unix', PIETY+'vt_terminal', 
    PIETY+'editors', PIETY+'tasking', PIETY+'threads', 
    PIETY+'coroutines', PIETY+'piety', PIETY+'python-stdlib' ]

