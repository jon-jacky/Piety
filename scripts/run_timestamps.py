"""
run_timestamps.py - Uses the Piety scheduler to run the three jobs
  created by session.py, concurrently with the two timestamp tasks
  created here.   Each timestamp task uses the print function
  to update an editor buffer.

Some interesting commands to type at the editor command prompt:

 b ts1 - in the focus window, display the buffer that contains the
 timeout messages from ts1task.  This window updates each time the 
 task generates a new message, even when another window gets focus
 and updates as its text is edited.

 !ts1task.enabled=piety.false - disable ts1task so ts1 buffer stops updating

 !ts1task.enabled=piety.true -  enable ts1task so ts1 buffer resumes updating

 !piety.cycle.period=0.1 - cause ts1 buffer to update ten times a second

 !piety.cycle.period=1.0 - cause ts1 buffer to resume updating once a second

 !session.editor.edsel.frame.window.Window.nupdates=9990 - advance N counter
    shown near right edge of status line.

 !session.editor.edsel.frame.refresh() - refresh all windows and the command
    line.  This is also provided by the edsel L command.

 !session.editor.console.command.point - print index in command line or
    text line where next typed character will appear.
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
