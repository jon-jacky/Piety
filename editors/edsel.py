"""
 - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import re
from contextlib import redirect_stdout

import util, terminal
import key, display, console, check, edda, pysh, wyshka, samysh

edo = edda.edo # use edo, ed, text, frame etc. APIs without prefix
ed = edo.ed    
text = ed.text
frame = edda.frame
bimport, breload, sh = edo.bimport, edo.breload, edo.sh

next_text = re.compile(r'\s\S') # White space char then non-white space char

class Console(console.Console):
    'Console subclass that adds methods and keymaps for screen editing'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keymap = self.init_edsel_keymaps()
        self.collecting_command = False # used by execute, accept_edsel methods

    # This method overrides the one in the Console base class.
    # Special case handling for C command that changes to display mode.
    # Handle here instead of in do_command.
    def accept_command(self):
        if self.line == 'C': # C command, change to display mode
            print() # advance line in command region
            self.set_display_mode(text.buf.lines[text.buf.dot].rstrip('\n'))
        else:
            super().accept_command()

    def load_line(self):
        'load self.line from line in buffer at dot'
        self.line = text.buf.lines[text.buf.dot].rstrip('\n')

    def store_line(self):
        'store self.line to line in buffer at dot'
        text.buf.replace(text.buf.dot, self.line + '\n')

    def set_display_mode(self, line):
        'Enter display editing mode.'
        # Based on ed.py do_command 'c' case
        ed.command_mode = False
        ed.prompt = ed.input_prompt
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        edsel.line = line # not including final \n at eol
        edsel.point = 0 # 0-based
        edsel.start_col = 1 # 1-based
        frame.display_mode()

    def set_command_mode(self):
        'Replace current line in buffer and resume command mode.'
        # Based on ed.py append and '.' handling, Console accept_line method.
        self.store_line()
        ed.command_mode = True
        ed.prompt = ed.command_prompt
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        frame.command_mode()
        self.restart() # print prompt and enter char mode

    def refresh(self):
        'Refresh entire display including whole frame and scrolling region.'
        if ed.command_mode:
            super().refresh() # just refresh the command line
        else:
            self.store_line()
            frame.refresh()

    def open_line(self):
        """
        Split line at point, replace line in buffer at dot
        with its prefix, append suffix after line at dot.
        """
        prefix = self.line[:self.point]
        suffix = self.line[self.point:].rstrip('\n')
        text.buf.replace(text.buf.dot, prefix + '\n') # similar to store_line
        display.kill_line() # from cursor to end of line
        # Must update self.point etc. *before* text.buf.a calls frame.insert
        self.line = suffix
        self.point = 0
        self.start_col = 1
        text.buf.a(text.buf.dot, suffix + '\n') # calls frame.insert()

    def join_prev(self):
        'Helper - join this line to previous. At first line do nothing.'
        if text.buf.dot > 1:
            new_point = len(text.buf.lines[text.buf.dot-1])-1 # don't count \n
            self.store_line()
            text.buf.j(text.buf.dot-1, text.buf.dot)
            self.load_line()
            self.point = new_point
            frame.put_display_cursor()
        else:
            pass

    def delete_backward_char(self):
        """
        If point is not at start of line, delete preceding character.
        Otherwise join to previous line.  At start of first line do nothing.
        """
        if self.point > 0:
            super().delete_backward_char()
        else: 
            self.join_prev()

    def join_next(self):
        'Helper - join next line to this one. At last line do nothing.'
        if text.buf.dot < text.buf.nlines():
            self.store_line()
            text.buf.j(text.buf.dot, text.buf.dot+1)
            self.load_line()
            frame.put_display_cursor()
        else:
            pass

    def delete_char(self):
        """
        If point is not at end of line, delete character under cursor.
        Otherwise join next line to this one.  At end of last line do nothing.
        """
        if self.point < len(self.line):
            super().delete_char()
        else:
            self.join_next()

    def goto_line(self, iline, jcol):
        if check.iline_ok(text.buf, iline):
            self.store_line()
            text.buf.l(iline)
            self.load_line()
            self.point = min(jcol, len(self.line))
            frame.put_display_cursor()
        if iline == text.buffer.no_match:
            frame.put_message('? no match')

    def prev_line(self):
        """
        Move cursor from current line in window to same
        column in line above, or end of line - whichever comes first.
        When cursor would leave top, redraw window with current line in middle
        Replace current line in buffer and copy preceding buffer line into line
        """
        self.goto_line(text.buf.dot-1, self.point)

    def next_line(self):
        'Like prev_line, but line below/bottom.'
        self.goto_line(text.buf.dot+1, self.point)

    def page_down(self):
        'Move cursor forward several/many lines.'
        dest = min(text.buf.dot + frame.win.nlines - 1, text.buf.nlines())
        self.goto_line(dest, self.point)

    def page_up(self):
        'Move cursor backward several/many lines.'
        dest = max(text.buf.dot - frame.win.nlines + 1, 1)
        self.goto_line(dest, self.point)

    def top(self):
        'Move cursor to first line (top) of buffer'
        self.goto_line(1, 1)

    def bottom(self):
        'Move cursor to last line (bottom) of buffer'
        self.goto_line(text.buf.nlines(), 1)

    def fill(self):
        'Fill paragraph'
        self.store_line() # might not have been stored yet
        text.buf.J(text.buf.para_first(), text.buf.para_last(), 
                   text.buf.fill_column)
        self.load_line() # now there is a new line at dot
        
    def search(self):
        'Search forward for previous search string.'
        self.goto_line(text.buf.F(''), self.point)

    def rsearch(self):
        'Search backward for previous search string.'
        self.goto_line(text.buf.R(''), self.point)

    def set_mark(self):
        'Define region from mark (inclusive) to dot (exclusive) that is deleted by cut'
        text.buf.mark['@'] = text.buf.dot
        frame.put_message('Mark set')

    def exchange(self):
        'Exchange point and mark (to make mark visible by putting cursor there).'
        if '@' in text.buf.mark:
            saved_dot = text.buf.dot
            self.goto_line(text.buf.mark['@'], 1) # updates text.buf.dot
            text.buf.mark['@'] = saved_dot
        else:
            frame.put_message('? No mark')

    def cut(self):
        """
        Delete from mark to line before dot, store deleted text in paste buffer.
        If no mark, do nothing.
        If mark follows dot, delete from dot to one before mark, reassign dot/
        """
        if '@' in text.buf.mark:
            start = text.buf.mark['@']
            end = text.buf.dot
            if start > end:
                start, end = end, start
            end -= 1 # exclude last line, dot (usually) or mark
            if check.range_ok(text.buf, start, end):
                self.inline_yank = False
                text.buf.d(start, end)
                frame.put_display_cursor()
        else:
            frame.put_message('? No mark')

    def kill_line(self):
        super().kill_line()
        if not ed.command_mode:
            text.buffer.Buffer.yank_lines = False
            text.buf.modified = True

    def discard(self):
        super().discard()
        if not ed.command_mode:
            text.buffer.Buffer.yank_lines = False
            text.buf.modified = True

    def yank(self):
        if ed.command_mode or self.inline_yank:
            # Insert string from self.yank_buffer inline at point.
            super().yank()
        else:
            # Insert lines from Buffer class cut_buffer before dot.
            text.buf.x(text.buf.dot-1) # ed x appends, edsel ^Y inserts
            text.buf.dot += 1  # x puts dot at last line in region, ^Y at first after
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
            match = next_text.search(text.buf.lines[prev_line], 0)
            if match:
                indent = match.start()+1
            else:
                prev_line -= 1
        return indent, prev_line

    def tab(self):
        'For first tab stop, try to match indentation of preceding line'
        if self.point == 0:
            indent, _ = self.prev_indent(text.buf.dot - 1)
        else:
            indent = self.n_tab_spaces
        self.tab_n(indent)
        text.buf.modified = True

    def other_window(self):
        'Move cursor to other window, next in sequence.'
        self.store_line()
        edda.o() # call frame.next() then reassign win, text.buf, text.current
        self.load_line()
        self.point = 0
        self.start_col = 1
        frame.put_display_cursor()

    def split_window(self):
        'Split window into two horizontally'
        edda.o(2)
        frame.put_display_cursor()
        
    def one_window(self):
        'Current window becomes the only window'
        edda.o(1)        
        frame.put_display_cursor()

    def switch_to_buffer(self):
        'Switch to another buffer, default is previous buffer'
        frame.put_message('Switch to buffer (default %s): ' % text.previous)
        # FIXME How best to collect non-default filename without blocking?

    # Run Python code and Shell commands

    def push_print_last_line(self):
        'Run Python statement at dot and print output at end of buffer'
        # name by analogy with emacs eval-print-last-sexp
        self.store_line() # Python statement
        edo.T()
        self.load_line() # empty line after Python output

    def shell_print_last_line(self):
        'Run shell commmand at dot and print output at end of buffer'
        # name by analogy with emacs eval-print-last-sexp
        self.store_line() # shell command
        edo.Z()
        self.load_line() # empty line after shell output

    # Miscellaneous commands, not bound to any keycodes

    def status(self):
        '^T handler, override base class'
        # Now ^T is bound to runlines
        if ed.command_mode:
            super().status()
        else:
            util.putstr('%s.%s point %s len %s dot %s nlines %s' %
                        (self.line[:self.point], self.line[self.point:],
                         self.point, len(self.line), text.buf.dot, text.buf.nlines()))

    def crash(self):
        'For now, just crash' # FIXME - not used, ^K is now console kill line
        return 1/0  # raise exception on demand (crash), for testing

    # Using the command line

    def execute(self):
        """
        Execute command: cursor moves to command line, prompt appears,
        then type any ed/edo/edda command, then type RET to return to display
        mode (without having to type C then RET).  The command can simply be a
        line address: a line number, $ (end), a search string in /.../ etc
        So this command acts as go-to-line or search command also.
        """
        self.collecting_command = True
        self.set_command_mode() # like edsel ^Z command
        # Now console will collect command line
        # BUT collecting_command tells console not to call accept_command
        # but (via keymap lambda with if...) to call accept_edsel_command
        # instead, which returns immediately to display mode.

    def accept_edsel_command(self):
        'After execute() above, execute the line, then return to display mode.'
        self.collecting_command = False
        if self.line == 'C': # no handler for 'C', avoid bogus 'command expected'
            print() # advance line in command region
        else:
            self.process_command() # exits inline editing with term.set_char_mode
        if self.stopped() and not self.quit: # if .quit, stop() already called
            self.stop()
        else:
            terminal.set_char_mode() # resume inline editing
            self.set_display_mode(text.buf.lines[text.buf.dot].rstrip('\n'))

    def cancel_edsel_command(self):
        'After execute() above, just discard the line, then return to display mode.'
        self.collecting_command = False
        self.move_beginning()
        display.kill_line()
        self.set_display_mode(text.buf.lines[text.buf.dot].rstrip('\n'))

    # Keymaps
         
    def init_edsel_keymaps(self):
        self.display_keys = {
            key.C_d: self.delete_char,
            # key.C_k: self.crash, # FIXME? Now ^K is kill
            key.C_j: self.push_print_last_line, # emacs has eval-print-last-sexp
            key.C_k: self.kill_line,
            key.C_l: self.refresh,
            key.C_n: self.next_line,
            # key.C_o: self.other_window, # now assigned to C_x + 'o'
            key.C_p: self.prev_line,
            key.C_r: self.rsearch,
            key.C_s: self.search,
            key.C_u: self.discard,
            key.C_v: self.page_down,
            key.C_w: self.cut,
            key.C_y: self.yank,
            key.C_z: self.set_command_mode,

            # M prefix - esc key prefix or alt key modifier
            key.M_j: self.shell_print_last_line,
            key.M_v: self.page_up,
            key.M_x: self.execute,
            key.M_lt: self.top,    # lt is <
            key.M_gt: self.bottom, # gt is >
            key.M_q: self.fill,

            # C_x prefix - window commands
            key.C_x + 'o' : self.other_window,
            key.C_x + '2' : self.split_window,
            key.C_x + '1' : self.one_window,

            # C_x prefix - miscellaneous
            key.C_x + key.C_x : self.exchange, # exchange point and mark

            # C_x prefix - buffer and file commands
            # FIXME not ready
            # key.C_x + key.C_b : ed.N, # list buffers in a buffer
            # key.C_x + 'b': self.switch_to_buffer,

            # C-space also works as C-@ on many terminals
            key.C_at: self.set_mark,
            key.cr: self.open_line,
            key.up: self.prev_line,
            key.down: self.next_line,
            key.bs: self.delete_backward_char,
            key.delete: self.delete_backward_char,
            }
        self.display_keymap = self.input_keymap.copy()# FIXME? Why?
        self.display_keymap.update(self.display_keys) # override some keys
        self.edsel_command_keys = {
            key.C_g: self.cancel_edsel_command,
            key.cr: self.accept_edsel_command,
            }
        # Be sure to preserve console command_keymap, we stil use it
        self.edsel_command_keymap = self.command_keymap.copy()
        self.edsel_command_keymap.update(self.edsel_command_keys)
        return (lambda: self.edsel_display_keymap)

edsel = Console(prompt=(lambda: wyshka.prompt),
               process_line=edda.process_line,
               stopped=(lambda command: ed.quit),
               startup=edda.startup, cleanup=edda.cleanup)

frame.console = edsel # frame needs edsel console instance to position cursor

edsel.keymap = (lambda: (edsel.edsel_command_keymap
                        if edsel.collecting_command
                        else edsel.display_keymap
                        if frame.mode == frame.Mode.display
                        else edsel.input_keymap
                        if frame.mode == frame.Mode.input
                        else edsel.command_keymap)) # frame.Mode.command

def main(*filename, **options):
    edsel.run(*filename, **options)

if __name__ == '__main__':
    filename, options = ed.cmd_options()
    main(*filename, **options)
