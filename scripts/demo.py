"""
run_timestamps.py - Demonstrates many features of the Piety system.
  Uses the Piety scheduler to run the three jobs created by
  session.py, concurrently with the two timestamp tasks created here.
  Each timestamp task uses the print function to update an editor
  buffer.  You can see these buffers update in their windows as you
  edit in another window
"""

import terminal, display, piety, timestamp

# session.editor is the edsel module, session.edsel is the edsel Console job
from session import pysh, ed, edsel, jobs, fg, editor# so we can say ed() etc.

import ed as ed_api  # we already imported ed from session

# Put some content in main buffer
ed_api.i('This is the main buffer')

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')

# create buffers for timestamp messages
ed_api.b('ts1')
ed_api.b('ts2')

# return to main buffer
ed_api.b('main')

# aliases for timestamp buffers
ts1buf = ed_api.buffers['ts1']
ts2buf = ed_api.buffers['ts2']

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
    pysh()
    piety.run()

if __name__ == '__main__':
    main()
