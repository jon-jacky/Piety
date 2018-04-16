"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import keyboard, console, edsel, wyshka, samysh

ed = edsel.edo.ed  # so we can use it without prefix

def base_do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()
    if ed.command_mode and line == 'C':
        # ed.command_mode = False # enter display editing mode 
        pass # FIXME - more to come
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
    def command_mode(self):
        'Resume command mode'
        #ed.command_mode = True # FIXME - Console shouldn't depend on ed
        pass # FIXME - more to come

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
