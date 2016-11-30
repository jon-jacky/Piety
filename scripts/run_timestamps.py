"""
piety_timestamps.py - Uses the Piety scheduler to run the console
  session with three jobs created by console_tasks, concurrently with
  the two timestamp tasks created here.

The timestamp tasks write to editor buffers named ts1 and ts2.
Display these buffers using the edsel display editor commands 'b ts1'
and 'b ts2' to see the buffers update as each timestamp is written.

The code that writes to the editor buffers demonstrates how to use 
the Buffer class write method and update attribute.

See console_tasks header for directions on how to run the console jobs
including the edsel editor, except start ed with con.job.ed not just
job.ed etc.
"""

import terminal, display
import piety
import timestamp
import console_tasks as con

# add content to main buffer
# we haven't started edsel yet, window not initialized, use con.ed commands
con.ed.cmd('i')
con.ed.cmd('This is the main buffer')
con.ed.cmd('.')

# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')

# create buffers for timestamp messages
con.ed.cmd('b ts1')
con.ed.cmd('b ts2')

# aliases for timestamp buffers
ts1buf = con.ed.buffers['ts1']
ts2buf = con.ed.buffers['ts2']

# window update function
def update(buf):
    if con.console.foreground == con.job.edsel and con.ed.buf == buf:
        terminal.set_line_mode()
        con.edsel.win.update_window(True) # command mode not insert mode
        # restore cursor to edsel cmd line (bottom of scroll region), edit point
        display.put_cursor(con.edsel.cmd_n, con.cmd.edsel.point+1) 
        terminal.set_char_mode() # FIXME should restore whatever was before
        
# add window update callbacks to timestamp buffers
ts1buf.update = (lambda: update(ts1buf))
ts2buf.update = (lambda: update(ts2buf))

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
    'Run the console session and writer tasks concurrently under the event loop'
    # con.job.pysh() runs its startup(), calls pysh.start() sets pysh.running=True
    con.job.pysh() # start the first job, recall pysh is in jobs namespace
    # piety.run() calls its piety.start() which sets eventloop.running=True
    piety.run() # start event loop, until pysh >> exit() triggers piety.stop()

if __name__ == '__main__':
    main()
