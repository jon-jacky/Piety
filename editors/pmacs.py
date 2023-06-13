"""
pmacs.py - Invoke editor functions with emacs keys (control keys or key seqs).

The module name pmacs differs from the editor function name pm
so the function name does not shadow the module name when we do
'from pmacs import pm' so we can type the function name in the REPL
without the module name prefix, just pm() not pmacs.pm().   
Then, if we edit more commands into pm, we can load them without restarting
the session by reload(pmacs).  The argument to reload must be the module name.
"""

import sys, importlib
import util, terminal, key, keyseq, display, edsel
import sked as ed

# Define and initialize global variables used by pmacs.
# Conditinally exec only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = mark # if mark is already defined, then pmacsinit was already exec'd
except:
    exec(open("pmacsinit.py").read())

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

def request(prompt):
    display.put_cursor(promptline, 1)
    display.kill_whole_line()
    terminal.set_line_mode()
    response = input(prompt)
    terminal.set_char_mode()
    return response

def request_search():
    if not prev_k in (key.C_s, key.C_r):
        response = request(f'Search string (default {ed.searchstring}): ')
        if response: ed.searchstring = response

def fwd_search():
    request_search()
    edsel.s()

def bkwd_search():
    request_search()
    edsel.r()

def switch_buffer():
    response = request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if response: ed.prev_bufname = response
    edsel.b()

def replace_string():
    response = request(f'Replace string (default {ed.searchstring}): ') 
    if response: ed.searchstring = response
    response = request(
     f'Replace {ed.searchstring} with (default {ed.replacestring}): ')
    if response: ed.replacestring = response
    edsel.c()

def find_file():
    filename = request('Find file: ')
    edsel.e(filename)

def write_named_file():
    filename = request('Write file: ')
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

def range():
    'Return start, end for ascending range defined by mark and dot'
    return (mark, ed.dot) if mark < ed.dot else (ed.dot, mark)

def in_region(f):
    'Execute function f on the region defined by mark and dot.'
    global mark
    if mark: # mark activated
        start, end = (mark, ed.dot) if mark < ed.dot else (ed.dot, mark)
        f(start, end)
    else:
        f()
    mark = 0 # deactivate mark

# FIXME: emacs C-w cuts from mark (inclusive) up to dot *exclusive*.
# But present edsel.d() deletes through dot *inclusive*.
# For now, our cut() must work the same way so edsel d() display still works.
# Later fix sked, edsel, pmacs so d() cut() and y() work like emacs C_w C_y.

def cut():
    start, end = range()
    edsel.d(start, end)

def yank():
    'Paste yank buffer after dot, move mark to first pasted line'
    global mark
    prev_dot = ed.dot
    edsel.y()
    mark = prev_dot # first pasted line

def wrap():
    start, end = range()
    edsel.wrap(start, end)

def join():
    start, end = range()
    edsel.j(start, end)

def indent():
    start, end = range()
    edsel.indent(start, end)

def outdent():
    start, end = range()
    edsel.outdent(start, end)

def reload():
    'Reload module for current buffer'
    modname = ed.bufname[:-3] # trim trailing '.py'
    importlib.reload(sys.modules[modname])
    print(f'Reload module {modname}\n\r', end='') # \n\r end for char mode

def save_reload():
    'Write out buffer, reload module, so file and module stay consistent.'
    ed.w()
    reload() # synchronization?  Does w() finish before reload() begins?

# Table from keys to editor functions
keycode = {
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
    key.C_k: edsel.d,   # delete line
    key.C_y: yank,   # yank (paste) deleted line
    key.cr: append,   # open line and enter append mode 
    # cut and paste
    key.C_at: set_mark,
    key.C_x + key.C_x : exchange_mark, # exchange dot and mark,
    key.C_w:  cut,    # use existing C_y (yank, above) for paste
    # formatting
    # key.M_q: wrap,
    key.M_q: (lambda: in_region(edsel.wrap)),
    key.M_carat: join,
    key.C_c + '>': indent, # like in emacs Python mode
    key.C_c + '<': outdent,
    # buffers and files
    key.C_x + 'b' : switch_buffer,
    key.C_x + key.C_b: ed.n, # list buffers  
    key.C_x + key.C_f : find_file,
    key.C_x + 'k' : edsel.k, # kill buffer, edsel.k prompts if file is unsaved
    key.C_x + key.C_s : edsel.w,  # write file, with stored filename
    key.C_x + key.C_w : write_named_file, # write file, prompt for filename
    key.C_x + key.C_r : save_reload, # *not* like emacs find-file read-only
    # miscellaneous
    key.C_l: edsel.refresh, # refresh, frame
}

def open_promptline():
    global promptline
    promptline = edsel.flines+1 # may have changed since prev pm() call
    display.set_scroll(promptline+1, edsel.tlines) # open prompt line
    display.put_cursor(promptline, 1)
    display.kill_whole_line() 
    display.put_cursor(edsel.tlines, 1)

def close_promptline():
    display.set_scroll(promptline, edsel.tlines) # dismiss prompt line

def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Supported keys and the fcns they invoke are expressed in keycode table.
    Exit by typing M_x (that's alt X).
    """
    global prev_k
    open_promptline()
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.M_x:
                prev_k = k
                break
            else:
                fcn = keycode.get(k, lambda: util.putstr(key.bel))
                fcn()
                prev_k = k
    terminal.set_line_mode()
    close_promptline()
    display.put_cursor(edsel.tlines, 1) # return cursor to command line
