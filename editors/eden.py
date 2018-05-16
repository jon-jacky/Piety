"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import util, terminal
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
        eden.point = 0 # 0-based
        eden.start_col = 1 # 1-based
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
        if self.clear_command: # default case, usually True
            self.command = ''
            self.point = 0 # index into self.command
            self.start_col = len(self.prompt())+1 # 1-based indexing, not 0-
            util.putstr(self.prompt() + self.command) # command might be empty
            self.move_to_point() # might not be end of line
        else:
            self.clear_command = True # restore default
        terminal.set_char_mode()

    # The following  methods and keymaps all have new names, so they are added 
    #  to the ones in the Console base class, they do not replace any.

    # This method is based on expanding code inline here 
    # from ed.py append and '.' handling, and Console accept_line method.
    def command_mode(self):
        '^Z: Replace current line in buffer and resume command mode'
        self.restore() # advance line and put terminal in line mode 
        ed.buf.replace(ed.buf.dot, self.command + '\n')
        ed.command_mode = True
        ed.prompt = ed.ps1
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        edsel.frame.put_command_cursor()
        self.restart()      # print prompt and put term in character mode

    def open_line(self):
        """
        RET: Split line at point, replace line in buffer at dot 
        with its prefix, append suffix after line at dot.
        """
        prefix = self.command[:self.point]
        suffix = self.command[self.point:].rstrip()
        ed.buf.replace(ed.buf.dot, prefix + '\n')
        display.kill_line() # from cursor to end of line
        terminal.set_line_mode() # needed by update called by buf.a() below
        ed.buf.a(ed.buf.dot, suffix + '\n') # calls update(Op.insert ...)
        self.command = suffix
        self.point = 0
        self.start_col = 1
        terminal.set_char_mode()
        # buf.a() update moved cursor so we have to put it back
        win = edsel.frame.win
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot,1)

    def delete_or_join(self):
        """
        DEL: If point is not at start of line, delete preceding character.
        Otherwise join to previous line.
        """
        if self.point > 0:
            self.backward_delete_char()
        else:
            ed.buf.join()

    def prev_line(self):
        """
        ^P, up arrow: Move cursor from current line in window to line above.
        When cursor would leave top, redraw window with current line in middle
        Replace current line in buffer and copy preceding buffer line into line
        """
        pass

    def next_line(self):
        """
        ^N, down arrow: Move cursor from current line in window to line below.
        When cursor would leave bottom, redraw window w/current line in middle
        Replace current line in buffer and copy following buffer line into line
        """
        pass

    def init_eden_keymaps(self):
        self.display_keys = {
            keyboard.C_z: self.command_mode,
            keyboard.cr: self.open_line,
            keyboard.C_p: self.prev_line,
            keyboard.C_n: self.next_line
            keyboard.up: self.prev_line,
            keyboard.down: self.next_line,
            keyboard.bs: self.delete_or_join,
            keyboard.delete: self.delete_or_join
            }
        self.display_keymap = self.input_keymap.copy()
        self.display_keymap.update(self.display_keys) # override some keys
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
