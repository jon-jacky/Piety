"""
demo.py - Runs edsel display editor
  concurrently with the two timestamp tasks created here.
  Each timestamp task uses the print function to update an editor
  buffer.  You can see these buffers update in their windows as you
  edit in another window
"""

import sys # for sys.stdin

import edsel, piety, timestamp

# Create the main buffer and add some content
edsel.text.startup('main')
edsel.ed.i('This is the main buffer')

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')

# create buffers for timestamp messages
edsel.ed.b('ts1')
edsel.ed.b('ts2')

# return to main buffer
edsel.ed.b('main')

# aliases for timestamp buffers
ts1buf = edsel.text.buffers['ts1']
ts2buf = edsel.text.buffers['ts2']

# add content to timestamp buffers
print(next(ts1), file=ts1buf)
print(next(ts2), file=ts2buf)

# use this for ts2task.guard - copied from writer_tasks.py
def alternate():
    'Return True on every other timeout event.'
    return bool(piety.ievent[piety.timer]%2)

# Tasks

# The edsel task handles keyboard input without blocking

console = piety.Task(name="console", input=sys.stdin, 
                     handler=edsel.edsel.handler, enabled=piety.true)

# Two timestamp tasks with their handlers

ts1handler = (lambda: print(next(ts1),file=ts1buf))
ts2handler = (lambda: print(next(ts2),file=ts2buf))

ts1task = piety.Task(handler=ts1handler, input=piety.timer, enabled=piety.true)
ts2task = piety.Task(handler=ts2handler, input=piety.timer, enabled=alternate)

def main():
    edsel.edsel.main() # edsel console object method, not edsel module function
    piety.run()

if __name__ == '__main__':
    main()
