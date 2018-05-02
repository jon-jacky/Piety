"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import util, terminal # used only in restart
import keyboard, display, console, view, edsel, wyshka, samysh
from updates import Op

ed = edsel.edo.ed  # so we can use it without prefix

def base_do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()

    # Begin full-screen display editing
    if ed.command_mode and line == 'C':
        # following lines based on ed.py do_command 'c' case
        ed.command_mode = False
        ed.prompt = ed.ps2
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        eden.command = ed.buf.lines[ed.buf.dot].rstrip() # strip \n at eol
        eden.clear_command = False
        # following lines based on frame Op.input
        win = edsel.frame.win
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot,1)

    else:
        edsel.base_do_command(line)

# wyshka adds embedded python interpreter to do_command
_do_command = wyshka.shell(do_command=base_do_command,
                           command_mode=(lambda: ed.command_mode),
                           command_prompt=(lambda: ed.prompt))

# do_command: add edo.x_command that executes script using samysh
do_command = samysh.add_command(edsel.edo.x_command(_do_command), _do_command)

class Console(console.Console):
    'Console subclass that adds methods and keymaps for screen editing'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keymap = self.init_eden_keymaps()
        self.clear_command = True # used by restart method

    # The following methods override methods in console.Console

    def restart(self):
        'Prepare to collect a command string in self.command'
        if self.clear_command: # default, but not always
            self.command = ''
            self.point = 0 # index into self.command
        else:
            self.clear_command = True # restore default
        self.start_col = len(self.prompt())+1 # 1-based indexing, not 0-based
        util.putstr(self.prompt() + self.command) # command might be empty
        self.move_to_point() # might not be end of line
        terminal.set_char_mode()

    # The following  methods and keymaps all have new names, so they are added 
    #  to the ones in the base class, they do not replace any.

    # This method is based on expanding code inline here 
    # from ed.py append and '.' handling, and Console accept_line method.
    def command_mode(self):
        'Add current line to buffer and resume command mode'
        self.restore() # advance line and put terminal in line mode 
        ed.buf.replace(ed.buf.dot, self.command + '\n')
        ed.command_mode = True
        ed.prompt = ed.ps1
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        edsel.frame.put_command_cursor()
        self.restart()      # print prompt and put term in character mode

    def init_eden_keymaps(self):
        self.display_keys = {
            keyboard.C_z: self.command_mode
            }
        self.display_keymap = self.input_keymap.copy()
        self.display_keymap.update(self.display_keys)
        return (lambda: self.command_keymap)

eden = Console(prompt=(lambda: wyshka.prompt), 
               do_command=do_command,
               stopped=(lambda command: ed.quit),
               startup=edsel.startup, cleanup=edsel.cleanup)

eden.keymap = (lambda: (eden.command_keymap 
                        if ed.command_mode
                        else eden.display_keymap))

def main(*filename, **options):
    eden.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
