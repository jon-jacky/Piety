"""
run_timestamps.py - Uses the Piety scheduler to run the three jobs
  created by session.py, concurrently with the two timestamp tasks
  created here.

The timestamp tasks write to editor buffers named ts1 and ts2.
Display these buffers using the edsel display editor commands 'b ts1'
and 'b ts2' to see the buffers update as each timestamp is written.

The code that writes to the editor buffers demonstrates how to use 
the Buffer class write method and update attribute.
"""

import terminal, display, piety, timestamp, session

# We haven't started display editor yet, window not initialized, 
#  so use ed commands
edsel = session.editor.edsel
ed = edsel.ed

# Put some content in main buffer
ed.i('This is the main buffer') 

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')

# create buffers for timestamp messages
ed.b('ts1')
ed.b('ts2')

# return to main buffer
ed.b('main')

# aliases for timestamp buffers
ts1buf = ed.buffers['ts1']
ts2buf = ed.buffers['ts2']

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
    session.pysh()
    piety.run()

if __name__ == '__main__':
    main()
