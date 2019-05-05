"""
etty.py - Run ed line editor session, but use console module instead
 of Python input to collect and edit command line and inserted text.
 Add new methods and keymaps to provide retro printing-terminal-style
 editing and history.
To use the ed API from the Python prompt, use prefix as in etty.ed.p()
"""

import util, terminal, keyboard, ed, console

class Console(console.Console):
    'Console subclass that adds methods and keymaps for printing terminals'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keymap = self.init_tty_keymaps()

    # These methods and keymaps all have new names, so they are added 
    #  to the ones in the base class, they do not replace any.
    def previous_history_tty(self):
        self.retrieve_previous_history()
        self.redraw_with_prefix('^P\r\n')

    def next_history_tty(self):
        self.retrieve_next_history()
        self.redraw_with_prefix('^N\r\n')
    
    def append_char(self, keycode):
        self.line += keycode
        self.point += 1
        util.putstr(keycode)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.line[-1]
            self.line = self.line[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def discard_tty(self): # name like gnu readline unix-line-discard
        'discard entire line including prompt on printing terminal'
        self.line = ''
        util.putstr('^U\r\n' + self.prompt())  # prompt on new line

    def redraw_with_prefix(self, prefix):
        'redraw entire line with prefix and prompt on printing terminal'
        util.putstr(prefix + self.prompt())
        self.redraw()

    def redraw_tty(self):
        'redraw entire line including prompt on printing terminal'
        self.redraw_with_prefix('^L\r\n')

    def init_tty_keymaps(self):
        # This keymap works on a printing terminal.
        self.tty_input_keymap = {
            console.printable: self.append_char, 
            keyboard.cr: self.accept_line,
            keyboard.C_c: self.interrupt,
            # Rudimentary in-line editing, just delete last char in line
            keyboard.bs: self.backward_delete_last_char,
            keyboard.delete: self.backward_delete_last_char,
            # Show the line, useful after several edits
            keyboard.C_l: self.redraw_tty,
            keyboard.C_u: self.discard_tty,
        }

        # This keymap works on a printing terminal with no arrow keys.
        self.tty_command_keys = {
            # Any keycode that maps to accept_command is a command terminator.
            keyboard.cr: self.accept_command, # add to history, possibly exit
            keyboard.C_n: self.next_history_tty,
            keyboard.C_p: self.previous_history_tty,
            }

        # This combined keymap works on a printing terminal.
        self.tty_command_keymap = self.tty_input_keymap.copy()
        self.tty_command_keymap.update(self.tty_command_keys)
        self.tty_command_keymap.update(self.job_control_keys)

        return (lambda: self.tty_command_keymap) # default keymap

etty = Console(prompt=(lambda: ed.prompt),
               reader=terminal.getchar,
               process_line=ed.process_line,
               stopped=(lambda command: ed.quit),
               startup=ed.startup, cleanup=ed.q)

# use non-default tty keymaps
etty.keymap = (lambda: (etty.tty_command_keymap
                        if ed.command_mode
                        else etty.tty_input_keymap))

def main(*filename, **options):
    etty.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
