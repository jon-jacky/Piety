"""
edsel_task - Edsel display editor with Command, Job, and Task classes.
               BUT without Session.  Use the Piety non-blocking event loop.
"""

import edsel, command, key, keyboard, piety, sys

console = command.Command(handler=key.Key())

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()

edselj = piety.Job(handler=console.handler, command=console,
                   do_command=edsel.cmd,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   restart=console.restart,
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
