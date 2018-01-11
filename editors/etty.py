"""
etty.py - Run ed line editor session, but use console module
 instead of Python input to collect and edit command line and inserted text.
 Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, console as con, terminal

console = con.Console(prompt=(lambda: ed.prompt), 
                      reader=terminal.getchar,
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      # specify non-default tty_keymap 
                      keymap=(lambda: (con.command_tty_keymap 
                                               if ed.command_mode 
                                               else con.insert_tty_keymap)))

def main():
    ed.startup()
    console.run()

if __name__ == '__main__':
    main()
