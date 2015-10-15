"""
edsel_timestamps.py -  Initialize edsel and timestamp applications.
 Start edsel session using its own blocking event loop, not piety event loop.

To update ts1 buffer with new timestamp: !print(next(ts1),file=ts1buf)
"""

import edsel # creates edsel.ed.buffers with main buffer
import timestamp

# add content to main buffer
# we haven't started edsel yet, window not initialized, use edsel.ed commands
edsel.ed.cmd('i')
edsel.ed.cmd('This is the main buffer')
edsel.ed.cmd('.')

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')
# create buffers for timestamp messages
edsel.ed.cmd('b ts1')
edsel.ed.cmd('b ts2')
# aliases for timestamp buffers
ts1buf = edsel.ed.buffers['ts1']
ts2buf = edsel.ed.buffers['ts2']
# add content to timestamp buffers
print(next(ts1), file=ts1buf)
print(next(ts2), file=ts2buf)

# start interactive edsel session, blocking main loop
edsel.main(h=15)
