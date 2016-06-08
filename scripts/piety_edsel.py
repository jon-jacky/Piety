"""
piety_edsel - Run an edsel display editor session under Piety.
         Based on edsel_task but less code, run Job as task without Session.
"""

import sys, piety, command, keyboard, key, edsel

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()

edselc = command.Command(prompt='', handler=key.Key(), do_command=edsel.cmd,
                         stopped=(lambda command: 
                                  edsel.ed.quit or command == keyboard.C_d),
                         cleanup=edsel_cleanup)

edselj = piety.Job(application=edselc, startup=edsel.init_session)

edselt = piety.Task(name='edsel', handler=edselj.handler, input=sys.stdin, 
                    enabled=piety.true)

def main():
    'Run edsel under the piety scheduler'
    edselj() # start edsel, edselj(c=15) shows more cmd lines
    piety.run() # exit from edsel calls piety.stop()

if __name__ == '__main__':
    main()
