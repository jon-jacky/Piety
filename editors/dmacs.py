"""
dmacs.py - Invoke editor functions with emacs keys (control keys or key seqs).

See README.md for directions on using dmacs, NOTES.txt about its code. 

The name means 'dumb emacs' or 'defective emacs' or maybe 'grade D emacs',
barely above F (fail).
"""

import sys, importlib
import terminal, key, keyseq, display, edsel
import sked as ed

# Define and initialize global variables used by dmacs.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = mark # if mark is already defined, then dmacsinit was already exec'd
except:
    from dmacsinit import *

def append():
    'Restore line mode, run edsel a(), return to char mode'
    terminal.set_line_mode()
    edsel.a()
    terminal.set_char_mode()

def inform(message):
    'Put informational message on prompt line, do not prompt, return nothing'
    display.put_cursor(promptline, 1)
    display.kill_whole_line()
    display.putstr(message)
    display.put_cursor(edsel.tlines, 1)

cancel = '???'

def cancelled(response):
    """
    Python input() does not return on ^G or any other control character.
    To cancel input(), must type printable chars into the input string itself.
    User types '???' at the end of the input string to cancel input().
    Caller can test for this and handle it.
    """
    return response.endswith(cancel)

def request(prompt):
    display.put_cursor(promptline, 1)
    display.kill_whole_line()
    terminal.set_line_mode()
    response = input(prompt)
    if cancelled(response):
        inform('Cancelled')  # also puts cursor at tlines
    else: 
        display.put_cursor(edsel.tlines, 1)
    terminal.set_char_mode()
    return response

def request_search():
    if not prev_cmd in (fwd_search, bkwd_search):
        response = request(f'Search string (default {ed.searchstring}): ')
        if response and not cancelled(response): ed.searchstring = response
        return response # because caller always check cancelled(response)
    else:
        return ed.searchstring # callers always check cancelled(response)

def fwd_search():
    response = request_search() # might update ed.searchstring
    if cancelled(response): return # response might indicate search cancelled
    edsel.s()

def bkwd_search():
    response = request_search()
    if cancelled(response): return
    edsel.r()

def switch_buffer():
    response = request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if cancelled(response): return
    if response: ed.prev_bufname = response
    edsel.b()

def find_file():
    filename = request('Find file: ')
    if cancelled(filename): return
    edsel.e(filename)

def write_named_file():
    filename = request('Write file: ')
    if cancelled(filename): return
    edsel.w(filename)

def set_mark():
    'Set mark at current dot'
    global mark
    mark = ed.dot
    inform(f'Mark set at line {mark}')

def exchange_mark():
    'Exchange mark and dot so you can see mark.'
    global mark
    iline, mark = mark, ed.dot
    edsel.display_move_dot(iline) # assigns ed.dot = iline

def in_region(f):
    'Execute function f on the region defined by mark and dot.'
    global mark
    if mark: # mark activated
        start, end = (mark, ed.dot) if mark < ed.dot else (ed.dot, mark)
        f(start, end)
    else:
        f() # mark deactivated, just execute f on dot
    mark = 0 # deactivate mark

def replace_string():
    response = request(f'Replace string (default {ed.searchstring}): ') 
    if cancelled(response): return
    if response: ed.searchstring = response
    response = request(
     f'Replace {ed.searchstring} with (default {ed.replacestring}): ')
    if cancelled(response): return
    if response == '\\\\\\': ed.replacestring = '' # \\\ -> empty string
    elif response: ed.replacestring = response # replace previous default
    else: pass # use previous default
    # Tried to fix edsel.c arg list for in_region with lambda, didn't work so:
    def c1(start=None, end=None):
        edsel.c(ed.searchstring, ed.replacestring, start, end)
    in_region(c1)

def kill_line():
    'Delete single line, accumulate consecutive deleted lines in yank buffer'
    if prev_cmd != kill_line: # first kill_line:, rewrite yank buffer
        edsel.d()
    else: 
        edsel.d(None,None,True) # consecutive C_k, append line to yank buffer

def reload_buffer():
    'Reload module for current buffer'
    modname = ed.bufname[:-3] # trim trailing '.py'
    importlib.reload(sys.modules[modname])
    print(f'Reload module {modname}\n\r', end='') # \n\r end for char mode

def save_reload():
    'Write out buffer, reload module, so file and module stay consistent.'
    edsel.w()
    reload_buffer() # synchronization?  Does w() finish before reload() begins?

# Table from keys to editor functions
keymap = {
    # cursor movement
    key.C_n: edsel.l,  # next line
    key.C_p: edsel.rl,  # previous line
    key.C_v: edsel.v,   # page down
    key.M_v: edsel.rv,  # page up
    key.M_lt: (lambda: edsel.p(1)), # go to top, line 1.  lt is <.
    key.M_gt: (lambda: edsel.p(ed.S())), # go to bottom, last line.  gt is >.
    # search and replace
    key.C_s: fwd_search,
    key.C_r: bkwd_search,
    key.M_percent: replace_string, # M-%
    # editing
    key.C_k: kill_line, # append consecutive killed lines to yank buffer
    key.C_y: edsel.y, # yank (paste) deleted lines
    key.cr: append,   # open line and enter append mode 
    # cut and paste
    key.C_at: set_mark,
    key.C_x + key.C_x : exchange_mark, # exchange dot and mark,
    key.C_w: (lambda: in_region(edsel.d)), # cut, use C_y (yank above) to paste
    # formatting
    key.M_q: (lambda: in_region(edsel.wrap)),
    key.M_carat: (lambda: in_region(edsel.j)), # join lines
    key.C_c + '>': (lambda: in_region(edsel.indent)), # like emacs Python mode
    key.C_c + '<': (lambda: in_region(edsel.outdent)),
    # buffers and files
    key.C_x + 'b' : switch_buffer,
    key.C_x + key.C_b: ed.n, # list buffers  
    key.C_x + key.C_f : find_file,
    key.C_x + 'k' : edsel.k, # kill buffer, edsel.k prompts if file is unsaved
    key.C_x + key.C_s : edsel.w,  # write file, with stored filename
    key.C_x + key.C_w : write_named_file, # write file, prompt for filename
    key.C_x + key.C_r : save_reload, # *not* like emacs find-file read-only
    # windows
    key.C_x + '2' : edsel.o2,
    key.C_x + '1' : edsel.o1,
    key.C_x + 'o' : edsel.on,
    # miscellaneous
    key.C_l: edsel.refresh, # refresh, frame
    # arrow keys, send ANSI escape sequences
    key.down: edsel.l, # next line
    key.up: edsel.rl, # previous line
}

def open_promptline():
    global promptline
    promptline = edsel.flines+1 # may have changed since prev dm() call
    display.set_scroll(promptline+1, edsel.tlines) # open prompt line
    display.put_cursor(promptline, 1)
    display.kill_whole_line() 
    display.put_cursor(edsel.tlines, 1)

def close_promptline():
    display.set_scroll(promptline, edsel.tlines) # dismiss prompt line

def runcmd(k):
    """
    Invoke a single dmacs command: look up k in keymap, run that command.
    """
    global prev_cmd
    cmd = keymap.get(k, lambda: display.putstr(key.bel))
    cmd()
    prev_cmd = cmd

def dm():
    """
    dmacs editor: loop invoking editor commands with emacs control keys.
    Supported keys and the cmds they invoke are expressed in keymap table.
    Exit by typing M_x (that's alt X), like emacs 'do command'.
    """
    open_promptline()
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                # preserve prev_cmd after dm exit for debugging and resuming
                break
            else:
                runcmd(k)
    terminal.set_line_mode()
    close_promptline()
    display.put_cursor(edsel.tlines, 1) # return cursor to command line
