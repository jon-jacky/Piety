"""
edsel_cmd_job.py - Edsel display editor with Command and Job classes,
  created and connected using console_job function.  Contrast to edsel_cmd_job.
"""

import edsel, key, keyboard
from console_job import console_job

edselj, c = console_job(prompt=': ', reader=key.Key(),
                        do_command=edsel.cmd,
                        startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                        stopped=(lambda command: 
                                 edsel.ed.quit or command == keyboard.C_d),
                        cleanup=edsel.restore_display)

def main():
    edselj() # run startup
    while not c.stopped():
        edselj.handler()

if __name__ == '__main__':
    main()
