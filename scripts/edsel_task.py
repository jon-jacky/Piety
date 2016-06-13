"""
edsel_task - Edsel display editor with Command, Job, and Task classes.
               BUT without Session.  Use the Piety non-blocking event loop.
"""

import sys, piety, command, keyboard, key, edsel

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()

console = command.Command(handler=key.Key())

edselj = piety.Job(handler=console.handler, 
                   command=console.command,
                   restart=console.restart,
                   do_command=edsel.cmd,
                   startup=edsel.init_session,
                   stopped=(lambda command: 
                            edsel.ed.quit or command == keyboard.C_d),
                   cleanup=edsel_cleanup)

# assign callbacks
console.do_command = edselj.do_command
console.stopped = edselj.stopped

task = piety.Task(name='edsel', handler=edselj.handler, input=sys.stdin, 
                  enabled=piety.true)

def main():
    'Run edsel under the piety scheduler'
    edselj() # start edsel, edselc(c=15) shows more cmd lines
    piety.run() # exit from edsel calls piety.stop()

if __name__ == '__main__':
    main()
