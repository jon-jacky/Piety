"""
getkey_task.py - Like test in getkey.py main() but 
                 run as a task under the Piety scheduler,
                  modeled on editors/edsel_piety
"""

import sys # for sys.stdin
import util, terminal, key, getkey, piety

my_getkey = getkey.GetKey()

line = []
    
def getkey_handler():
    global line
    k = my_getkey()
    line += [k]
    util.putstr(k)

    if k == key.cr:
        terminal.set_line_mode()
        print() 
        print([ [c for c in k] for k in line ])
    # Now just ^C or whatever to get out of piety.run

getkey_task = piety.Task(name="getkey_task", input=sys.stdin, 
                         handler=getkey_handler, enabled=piety.true)
def main():
    util.putstr('> ')
    terminal.set_char_mode()
    piety.run()   # How do we exit when user types RET?

# Just start with python3 -i then >>> main() then ^C 
#if __name__ == '__main__':
#    main()
