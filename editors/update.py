"""
update.py - Define display updates: generic editing, buffer, window, operations 
             named independently of particular editors or other programs.
"""

from enum import Enum
from collections import namedtuple, deque

class Op(Enum):
    'Display update operations, named independently of particular programs'
    # update operations in buffer, refer to lines
    # m(ove), c(hange)/replace are just d(elete) then i(nsert)
    # ed e E are delete, then insert via r
    insert = 1  # Buffer methods: insert, also via ed a i r t y but not c
    delete = 2  # ed d, also via ed m c, ed e E but then insert via r
    mutate = 3  # ed s
    locate = 4  # ed l
    # update operations in ed, refer to buffers
    # ed D DD are remove, then select
    create = 5   # ed b, B via create_buf
    remove = 6   # ed D, DD but then Op.select
    select = 7   # ed b, D via select_buf
    # user interface in ed, toggle command mode/input mode (insert mode)
    input = 8    # ed a i c  enter input (insert) mode, from command mode.
    command = 9  # ed .  exit input (insert) mode, return to command mode
    # update operations in frame, refer to windows
    next = 10     # edsle o, switch to next window
    single = 11  # edsel o1, return to single window
    hsplit = 12  # edsel o2, split window, horizontal

# Record that describes a single display update
Update = namedtuple('Update', 
                    ['op','buffer','start','end','destination','nlines'])

# Queue of pending display updates from all tasks
updates = deque()

def update(op, buffer=None, start=0, end=0, destination=0, nlines=0):
    'Create an Update record and append it to the updates queue'
    updates.append(Update(op, buffer=buffer, start=start, end=end, 
                          destination=destination, nlines=nlines))
