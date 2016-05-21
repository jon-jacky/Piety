"""
piety_edsel.py  - Run an edsel display editor session under Piety.
         Based on edsel_task but less code, run Job as task without Session.

Call this piety because it provides editor + python repl
"""

import edsel, command, key, sys, piety

edselc = command.Command(prompt='', reader=key.Key(), handler=edsel.cmd)

def edsel_cleanup():
    edsel.restore_display()
    piety.stop()

edselj = piety.Job(session=None, application=edselc, startup=edsel.init_session,
                   stopped=(lambda: ed.quit or edselc.command == keyboard.C_d),
                   cleanup=edsel_cleanup)

edselt = piety.Task(name='edsel', handler=edselj.reader(), input=sys.stdin, 
                    enabled=piety.true)

def main():
    'Run edsel under the piety scheduler'
    edselj() # start edsel
    piety.run() # exit from edsel calls piety.stop()

if __name__ == '__main__':
    main()
