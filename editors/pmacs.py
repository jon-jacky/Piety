"""
pmacs.py - Invoke editor functions with emacs keys (control keys or key seqs).

The module name pmacs differs from the editor function name pm
so the function name does not shadow the module name when we do
'from pmacs import pm' so we can type the function name in the REPL
without the module name prefix, just pm() not pmacs.pm().   
Then, if we edit more commands into pm, we can load them without restarting
the session by reload(pmacs).  The argument to reload must be the module name.
"""

import util, terminal, key, display, edsel
import sked as ed
from keyseq import keyseq

def append():
    'Restore line mode, run edsel a(), return to char mode'
    terminal.set_line_mode()
    edsel.a()
    terminal.set_char_mode()

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
    key.C_y: edsel.y,   # yank (paste) deleted line
    key.cr: append,   # open line and enter append mode 
    # formatting
    key.M_q: edsel.wrap,  # wrap, single long line
    # buffers and files
    key.C_x + 'b' : switch_buffer,
    key.C_x + key.C_f : find_file,
    key.C_x + 'k' : edsel.k, # edsel.k prompts if file is unsaved
    key.C_x + key.C_s : edsel.w,  # write file, with stored filename
    key.C_x + key.C_w : write_named_file, # write file, prompt for filename
    # miscellaneous
    key.C_l: edsel.refresh, # refresh, frame
}

promptline = 21

def open_promptline():
    global promptline
    promptline = edsel.flines+1 # may have changed since prev pm() call
    display.set_scroll(promptline+1, edsel.tlines) # open prompt line
    display.put_cursor(promptline, 1)
    display.kill_whole_line() 

def close_promptline():
    display.set_scroll(promptline, edsel.tlines) # dismiss prompt line

prev_k = key.C_z

def pm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Supported keys and the fcns they invoke are expressed in keycode table.
    Exit by typing C_z (that's ^Z).
    """
    global prev_k
    open_promptline()
    terminal.set_char_mode()
    while True:
        c = terminal.getchar()
        k = keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.C_z:
                prev_k = k
                break
            else:
                fcn = keycode.get(k, lambda: util.putstr(key.bel))
                fcn()
                prev_k = k
    terminal.set_line_mode()
    close_promptline()
    display.put_cursor(edsel.tlines, 1) # return cursor to command line
