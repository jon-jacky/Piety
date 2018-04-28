"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import keyboard, console, edsel, view, wyshka, samysh
from updates import Op

ed = edsel.edo.ed  # so we can use it without prefix

def base_do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()
    if ed.command_mode and line == 'C':
        ed.do_command('c') # FIXME stub, for now behave like classic ed 'c'
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

    # These methods and keymaps all have new names, so they are added 
    #  to the ones in the base class, they do not replace any.

    # This method is based on expanding code inline here 
    # from ed.py append and '.' handling, and Console accept_line method.
    def command_mode(self):
        'Add current line to buffer and resume command mode'
        self.restore() # advance line and put terminal in line mode 
        ed.buf.a(ed.buf.dot, self.command + '\n') #append after dot,advance dot
        ed.command_mode = True
        ed.prompt = ed.ps1
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        view.update(Op.command) # return from input mode to cmd mode
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
