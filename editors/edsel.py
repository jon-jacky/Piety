"""
edsel - Full screen display editing, with screen editing keys defined
        in a new Console subclass.
"""

import re
import util, terminal
import keyboard, console, check, edda, pysh, wyshka, samysh

ed = edda.edo.ed    # use ed, frame, st APIs without prefix
st = ed.st
frame = edda.frame

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
            self.set_display_mode(st.buf.lines[st.buf.dot].rstrip('\n'))
        else:
            super().accept_command()

    # The following  methods and keymaps all have new names, so they are added
    #  to the ones in the Console base class, they do not replace any.

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
        st.buf.replace(st.buf.dot, self.line + '\n')
        ed.command_mode = True
        ed.prompt = ed.command_prompt
        wyshka.prompt = ed.prompt # self.do_command does this via wyshka shell
        frame.command_mode()
        self.restart() # print prompt and enter char mode

    def refresh(self):
        'Refresh entire display including whole frame and scrolling command region.'
        st.buf.replace(st.buf.dot, self.line + '\n') # so refresh renders it
        frame.refresh(self.start_col + self.point)

    def open_line(self):
        """
        Split line at point, replace line in buffer at dot
        with its prefix, append suffix after line at dot.
        """
        prefix = self.line[:self.point]
        suffix = self.line[self.point:].rstrip('\n')
        st.buf.replace(st.buf.dot, prefix + '\n')
        self.kill_line() # from cursor to end of line
        st.buf.a(st.buf.dot, suffix + '\n') # calls frame.insert()
        self.line = suffix
        self.point = 0
        self.start_col = 1

    def del_or_join_prev(self):
        """
        If point is not at start of line, delete preceding character
        Otherwise join to previous line.  At start of first line do nothing.
        """
        if self.point > 0:
            self.backward_delete_char()
        elif st.buf.dot > 1:
            new_point = len(st.buf.lines[st.buf.dot-1])-1 # don't count \n
            st.buf.replace(st.buf.dot, self.line)
            st.buf.j(st.buf.dot-1, st.buf.dot)
            self.line = st.buf.lines[st.buf.dot].rstrip('\n')
            self.point = new_point
            frame.put_display_cursor(column=(self.start_col + self.point))
        else:
            pass

    def join_next(self):
        'Helper - join next line to this one. At last line do nothing.'
        if st.buf.dot < st.buf.nlines():
            st.buf.replace(st.buf.dot, self.line)
            st.buf.j(st.buf.dot, st.buf.dot+1)
            self.line = st.buf.lines[st.buf.dot].rstrip('\n')
            frame.put_display_cursor(column=(self.start_col + self.point))
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
        if check.iline_ok(st.buf, iline):
            st.buf.replace(st.buf.dot, self.line + '\n')
            st.buf.l(iline)
            line = st.buf.lines[st.buf.dot].rstrip('\n')  # FIXME? [iline] - ?
            self.line = line
            self.point = min(jcol, len(line))
            frame.put_display_cursor(column=(self.start_col + self.point))
        if iline == st.buffer.no_match:
            frame.put_message('? no match')

    def prev_line(self):
        """
        Move cursor from current line in window to same
        column in line above, or end of line - whichever comes first.
        When cursor would leave top, redraw window with current line in middle
        Replace current line in buffer and copy preceding buffer line into line
        """
        self.goto_line(st.buf.dot-1, self.point)

    def next_line(self):
        'Like prev_line, but line below/bottom.'
        self.goto_line(st.buf.dot+1, self.point)

    def page_down(self):
        'Move cursor forward several/many lines.'
        dest = min(st.buf.dot + frame.win.nlines - 1, st.buf.nlines())
        self.goto_line(dest, self.point)

    def page_up(self):
        'Move cursor backward several/many lines.'
        dest = max(st.buf.dot - frame.win.nlines + 1, 1)
        self.goto_line(dest, self.point)

    def search(self):
        'Search forward for previous search string.'
        self.goto_line(st.buf.F(''), self.point)

    def rsearch(self):
        'Search backward for previous search string.'
        self.goto_line(st.buf.R(''), self.point)

    def set_mark(self):
        'Define region from mark (inclusive) to dot (exclusive) that is deleted by cut'
        st.buf.mark['@'] = st.buf.dot
        frame.put_message('Mark set')

    def exchange(self):
        'Exchange point and mark (to make mark visible by putting cursor there).'
        if '@' in st.buf.mark:
            saved_dot = st.buf.dot
            self.goto_line(st.buf.mark['@'], 1) # updates st.buf.dot
            st.buf.mark['@'] = saved_dot
        else:
            frame.put_message('? No mark')

    def cut(self):
        """
        Delete from mark to line before dot, store deleted text in paste buffer.
        If no mark, do nothing.
        If mark follows dot, delete from dot to one before mark, reassign dot/
        """
        if '@' in st.buf.mark:
            start = st.buf.mark['@']
            end = st.buf.dot
            if start > end:
                start, end = end, start
            end -= 1 # exclude last line, dot (usually) or mark
            if check.range_ok(st.buf, start, end):
                st.buf.d(start, end)
                frame.put_display_cursor()
        else:
            frame.put_message('? No mark')

    def kill(self):
        super().kill()
        if not ed.command_mode:
            st.buffer.Buffer.yank_lines = False
            st.buf.modified = True

    def discard(self):
        super().discard()
        if not ed.command_mode:
            st.buffer.Buffer.yank_lines = False
            st.buf.modified = True

    def yank(self):
        if ed.command_mode or not st.buffer.Buffer.yank_lines:
            # Insert string from self.yank_buffer inline at point.
            super().yank()
        else:
            # Insert lines from Buffer class cut_buffer before dot.
            st.buf.x(st.buf.dot-1) # ed x appends, edsel ^Y inserts
            st.buf.dot += 1  # x puts dot at last line in region, ^Y at first after
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
            match = next_text.search(st.buf.lines[prev_line], 0)
            if match:
                indent = match.start()+1
            else:
                prev_line -= 1
        return indent, prev_line

    def tab(self):
        'For first tab stop, try to match indentation of preceding line'
        if self.point == 0:
            indent, _ = self.prev_indent(st.buf.dot - 1)
        else:
            indent = self.n_tab_spaces
        self.tab_n(indent)
        st.buf.modified = True

    def other_window(self):
        'Move cursor to other window, next in sequence.'
        st.buf.replace(st.buf.dot, self.line + '\n') # from goto_line
        edda.o() # call frame.next() then reassign win, st.buf, st.current
        self.line = st.buf.lines[st.buf.dot].rstrip('\n') # from several methods
        # From set_display_mode
        self.point = 0
        self.start_col = 1
        frame.put_display_cursor()

    def status(self):
        '^T handler, override base class, for now print items used by del_or_join_next'
        # Now ^T is bound to runlines
        if ed.command_mode:
            super().status()
        else:
            util.putstr('%s.%s point %s len %s dot %s nlines %s' %
                        (self.line[:self.point], self.line[self.point:],
                         self.point, len(self.line), st.buf.dot, st.buf.nlines()))

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
            self.set_display_mode(st.buf.lines[st.buf.dot].rstrip('\n'))

    def cancel_edsel_command(self):
        'After execute() above, just discard the line, then return to display mode.'
        self.collecting_command = False
        self.move_beginning()
        self.kill_line()
        self.set_display_mode(st.buf.lines[st.buf.dot].rstrip('\n'))

    def crash(self):
        'For now, just crash' # FIXME - not used, ^K is now console kill line
        return 1/0  # raise exception on demand (crash), for testing

    def runlines(self):
        """
        Run Python statements in current selection (mark to dot).
        If there is no current selection, just run the current line.
        """
        if '@' in st.buf.mark:
            start = st.buf.mark['@']
            end = st.buf.dot
            if start > end:
                start, end = end, start
            end -= 1 # exclude last line, dot (usually) or mark
        else:
            start = end = st.buf.dot
        if check.range_ok(st.buf, start, end):
            terminal.set_line_mode() # exit inline editing, prepare for P(...)
            frame.put_command_cursor()
            # Use pushlines, uses code.InteractiveConsole not builtin exec
            pysh.pushlines(st.buf.lines[start:end+1])
            # Sometimes buf.lines prints nothing - did anything happen?
            print('%s, ran lines %d..%d' % (st.current, start, end))
            terminal.set_char_mode() # resume inline editing
            frame.put_display_cursor()

    def init_edsel_keymaps(self):
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
            keyboard.C_t: self.runlines, # overrides base class ^T status
            keyboard.C_u: self.discard,
            keyboard.C_v: self.page_down,
            keyboard.C_w: self.cut,
            keyboard.C_x: self.execute,
            keyboard.C_y: self.yank,
            keyboard.C_z: self.set_command_mode,
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
        self.edsel_command_keys = {
            keyboard.C_g: self.cancel_edsel_command,
            keyboard.cr: self.accept_edsel_command,
            }
        # Be sure to preserve console command_keymap, we stil use it
        self.edsel_command_keymap = self.command_keymap.copy()
        self.edsel_command_keymap.update(self.edsel_command_keys)
        return (lambda: self.edsel_display_keymap)

edsel = Console(prompt=(lambda: wyshka.prompt),
               process_line=edda.process_line,
               stopped=(lambda command: ed.quit),
               startup=edda.startup, cleanup=edda.cleanup)

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
