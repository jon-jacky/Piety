"""
etty.py - Run ed line editor session, but use console/command.py
 instead of Python input() to collect and edit command line and inserted text.
 Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, console as con, terminal

console = con.Console(prompt=':', reader=terminal.getchar,
                      command=con.LineInput(),
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      keymap=con.printing_keymap,
                      mode=(lambda: ed.command_mode), # True or False
                      behavior={ False: ('', con.printing_insertmode_keymap) })

def main():
    ed.quit = False # previous quit might have set it True
    console.run()

if __name__ == '__main__':
    main()
