"""
eden - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import re
import util, terminal
import keyboard, display, console, check, edsel, frame, wyshka, samysh
from updates import Op

ed = edsel.edo.ed    # use ed and frame APIs without prefix
frame = edsel.frame

next_text = re.compile(r'\s\S') # White space char then non-white space char

class Console(console.Console):
    'Console subclass that adds methods and keymaps for screen editing'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keymap = self.init_eden_keymaps()
        self.clear_line = True # used by restart method
        self.collecting_command = False # used by execute, accept methods

    # The following methods override methods in console.Console

    def restart(self):
        'Prepare to collect a command string in self.line'
        if self.clear_line: # default case, usually True
            super().restart() # clear self.line=''; show prompt; set_char_mode
        else:
            # display_mode sets clear_line = False - but does not call restart
            self.clear_line = True # restore default,leave self.line,no prompt
            terminal.set_char_mode()

    # The following  methods and keymaps all have new names, so they are added
    #  to the ones in the Console base class, they do not replace any.

    def display_mode(self, line):
        'Enter display editing mode.'
        # Based on ed.py do_command 'c' case
        ed.command_mode = False
        frame.update(Op.display)
        ed.prompt = ed.input_prompt
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        eden.line = line # not including final \n at eol
        eden.point = 0 # 0-based
        eden.start_col = 1 # 1-based
        eden.clear_line = False
        # following lines based on frame Op.input and Op.command
        win = frame.win
        win.clear_marker(win.buf.dot)
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot,1)
        
    def command_mode(self):
        'Replace current line in buffer and resume command mode.'
        # Based on ed.py append and '.' handling, Console accept_line method.
        self.restore() # advance line and put terminal in line mode
        ed.buf.replace(ed.buf.dot, self.line + '\n')
        ed.command_mode = True
        frame.update(Op.command)
        ed.prompt = ed.command_prompt
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        win = frame.win
        win.set_marker(win.buf.dot)
        frame.put_command_cursor()
        super().restart() # not self.restart.  print prompt and enter char mode

    def refresh(self):
        'Refresh entire display including whole frame and scrolling command region.'
        ed.buf.replace(ed.buf.dot, self.line + '\n') # so refresh renders it
        frame.update(Op.refresh, column=(self.start_col + self.point))

    def open_line(self):
        """
        Split line at point, replace line in buffer at dot
        with its prefix, append suffix after line at dot.
        """
        prefix = self.line[:self.point]
        suffix = self.line[self.point:].rstrip()
        ed.buf.replace(ed.buf.dot, prefix + '\n')
        display.kill_line() # from cursor to end of line
        ed.buf.a(ed.buf.dot, suffix + '\n') # calls update(Op.insert ...)
        self.line = suffix
        self.point = 0
        self.start_col = 1
        frame.put_display_cursor()
        
        # buf.a() update moved cursor so we have to put it back.FIXME?Redundant?
        win = frame.win
        wdot = win.wline(win.buf.dot)
        display.put_cursor(wdot,1)

    def del_or_join_prev(self):
        """
        If point is not at start of line, delete preceding character
        Otherwise join to previous line.  At start of first line do nothing.
        """
        if self.point > 0:
            self.backward_delete_char()
        elif ed.buf.dot > 1:
            new_point = len(ed.buf.lines[ed.buf.dot-1])-1 # don't count \n
            ed.buf.replace(ed.buf.dot, self.line)
            ed.buf.j(ed.buf.dot-1, ed.buf.dot)
            self.line = ed.buf.lines[ed.buf.dot].rstrip()
            self.point = new_point
            frame.put_display_cursor(self.start_col + self.point)
        else:
            pass
            
    def join_next(self):
        'Helper - join next line to this one. At last line do nothing.'
        if ed.buf.dot < ed.buf.nlines():
            ed.buf.replace(ed.buf.dot, self.line)
            ed.buf.j(ed.buf.dot, ed.buf.dot+1)
            self.line = ed.buf.lines[ed.buf.dot].rstrip()
            frame.put_display_cursor(self.start_col + self.point)
        else:
            pass
            
    def del_or_join_next(self):
        """
        If point is not at end of line, delete character under cursor.
        Otherwise join next line to this one.  At end of last line do nothing.
        """
        if self.point < len(self.line):
            self.delete_char()
        else:
            self.join_next()

    def goto_line(self, iline, jcol):
        if check.iline_ok(ed.buf, iline):
            ed.buf.replace(ed.buf.dot, self.line + '\n')
            ed.buf.l(iline)
            line = ed.buf.lines[ed.buf.dot].rstrip()  # FIXME? [iline] - ?
            self.line = line
            self.point = min(jcol, len(line))
            frame.put_display_cursor(self.start_col + self.point)
        # FIXME? else: ... bad line address ...

    def prev_line(self):
        """
        Move cursor from current line in window to same
        column in line above, or end of line - whichever comes first.
        When cursor would leave top, redraw window with current line in middle
        Replace current line in buffer and copy preceding buffer line into line
        """
        self.goto_line(ed.buf.dot-1, self.point)

    def next_line(self):
        'Like prev_line, but line below/bottom.'
        self.goto_line(ed.buf.dot+1, self.point)

    def page_down(self):
        'Move cursor forward several/many lines.'
        dest = min(ed.buf.dot + frame.win.nlines - 1, ed.buf.nlines())
        self.goto_line(dest, self.point)

    def page_up(self):
        'Move cursor backward several/many lines.'
        dest = max(ed.buf.dot - frame.win.nlines + 1, 1)
        self.goto_line(dest, self.point)

    def search(self):
        'Search forward for previous search string.'
        self.goto_line(ed.F(''), self.point)

    def rsearch(self):
        'Search backward for previous search string.'
        self.goto_line(ed.R(''), self.point)

    def set_mark(self):
        'Define region from mark (inclusive) to dot (exclusive) that is deleted by cut'
        ed.buf.mark['@'] = ed.buf.dot
        frame.put_command_cursor()
        util.putstr('Mark set\n')
        frame.put_display_cursor() # Or display.put_cursor(wdot,1) ?

    def exchange(self):
        'Exchange point and mark (to make mark visible by putting cursor there).'
        if '@' in ed.buf.mark:
            saved_dot = ed.buf.dot
            self.goto_line(ed.buf.mark['@'], 1) # updates ed.buf.dot
            ed.buf.mark['@'] = saved_dot

    def cut(self):
        """
        Delete from mark to line before dot, store deleted text in paste buffer.
        If no mark, do nothing.
        If mark follows dot, delete from dot to one before mark, reassign dot/
        """
        if '@' in ed.buf.mark:
            start = ed.buf.mark['@']
            end = ed.buf.dot
            if start > end:
                start, end = end, start
            end -= 1 # exclude last line, dot (usually) or mark
            if check.range_ok(ed.buf, start, end):
                ed.buf.d(start, end)
                frame.put_display_cursor()
                self.inline_yank = False
        # FIXME? else: "The mark is not set now, so there is no region"

    def kill(self):
        super().kill()
        ed.buf.modified = True
        self.inline_yank = True

    def discard(self):
        super().discard()
        ed.buf.modified = True
        self.inline_yank = True

    def yank(self):
        if ed.command_mode or self.inline_yank == True:
            # Insert string from self.yank_buffer at point.
            super().yank()
        else:
            # Insert lines from Buffer class cut_buffer before dot.
            ed.buf.x(ed.buf.dot-1) # ed x appends, eden ^Y inserts
            ed.buf.dot += 1  # x puts dot at last line in region, ^Y at first after
            frame.put_display_cursor()

    def prev_indent(self, prev_line):
        """
        Return indentation level: index of first non-whitespace character
        in nearest non-empty preceding line, working back from prev_line.
        Also return that line number, 0 means no preceding non-empty lines
        """
        indent = self.n_tab_spaces # default
        match = None
        while not match and prev_line > 0:
            match = next_text.search(ed.buf.lines[prev_line], 0)
            if match:
                indent = match.start()+1
            else:
                prev_line -= 1
        return indent, prev_line

    def tab(self):
        'For first tab stop, try to match indentation of preceding line'
        if self.point == 0:
            indent, _ = self.prev_indent(ed.buf.dot - 1)
        else:
            indent = self.n_tab_spaces
        self.tab_n(indent)
        ed.buf.modified = True

    def other_window(self):
        'Move cursor to other window, next in sequence.'
        ed.buf.replace(ed.buf.dot, self.line + '\n') # from goto_line
        edsel.do_window_command('') # reassign win, ed.buf, call update(Op.next)
        self.line = ed.buf.lines[ed.buf.dot].rstrip() # from several methods
        # From display_mode
        self.point = 0
        self.start_col = 1
        wdot = frame.win.wline(frame.win.buf.dot)
        display.put_cursor(wdot, 1)

    def status(self):
        '^T handler, override base class, for now print items used by del_or_join_next'
        util.putstr('%s.%s point %s len %s dot %s nlines %s' %
                    (self.line[:self.point], self.line[self.point:],
                     self.point, len(self.line), ed.buf.dot, ed.buf.nlines()))

    def execute(self):
        """
        Execute command: cursor moves to command line, prompt appears,
        then type any ed/edo/edsel command, then type RET to return to display
        mode (without having to type C then RET).  The command can simply be a
        line address: a line number, $ (end), a search string in /.../ etc
        So this command acts as go-to-line or search command also.
        """
        self.collecting_command = True
        self.command_mode() # like eden ^Z command
        # Now console will collect command line
        # BUT collecting_command tells console not to call accept_command
        # but (via keymap lambda with if...) to call accept_eden_command
        # instead, which returns immediately to display mode.

    def accept_eden_command(self):
        'After execute() above, execute the line, then return to display mode.'
        self.collecting_command = False
        self.process_command()
        if self.stopped() and not self.quit: # if .quit, stop() already called
            self.stop()
        else:
            terminal.set_char_mode()
            self.display_mode(ed.buf.lines[ed.buf.dot].rstrip())

    def cancel_eden_command(self):
        'After execute() above, just discard the line, then return to display mode.'
        self.collecting_command = False
        # self.process_command()
        # next two lines from discard method
        self.move_beginning()
        display.kill_line()
        terminal.set_char_mode()
        self.display_mode(ed.buf.lines[ed.buf.dot].rstrip()) # strip \n at eol

    def crash(self):
        'For now, just crash' # FIXME - not used, ^K is now console kill line
        return 1/0  # raise exception on demand (crash), for testing

    def init_eden_keymaps(self):
        self.display_keys = {
            keyboard.C_c: self.page_up,
            keyboard.C_d: self.del_or_join_next,
            # keyboard.C_k: self.crash, # FIXME? Now ^K is kill
            keyboard.C_k: self.kill,
            keyboard.C_l: self.refresh,
            keyboard.C_n: self.next_line,
            keyboard.C_o: self.other_window,
            keyboard.C_p: self.prev_line,
            keyboard.C_q: self.exchange,
            keyboard.C_r: self.rsearch,
            keyboard.C_s: self.search,
            keyboard.C_u: self.discard,
            keyboard.C_v: self.page_down,
            keyboard.C_w: self.cut,
            keyboard.C_x: self.execute,
            keyboard.C_y: self.yank,
            keyboard.C_z: self.command_mode,
            # ^space also works as ^@ on many terminals
            keyboard.C_at: self.set_mark,
            keyboard.cr: self.open_line,
            keyboard.up: self.prev_line,
            keyboard.down: self.next_line,
            keyboard.bs: self.del_or_join_prev,
            keyboard.delete: self.del_or_join_prev,
            }
        self.display_keymap = self.input_keymap.copy()# FIXME? Why?
        self.display_keymap.update(self.display_keys) # override some keys
        self.eden_command_keys = {
            keyboard.C_g: self.cancel_eden_command,
            keyboard.cr: self.accept_eden_command,
            }
        # Be sure to preserve console command_keymap, we stil use it
        self.eden_command_keymap = self.command_keymap.copy()
        self.eden_command_keymap.update(self.eden_command_keys)
        return (lambda: self.eden_display_keymap)

def base_do_command(line):
    'Process one command line without blocking.'
    line = line.lstrip()

    # Begin full-screen display editing
    if line == 'C':
        eden.display_mode(ed.buf.lines[ed.buf.dot].rstrip()) # strip \n at eol
    else:
        edsel.base_do_command(line)

# We redefined do_command so we have to redefine process_line
def base_process_line(line):
    'process one line without blocking, according to mode'
    if ed.command_mode:
        base_do_command(line)
    else:
        ed.add_line(line)

# Add embedded python interpreter.
_process_line = wyshka.shell(process_line=base_process_line,
                             command_mode=(lambda: ed.command_mode),
                             command_prompt=(lambda: ed.prompt))

# Add command to run script from buffer with optional echo and delay.
process_line = samysh.add_command(edsel.edo.X_command(_process_line),
                                  _process_line)

eden = Console(prompt=(lambda: wyshka.prompt),
               process_line=process_line,
               stopped=(lambda command: ed.quit),
               startup=edsel.startup, cleanup=edsel.cleanup)

eden.keymap = (lambda: (eden.eden_command_keymap
                        if eden.collecting_command
                        else eden.display_keymap
                        if frame.mode == frame.Mode.display
                        else eden.input_keymap
                        if frame.mode == frame.Mode.input
                        else eden.command_keymap)) # frame.Mode.command

def main(*filename, **options):
    eden.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
