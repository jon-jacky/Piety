"""
console_task.py - Test console object running as a task under Piety scheduler.
                 Imports console_debug, the instrumented version of console.
                 This module is based on edsel.py and getkey_task.py
"""

import sys # for sys.stdin
import console_debug, piety

echo = console_debug.Console(prompt=(lambda: '> '), process_line=print)

console1 = piety.Task(name="console", input=sys.stdin, 
                     handler=echo.handler, enabled=piety.true)

def main():
    echo.main() # echo console object method
    piety.run()

#if __name__ == '__main__':
#    main()

