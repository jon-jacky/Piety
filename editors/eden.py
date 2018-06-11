"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import util, terminal
import keyboard, display, frame, console, check, edsel, wyshka, samysh
from updates import Op

ed = edsel.edo.ed  # so we can use it without prefix

def base_do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()

    # Begin full-screen display editing
    if ed.command_mode and line == 'C':
        # following lines based on ed.py do_command 'c' case
        ed.command_mode = False
        # but not frame command_mode= False, that means ed input mode for a i c
        frame.display_mode = True # probably should use update(Op...) for this
        ed.prompt = ed.ps2
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        eden.command = ed.buf.lines[ed.buf.dot].rstrip() # strip \n at eol
        eden.point = 0 # 0-based
        eden.start_col = 1 # 1-based
        eden.clear_command = False
        # following lines based on frame Op.input and Op.command
        win = edsel.frame.win
        win.clear_marker(win.buf.dot)
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
        # but not frame command_mode = True, it was never False
        frame.display_mode = False # probably should use update(Op...) for this
        ed.prompt = ed.ps1
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        win = edsel.frame.win
        win.set_marker(win.buf.dot)
        edsel.frame.put_command_cursor()
        self.restart()      # print prompt and put term in character mode

    def refresh(self):
        ed.buf.replace(ed.buf.dot, self.command + '\n') 
        terminal.set_line_mode() # needed by update called by buf.l() below
        frame.update(Op.refresh)
        terminal.set_char_mode()

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

    def del_or_join_up(self):
        """
        DEL: If point is not at start of line, delete preceding character.
        Otherwise join to previous line.
        """
        if self.point > 0:
            self.backward_delete_char()
        else:
            new_point = len(ed.buf.lines[ed.buf.dot-1])
            terminal.set_line_mode() # needed by update called by buf.j() below
            ed.buf.j(ed.buf.dot-1, ed.buf.dot)
            self.command = ed.buf.lines[ed.buf.dot].rstrip()
            self.point = new_point # FIXME what about marker?
            terminal.set_char_mode()
            # buf.j() update moved cursor to bottom so we have to put it back
            win = edsel.frame.win
            wdot = win.wline(win.buf.dot)
            display.put_cursor(wdot, self.start_col + self.point)

    def del_or_join_down(self):
        """
        ^D: If point is not at end of line, delete character under cursor.
        Otherwise join next line to this one.
        """
        pass

    def goto_line(self, iline, jcol):
        if check.iline_ok(ed.buf, iline):
            ed.buf.replace(ed.buf.dot, self.command + '\n')
            terminal.set_line_mode() # needed by update called by buf.l() below
            ed.buf.l(iline)
            line = ed.buf.lines[ed.buf.dot].rstrip()  # [iline] - ?
            self.command = line
            self.point = min(jcol, len(line)+1)
            terminal.set_char_mode()
            # buf.l() update moved cursor to bottom so we have to put it back
            # replace below with new win.put_cursor_at_dot(...) method ?
            win = edsel.frame.win
            wdot = win.wline(ed.buf.dot)
            display.put_cursor(wdot, self.start_col + self.point)

    def prev_line(self):
        """
        ^P, up arrow: Move cursor from current line in window to same
        column in line above, or end of line - whichever comes first.
        When cursor would leave top, redraw window with current line in middle
        Replace current line in buffer and copy preceding buffer line into line
        """
        self.goto_line(ed.buf.dot-1, self.point)

    def next_line(self):
        '^N, down arrow: Like prev_line, but line below/bottom'
        self.goto_line(ed.buf.dot+1, self.point)

    def page_down(self):
        '^v, page down.'
        dest = min(ed.buf.dot + ed.buf.npage, ed.buf.nlines())
        self.goto_line(dest, self.point)

    def page_up(self):
        '^x (for now, change to M_v later) - page up'
        dest = max(ed.buf.dot - ed.buf.npage, 1)
        self.goto_line(dest, self.point)
        
    def set_mark(self):
        '^space, set mark'
        pass

    def exchange(self):
        '^x, exchange point and mark'
        pass

    def cut(self):
        '^w, delete from mark to point, store deleted text in paste buffer'
        pass

    def paste(self):
        '^y, insert text from paste buffer'
        pass

    def init_eden_keymaps(self):
        self.display_keys = {
            keyboard.C_z: self.command_mode,
            keyboard.C_l: self.refresh,
            keyboard.cr: self.open_line,
            keyboard.C_p: self.prev_line,
            keyboard.C_n: self.next_line,
            keyboard.up: self.prev_line,
            keyboard.down: self.next_line,
            keyboard.bs: self.del_or_join_up,
            keyboard.delete: self.del_or_join_up,
            keyboard.C_d: self.del_or_join_down,
            keyboard.C_v: self.page_down,
            keyboard.C_x: self.page_up, #C_x is placeholder, use something else
            keyboard.C_space: self.set_mark,
            keyboard.C_w: self.cut,
            keyboard.C_y: self.paste,
            # keyboard.C_x: self.page_up, #C_x is placeholder, use something else
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
