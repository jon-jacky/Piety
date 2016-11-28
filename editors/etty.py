"""
etty.py - Run ed line editor session, but use console module
 instead of Python input to collect and edit command line and inserted text.
 Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, console as con, terminal, inputline

console = con.Console(prompt=':', reader=terminal.getchar,
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      # specify two non-default tty_keymap 
                      command_keymap=con.command_tty_keymap,
                      edit_keymap=inputline.tty_keymap,
                      mode=(lambda: ed.command_mode))

def main():
    ed.quit = False # previous quit might have set it True
    console.run()

if __name__ == '__main__':
    main()
