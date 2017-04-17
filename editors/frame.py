"""
frame.py - collection of windows 

Just a module, not a class.  We expect only a single frame in a session.
"""

from enum import Enum
from collections import namedtuple, deque

class Op(Enum):
    'Generic window operations named independently of particular editor cmds'
    window = 1 # FIXME placeholder for edsel o o1 o2, add more Op values later

Update = namedtuple('Update', ['op','buffer','start','end','dest','nlines'])

updates = deque()

def update(op, buffer=None, start=0, end=0, dest=0, nlines=0):
    'Create an Update record and append it to the updates queue'
    # op is the only required (positional) argument
    updates.append(Update(op, buffer=buffer, start=start, end=end, dest=dest, 
                          nlines=nlines))

# move update_display from edsel into here also 

