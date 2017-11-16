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
resumed.  Moreover the line editor ed and the display editor desoto
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
>> desoto()
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

import sys, piety, salysh, edda, desoto as editor

session = piety.Session(name='session', input=sys.stdin)

pysh = piety.Job(supervisor=session,
                 application=salysh.console,
                 handler=salysh.console.handler,
                 startup=salysh.console.restart, # no separate pysh.startup
                 cleanup=piety.stop) # sets piety.cycle.running = False

def edstartup():
    edda.ed.quit = False
    edda.ed.configure() # restore ed to no display, no updates
    edda.console.restart()

ed = piety.Job(supervisor=session,
               application=edda.console,
               handler=edda.console.handler,
               startup=edstartup)

def desotostartup():
    editor.ed.quit = False
    editor.edsel.startup(c=12)
    editor.console.restart()
 
# copied from editor_job.py
desoto = piety.Job(supervisor=session,
                 application=editor.console,
                 handler=editor.console.handler,
                 startup=desotostartup,
                 cleanup=editor.edsel.cleanup)

# So update() can restore cursor after updates from background task
editor.edsel.ed.buffer.inputline = editor.console.command # InputLine instance

# Test

def main():
    piety.cycle.running = True # not using Piety scheduler, just this flag
    pysh() # start the first job, which can start others
    while piety.cycle.running: # job.pysh.cleanup sets this False
        session.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
