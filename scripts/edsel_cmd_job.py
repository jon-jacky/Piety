"""
edsel_cmd_job.py - Edsel display editor with Command and Job classes,
 in blocking event loop.  Show how to use callbacks to connect Command
 to Job.  Contrast to edsel_command.py and edsel_job.py.
"""

import edsel, command, key, keyboard, piety

console = command.Command(handler=key.Key())

edselj = piety.Job(handler=console.handler, command=console,
                   do_command=edsel.cmd,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   restart=console.restart,
                   stopped=(lambda command: 
                            edsel.ed.quit or command == keyboard.C_d),
                   cleanup=edsel.restore_display)

# assign callbacks
console.do_command = edselj.do_command
console.stopped = edselj.stopped

def main():
    edselj() # run startup
    while not edselj.stopped():
        edselj.handler()

if __name__ == '__main__':
    main()
