"""
session.py - Creates a Session instance with three console jobs:
            the pysh shell, the ed line editor, and the edsel display editor.

Each job is a Console instance that wraps its application.

This module has a main function that runs the session in a while loop,
without the Piety scheduler.
"""

import sys, piety
import console # just type console.jobs() to see the list

from salysh import pysh
from edda import ed
from desoto import edsel, editor # desoto edsel is Console, editor is edsel.py

session = piety.Session(name='session', input=sys.stdin, jobs=[pysh,ed,edsel])
jobs = session.jobs # jobs() list jobs and their states
fg = session.fg # fg() resume most recently suspended job

pysh.name = 'pysh'
pysh.start = (lambda: session.start(pysh))
pysh.cleanup = piety.stop # sets piety.cycle.running = False

ed.name = 'ed'
ed.start = (lambda: session.start(ed))

edsel.name = 'edsel'
edsel.start = (lambda: session.start(edsel))

pysh.exit = ed.exit = edsel.exit = session.switch

# So update() can restore cursor after updates from background task
editor.ed.buffer.inputline = edsel # Console instance

def main():
    piety.cycle.running = True # not using Piety scheduler, just this flag
    pysh()  # start the first job, which can start others
    while piety.cycle.running: # pysh.cleanup sets this False
        session.handler()  # block waiting for each single character 

if __name__ == '__main__':
    main()
