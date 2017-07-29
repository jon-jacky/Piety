"""
updates.py - Define display operations Op, display update record UpdateRec
"""

from enum import Enum
from collections import namedtuple

class Op(Enum):
    'Display update operations, named independently of particular programs'
    # update operations in buffer, refer to lines
    # m(ove), c(hange)/replace are just d(elete) then i(nsert)
    # ed e E are delete, then insert via r
    insert = 1  # Buffer methods: insert, also via ed a i m r t y but not c
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
    next = 10    # edsel o, switch to next window
    single = 11  # edsel o1, return to single window
    hsplit = 12  # edsel o2, split window, horizontal
    refresh = 13 # clear screen and redraw all windows
    rescale = 14 # rescale frame and window sizes, then refresh

# Record that describes a single display update.
# Most Op do not use all fields, and their meanings depend on Op, for example:
# Op.delete start, end are in origin, Op.insert start, end are in destination.
UpdateRecord = namedtuple('UpdateRecord', 
                          ['op','buffer','origin','destination','start','end'])
