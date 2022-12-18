"""
edsel_task.py - Runs edsel display editor as a single task 
 under the Piety scheduler.   Extracted from from demo.py
"""

import sys # for sys.stdin

import edsel, piety

# Create the main buffer and add some content
edsel.text.startup('main')
edsel.ed.i('This is the main buffer')

# The edsel task handles keyboard input without blocking

# don't call it console - that has a separate meaning in frame.py

console1 = piety.Task(name="console", input=sys.stdin, 
                     handler=edsel.edsel.handler, enabled=piety.true)

def main():
    edsel.edsel.main() # edsel console object method, not edsel module function
    piety.run()

if __name__ == '__main__':
    main()
