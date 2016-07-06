"""
edsel_cmd_job.py - Edsel display editor with Command and Job classes,
 in blocking event loop.  Show how to use callbacks to connect Command
 to Job.  Contrast to edsel_command.py and edsel_job.py.
"""

import edsel, command, key, keyboard, piety

console = command.Command(prompt=': ', handler=key.Key(),
                          do_command=edsel.cmd,
                          stopped=(lambda command: 
                                   edsel.ed.quit or command == keyboard.C_d))

edselj = piety.Job(handler=console.handler,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   restart=console.restart,
                   cleanup=edsel.restore_display)

# assign callbacks
console.job = edselj

def main():
    edselj() # run startup
    while not console.stopped():
        edselj.handler()

if __name__ == '__main__':
    main()
