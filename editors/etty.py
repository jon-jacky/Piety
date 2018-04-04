"""
etty.py - Run ed line editor session, but use console module instead
 of Python input to collect and edit command line and inserted text.
 Add new methods and keymaps to provide retro printing-terminal-style
 editing and history.
"""

import util, terminal, keyboard, ed, console

class Console(console.Console):
    'Console subclass that adds methods and keymaps for printing terminals'
    def __init_(self, **kwargs):
        super.__init__(**kwargs)
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
        self.command += keycode
        self.point += 1
        util.putstr(keycode)

    def backward_delete_last_char(self):
        if self.point > 0:
            ch = self.command[-1]
            self.command = self.command[:-1]
            self.point -= 1
            # util.putstr('^H') # omit, it is more helpful to echo
            util.putstr('\\%s' % ch) # echo \c where c is deleted char

    def discard_tty(self): # name like gnu readline unix-line-discard
        'discard entire line including prompt on printing terminal'
        self.command = ''
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
        self.lineedit_tty_keymap = {
            # append_char requires special-case handling
            #  because it takes an additional argument: the key.
            printable: self.append_char,
            # Rudimentary in-line editing, just delete last char in line
            keyboard.bs: self.backward_delete_last_char,
            keyboard.delete: self.backward_delete_last_char,
            # Show the line, useful after several edits
            keyboard.C_l: self.redraw_tty,
            keyboard.C_u: self.discard_tty,
        }

        self.insert_tty_keymap = self.stub_insert_keymap.copy()
        self.insert_tty_keymap.update(self.lineedit_tty_keymap)

        # This keymap works on a printing terminal with no arrow keys.
        self.command_tty_keys = {
            # Any keycode that maps to accept_command is a command terminator.
            keyboard.cr: self.accept_command, # add to history, possibly exit
            keyboard.C_n: self.next_history_tty, 
            keyboard.C_p: self.previous_history_tty,
            }

        # This combined keymap works on a printing terminal.
        self.command_tty_keymap = self.insert_tty_keymap.copy()
        self.command_tty_keymap.update(self.command_tty_keys)
        self.command_tty_keymap.update(self.job_control_keys)

        return (lambda: self.command_tty_keymap) # default keymap

tty = Console(prompt=(lambda: ed.prompt), 
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
