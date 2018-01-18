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
>> edsel()
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

import sys, piety
from salysh import pysh
from edda import ed
from desoto import edsel

session = piety.Session(name='session', input=sys.stdin)

pysh.start = (lambda: session.start(pysh))
ed.start = (lambda: session.start(ed))
edsel.start = (lambda: session.start(edsel))
pysh.exit = ed.exit = edsel.exit = session.switch
pysh.cleanup = piety.stop # sets piety.cycle.running = False

# FIXME we didn't import desoto!  Also InputLine is gone
# So update() can restore cursor after updates from background task
# desoto.edsel.ed.buffer.inputline = desoto.console.command # InputLine instance

# Test

def main():
    piety.cycle.running = True # not using Piety scheduler, just this flag
    pysh.start()  # start the first job, which can start others
    pysh.resume() # cannot call pysh() here because it sets Console.replaced
    while piety.cycle.running: # pysh.cleanup sets this False
        session.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
