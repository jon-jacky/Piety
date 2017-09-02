"""
session.py - Creates a Session instance with three console jobs:
            a shell, a line editor, and a display editor.

Each job is a Job instance that supervises a Console instance
that wraps its application.

This module has a main function that runs the session in a while loop,
without the Piety scheduler.

Here is a typical session, that shows how to invoke each job.  The
pysh job (a Python interpreter) runs at startup.  Invoke the other
jobs from the Python prompt using function call syntax (which invokes
each job's __run__ method).  Exit from each job to return to the
Python interpreter.  Each job (including the Python interpreter)
preserves its state between invocations, so work in progress can be
resumed.  Moreover the line editor ed and the display editor eden
share the same state including editor buffers and insertion points.

...$ python3 -m session
>> dir()
...
>> ed()
: e README.md
... edit in README.md
:q
>> import datetime
...
>> eden()
... display editor appears, shows README.md
... continue editing README.md
:q
>> datetime.datetime.now()
... datetime module is still imported
>> ed()
... continue editing README.md
:q
>> exit()
...$

"""

import sys, piety, pyshc, edc, eden as editor

session = piety.Session(name='session', input=sys.stdin)

pysh = piety.Job(controller=session,
                 handler=pyshc.console.handler,
                 restart=pyshc.console.restart,
                 cleanup=piety.stop) # sets piety.cycle.running = False

pyshc.console.supervisor = pysh

def edstartup():
    edc.ed.quit = False
    edc.ed.configure() # restore ed to no display, no updates

ed = piety.Job(controller=session,
               handler=edc.console.handler,
               startup=edstartup,
               restart=edc.console.restart)

edc.console.supervisor = ed

# copied from editor_job.py
eden = piety.Job(controller=session,
                 handler=editor.console.handler,
                 startup=(lambda: editor.edsel.startup(c=12)),
                 restart=editor.console.restart, 
                 cleanup=editor.edsel.cleanup)

editor.console.supervisor = eden

# Test

def main():
    piety.cycle.running = True # not using Piety scheduler, just this flag
    pysh() # start the first job, which can start others
    while piety.cycle.running: # job.pysh.cleanup sets this False
        session.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
