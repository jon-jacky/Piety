"""
etty.py - Run ed line editor session, but use console module
 instead of Python input to collect and edit command line and inserted text.
 Use keymaps to provide retro printing-terminal-style editing and history.
"""

import ed, console, terminal

tty = console.Console(prompt=(lambda: ed.prompt), 
                      reader=terminal.getchar,
                      do_command=ed.do_command,
                      stopped=(lambda command: ed.quit),
                      startup=ed.startup, cleanup=ed.q)

# use non-default tty keymaps
tty.keymap=(lambda: (tty.command_tty_keymap 
                     if ed.command_mode 
                     else tty.insert_tty_keymap))

def etty(*filename, **options):
    tty.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    etty(*filename, **options)
