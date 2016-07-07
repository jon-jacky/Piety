"""
edsel_task - Edsel display editor with Command, Job, and Task classes,
              BUT without Session.  Use the Piety non-blocking event loop.
              Contrast to edsel_cmd_job.
"""

import edsel, command, key, keyboard, piety, sys

console = command.Command(handler=key.Key(),
                          do_command=edsel.cmd,
                          stopped=(lambda command: 
                                   edsel.ed.quit or command == keyboard.C_d))

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()

edselj = piety.Job(handler=console.handler,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   restart=console.restart,
                   cleanup=edsel_cleanup)

# assign callbacks
console.job = edselj

task = piety.Task(name='edsel', handler=edselj.handler, input=sys.stdin, 
                  enabled=piety.true)

def main():
    'Run edsel under the piety scheduler'
    edselj() # start edsel, edselc(c=15) shows more cmd lines
    piety.run() # exit from edsel calls piety.stop()

if __name__ == '__main__':
    main()
