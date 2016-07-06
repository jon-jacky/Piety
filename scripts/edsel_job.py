"""
edsel_job.py - Edsel display editor with Job class, but no Command.
  Use Python input function to get whole command line at once in
  blocking event loop.  Contrast to edsel_command.py
"""

import edsel, keyboard, piety, util

command = str()  # global so we can pass it to edsel_stopped

def edsel_stopped(command):
    return edsel.ed.quit or command == keyboard.C_d # But ^D crashes input() 

def edsel_restart():
    util.putstr(': ') # print prompt w/o newline

def edsel_handler():
     global command
     command = input()
     # the following lines are based on Command accept_line 
     if command != keyboard.C_d: # useless here - ^D already crashes input()
         edsel.cmd(command)
     if edselj.replaced:
         return
     if edsel_stopped(command):
         edselj.do_stop()
     else:
         edsel_restart()
     
# Here we use Command args rather than calling edsel functions in main()
edselj = piety.Job(handler=edsel_handler,
                   startup=(lambda: edsel.init_session(c=12)), # 12 cmd lines
                   restart=edsel_restart, cleanup=edsel.restore_display)

def main():
    edselj() # run startup, restart
    while not edsel_stopped(command):
        edselj.handler()

if __name__ == '__main__':
    main()
