"""
session.py - Creates a Session instance with four console jobs:
             the pysh shell, the ed line editor, and the 
             edda and edsel display editors.

Each job is a Console instance that wraps its application.

This module has a main function that runs the session in a while loop,
without the Piety scheduler.
"""

import sys
import piety
import salysh, edna, desoto
import edsel as edselm # so edsel job name does not hide edsel module

# Console jobs
pysh = salysh.pysh
ed = edna.ed
edda = desoto.edda
edsel = edselm.edsel

session = piety.Session(name='session', input=sys.stdin, jobs=[pysh,ed,edda,edsel])

# convenient abbreviations for the command line
jobs = session.jobs # list jobs and their states
fg = session.fg # resume most recently suspended job
edm = edna.edo.ed # ed module, needs different name from ed console job
frame = desoto.editor.frame
text = edm.text

pysh.name = 'pysh'
pysh.start = (lambda: session.start(pysh))
pysh.cleanup = piety.stop # sets piety.cycle.running = False

ed.name = 'ed'
ed.start = (lambda: session.start(ed))

edda.name = 'edda'
edda.start = (lambda: session.start(edda))

edsel.name = 'edsel'
edsel.start = (lambda: session.start(edsel))

pysh.exit = ed.exit = edda.exit = edsel.exit = session.switch

# can start or resume with session.main()
def main():
    piety.cycle.running = True # not using Piety scheduler, just this flag
    pysh.main()  # start the first job, which can start others
    while piety.cycle.running: # pysh.cleanup sets this False
        session.handler()  # block waiting for each single character

if __name__ == '__main__':
    main()
