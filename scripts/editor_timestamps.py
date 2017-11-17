"""
editor_timestamps.py - Demonstrate printing to editor buffers.  Use
 while blocking event loop in editor.main, not piety event loop.

To update ts1 buffer with new timestamp: !print(next(ts1),file=ts1buf)
"""

import timestamp
import desoto as editor 

# We haven't started display editor yet, window not initialized, 
#  so use ed commands.
ed = editor.edsel.ed

# Put some content in main buffer
ed.i('This is the main buffer') 
# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')
# create buffers for timestamp messages
ed.b('ts1')
ed.b('ts2')
# aliases for timestamp buffers
ts1buf = ed.buffers['ts1']
ts2buf = ed.buffers['ts2']
# add content to timestamp buffers
print(next(ts1), file=ts1buf)
print(next(ts2), file=ts2buf)

# start interactive editor session, its own blocking main event loop
editor.main(c=12)
