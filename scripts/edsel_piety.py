"""
edse_piety.py - Runs edsel display editor under Piety scheduler
                made by cutting from timestamp_tasks.py
"""

import sys # for sys.stdin

import edsel, piety

# abbreviation so we can use module names without prefix
ed = edsel.ed
text = edsel.text
frame = edsel.frame

# Create the main buffer and add some content
text.startup('main')
ed.i('This is the main buffer')

# The edsel task handles keyboard input without blocking

# don't call it console - that has a separate meaning in frame.py

console1 = piety.Task(name="console", input=sys.stdin, 
                     handler=edsel.edsel.handler, enabled=piety.true)

def main():
    edsel.edsel.main() # edsel console object method, not edsel module function.
    piety.run()

if __name__ == '__main__':
    main()

