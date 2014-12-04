"""
displayedit.py - Edit text on display with these functions.  

  These function both update text and insertion point, and render the
  modified text on the display.  
  The text argument must be an object that has text.line and text.point
"""


def putlines(s):
    """
    Format and print possibly multi-line string
    at each linebreak print \r\n
    """
    lines = s.splitlines()
    lastline = len(lines) - 1 # index of last line
    for iline, line in enumerate(lines):
        terminal.putstr(line)
        if iline < lastline:
            terminal.putstr('\r\n')

# Command line management
# These functions all start a new command line, never edit in line,
# so they all work on printing terminals.

def accept_line(self):
    self.history.append(self.cmdline) # save command in history list
    self.iline = len(self.history)-1
    self.do_command()

def do_command(self):
    'Process command line and restart'
    terminal.restore() # resume line mode for command output
    print # print command output on new line
    self.command(self.cmdline)
    self.restart()

def restart(self):
    'Clear command line, print command prompt, set single-char mode'
    self.cmdline = str()
    self.point = 0
    # not self.prompt, the cmd fcn may have changed the focus # FIXME?
    terminal.putstr(focus.prompt) # prompt does not end with \n
    terminal.setup() # enter or resume single character mode

def redraw_current_line(self):
    terminal.putstr('^L\r\n' + self.prompt)  # on new line
    putlines(self.cmdline) # might be multiple lines

def newline(self):
    self.cmdline += '\n'
    self.point += 1
    terminal.putstr('^J\r\n' + self.continuation)

def previous_history(self):
    if self.history:
        self.cmdline = self.history[self.iline]
    self.point = len(self.cmdline)
    self.iline = self.iline - 1 if self.iline > 0 else 0
    terminal.putstr('^P\r\n' + self.prompt) # on new line
    putlines(self.cmdline) # might be multiple lines

def next_history(self):
    self.iline = self.iline + 1 \
        if self.iline < len(self.history)-1 else self.iline
    if self.history:
        self.cmdline = self.history[self.iline]
    self.point = len(self.cmdline)
    terminal.putstr('^N\r\n' + self.prompt)  # on new line
    putlines(self.cmdline) # might be multiple lines

def line_discard(self): # name like gnu readline unix-line-discard
    self.cmdline = str() 
    self.point = 0
    terminal.putstr('^U\r\n' + self.prompt)

def interrupt(self):
    # raw mode terminal doesn't respond to ^C, must handle here
    terminal.putstr('^C') 
    terminal.restore() # on new line...
    print              # ... otherwise traceback is a mess
    raise KeyboardInterrupt

def handle_C_d(self):
    # two modes: manage command line or edit in line
    if not self.cmdline and not self.exit:
        terminal.putstr('^D\r\n' + noexit + '\r\n' + self.prompt)
    elif not self.cmdline and self.exit:
        self.end_of_file()
    else: # edit in line
        self.delete_char() # with line editing, below

def end_of_file(self):
    terminal.putstr('^D') 
    terminal.restore() 
    print # start new line
    self.point = 0
    self.exit() # call exiter

# Line editing
# None of these functions start a new line, they edit line in place.
# They accommodate a leading prompt, if one is present.

# The following work on printing terminals
# (they are not included in the keymap above)

def self_append_command(self, key):
    'Append last character on line, works on printing terminals'
    self.cmdline += key
    self.point += 1
    terminal.putstr(key)

def backward_delete_last_char(self):
    'Delete last character on line, works on printing terminals'
    if self.point > 0:
        ch = self.cmdline[-1]
        self.cmdline = self.cmdline[:-1]
        self.point -= 1
        # terminal.putstr('^H') # omit, it is more helpful to echo
        terminal.putstr('\\%s' % ch) # echo \ + deleted character

# The following all require video terminals with cursor addressing;
#  they do not work on printing terminals.
# They all appear in the keymap above.

def self_insert_command(self, key):
    self.cmdline = (self.cmdline[:self.point] 
                    + key + self.cmdline[self.point:])
    self.point += 1
    display.self_insert_char(key)

def backward_delete_char(self):
    if self.point > 0:
        self.cmdline = (self.cmdline[:self.point-1] 
                        + self.cmdline[self.point:])
        self.point -= 1
        display.backward_delete_char()

def move_beginning_of_line(self):
    self.point = 0
    start = len(self.prompt)+1 # allow for space after prompt
    display.move_to_column(start) # move to character after prompt

def backward_char(self):
    if self.point > 0:
        self.point -= 1
        display.backward_char()

def delete_char(self):
    self.cmdline = (self.cmdline[:self.point] 
                    + self.cmdline[self.point+1:])
    display.delete_char()

def move_end_of_line(self):
    self.point = len(self.cmdline)
    eol = len(self.prompt) + 1 + len(self.cmdline)
    display.move_to_column(eol)

def forward_char(self):
    if self.point < len(self.cmdline):
        self.point += 1
        display.forward_char()

def kill_line(self):
     self.cmdline = self.cmdline[:self.point] # point doesn't change
     display.kill_line()

