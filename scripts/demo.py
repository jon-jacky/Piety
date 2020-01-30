"""
demo.py - Demonstrates many features of the Piety system.
  Uses the Piety scheduler to run the four jobs created by
  session.py, concurrently with the two timestamp tasks created here.
  Each timestamp task uses the print function to update an editor
  buffer.  You can see these buffers update in their windows as you
  edit in another window
"""

import terminal, display, piety, timestamp

from session import pysh, ed, edda, edsel # Console jobs
from session import jobs, fg # functions to type at Python command line
from session import edm, frame # modules that contain data structures

# This assigment needed so code in frame can restore Console cursor
#  after updates from background task
# FIXME - This is not sufficiently general.
#  This  is needed for each Console job when it reaches foreground.
#  Here we have just hard-coded it for the edsel Console.
#  On each timestamp tick, edsel cursor will be restored
#  but edda cursor will reset to start of line.
edm.buffer.console = edsel # Console instance

# Put some content in main buffer
edm.i('This is the main buffer')

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')

# create buffers for timestamp messages
edm.b('ts1')
edm.b('ts2')

# return to main buffer
edm.b('main')

# aliases for timestamp buffers
ts1buf = edm.buffers['ts1']
ts2buf = edm.buffers['ts2']

# add content to timestamp buffers
print(next(ts1), file=ts1buf)
print(next(ts2), file=ts2buf)

# define timestamp handlers and tasks

# use this for ts2task.guard - copied from writer_tasks.py
def alternate():
    'Return True on every other timeout event.'
    return bool(piety.ievent[piety.timer]%2)

ts1handler = (lambda: print(next(ts1),file=ts1buf))
ts2handler = (lambda: print(next(ts2),file=ts2buf))

ts1task = piety.Task(handler=ts1handler, input=piety.timer, enabled=piety.true)
ts2task = piety.Task(handler=ts2handler, input=piety.timer, enabled=alternate)

def main():
    pysh.main()
    piety.run()

if __name__ == '__main__':
    main()
