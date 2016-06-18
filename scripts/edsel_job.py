"""
edsel_job.py - Edsel display editor with Job class, but no Command.
  Use Python input function to get whole command line at once in
  blocking event loop.  Contrast to edsel_command.py
"""

import edsel, keyboard, piety

# Here we use Command args rather than calling edsel functions in main()
edselj = piety.Job(do_command=edsel.cmd,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   stopped=(lambda command: 
                            edsel.ed.quit or command == keyboard.C_d),
                   cleanup=edsel.restore_display)

def main():
    edselj() # run startup
    while not edselj.stopped():
        edselj.command = input(': ') # with prompt 
        edselj.do_command() 

if __name__ == '__main__':
    main()
