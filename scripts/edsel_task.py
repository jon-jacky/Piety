"""
edsel_tasks.py - Creates a console Session instance with just one Job - edsel.
                  based on console_tasks.py, see its header for explanation

BUT unlike console_tasks, we start up edsel immediately and exit piety at edsel q.
No other console tasks besides edsel, so edsel_startup,cleanup differ from console_tasks.
"""

import sys
import piety, command, keyboard, key
import pysh, ed, edsel

class Namespace(object): pass 
job = Namespace() # avoid name clashes between job names and  module names
cmd = Namespace() # ditto for command names

# Session, a terminal task
console = piety.Session(name='console', input=sys.stdin)

# display editor
cmd.edsel = command.Command(prompt='', reader=key.Key(), handler=edsel.cmd)

# unlike console_tasks, only start edsel once, so we don't need edsel_startup, 
# and unlike console_tasks, exit piety at edsel q so we do need edsel_cleanup.

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()
    
job.edsel = piety.Job(session=console, application=cmd.edsel, startup=edsel.init_session,
                    stopped=(lambda: ed.quit or cmd.edsel.command == keyboard.C_d),
                    cleanup=edsel_cleanup)

# main method for test and demonstration

def main():
    'Run edsel under the piety scheduler'
    job.edsel() # start edsel
    piety.run() # exit from edsel calls piety.stop()

if __name__ == '__main__':
    main()
