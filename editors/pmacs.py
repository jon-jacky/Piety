"""
pmacs.py - display editor that uses emacs control keys.

pmacs might mean 'Python emacs' but actually means 'partly inspired by emacs'
or maybe 'poor imitation of emacs'.
"""

import os # for vdir
import terminal, key, keyseq, display, edsel, dmacs, pycall
import sked as ed, editline as el
import editcommand as ec # only used in runrequest 
import viewer # for lsl in vdir

# Define and initialize global variables used by pmacs functions,
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = saved_put_marker # if already defined, then pmacs was already imported
except:
    inline = True # kill (cut) and yank (paste) within a single line
    # Now use edsel.start_col throughout, can use both editor and viewer panels
    # start_col = 0 is WRONG WRONG WRONG! - edsel.py sets start_col = 1 -!
    # start_col is used to put_cursor, and terminal column numbers are 1-based
    # unlike Python strings, including buffer text lines, which are 0-based.
    # start_col = 0  # default 0, no prompt or etc. at left margin # WRONG!
    saved_put_marker = edsel.put_marker # so we can restore after put_no_marker

running = True # rpm main loop is running, set False to exit.

# helper functions

def reset_point():
    'Possibly move ed.point if needed when dot moves to another line'
    linelen = len(ed.buffer[ed.dot])
    if ed.point > linelen:
        ed.point = linelen - 1 # -1 to put point before final \n

def restore_cursor_to_window():
    # reset_point() # no longer needed here, each pmacs fcn maintains ed.point
    # point+1 to make put_cursor call consistent with editline move_to_column
    # edsel.start_col so it works in  editor windows and also viewer window.
    # NOT ... ed.point + 1, no +1 needed, edsel.start_col is already 1
    display.put_cursor(edsel.wline(ed.dot), 
                       edsel.start_col + min(ed.point, edsel.width-1))

# Some functions do not use keycode arg but caller keycmd requires it to be there.

def next_line(keycode):
    'Move to next line, same column, or end of line if next line is too short'
    edsel.restore_cursor_to_cmdline() # so any error message appears in REPL
    edsel.l() # advances dot
    reset_point() # move to end of line if next line is too short
    restore_cursor_to_window()

def prev_line(keycode):
    'Move to previous line, same col, or end of line if prev line is too short'
    edsel.restore_cursor_to_cmdline()
    edsel.rl() # decrements dot
    reset_point() # move to end of line if previous line is too short
    restore_cursor_to_window()

def select_buffer(keycode):
    if ed.bufname == '*Buffers*':
        edsel.select_buffer()
        restore_cursor_to_window()
        
def open_line(keycode):
    """
    Split line at point, replace line in buffer at dot
    with its prefix, append suffix after line at dot.
    Preserve indentation: add as many spaces as needed before suffix line
     to match indentation of prefix line.
    Pad prefix with spaces to right window edge to work with viewer panel.
    """
    suffix = ed.buffer[ed.dot][ed.point:] # including final \n
    ed.buffer[ed.dot] = ed.buffer[ed.dot][:ed.point] + '\n' # leave prefix on dot
    if ed.point < edsel.width:
        edsel.blank_line(edsel.width - len(ed.buffer[ed.dot])) # pad with spaces
    # Auto-indent suffix line to same indentation as prefix line.
    nspaces = 0
    while ed.buffer[ed.dot][nspaces] == ' ': nspaces += 1 # count leading spaces
    ed.buffer[ed.dot+1:ed.dot+1] = [ nspaces*' ' + suffix ] # indent by nspaces
    ed.point = nspaces # put cursor at first char after leading spaces, 0-indexed
    ed.dot += 1
    if edsel.in_window(ed.dot):
        edsel.update_below(ed.dot)
        edsel.update_status() # so line number increments, saved updates
    else:
        edsel.recenter()  # calls edsel.refresh, edsel.update_status
    restore_cursor_to_window()

# The following functions supercede and wrap functions in other modules

def join_prev():
    'Join this line to previous. At first line do nothing.'
    if ed.dot > 1:
        ed.point = len(ed.buffer[ed.dot-1])-1 # don't count \n
        edsel.j(ed.dot-1, ed.dot) # defaults in ed.j join dot to dot+1

def delete_backward_char(keycode):
    """
    If point is not at start of line, delete preceding character.
    Otherwise join to previous line.  At start of first line do nothing.
    """
    if ed.point > 0:
        # Calls el.delete_backward_char, thanks to keycode DEL key.bs
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, edsel.start_col) 
        ed.save = False
    else: 
        join_prev() # see above
        restore_cursor_to_window()

def join_next():
    'Join next line to this one. At last line do nothing.'
    if ed.dot < ed.S():
        edsel.j() # defaults in ed.j join dot to dot+1

def delete_char(keycode):
    """
    If point is not at end of line, delete character under cursor.
    Otherwise join next line to this one.  At end of last line do nothing.
    """
    if ed.point < len(ed.buffer[ed.dot].rstrip('\n')):
        # Calls el.delete_char, thanks to keycode C_d
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, edsel.start_col)
        ed.saved = False
    else:
        join_next() # see above
        restore_cursor_to_window()

def kill_line(keycode):
    """
    In inline mode, kill line from the cursor up to but not including final \n
     save killed segment in editline.killed buffer for subsequent yank.
    In multline mode, kill entire line including final \n
     save consecutive killed lines in sked.killed buffer for subsequent yank.
    Manage transitions between inline and multiline modes:
    kill line on empty line consisting only of \n enters multiline mode.
    kill line after any other command than kill line resumes inline mode.
    """
    global inline
    # Lone kill line or first kill line in a series is inline ...
    if dmacs.prev_cmd != kill_line:
        inline = True
    # ... except begin multiline mode when kill empty line of only \n
    #      and we are not already in multiline mode
    if ed.buffer[ed.dot] == '\n' and inline: 
        inline = False # Enter multiline mode
        # If this is second consecutive C_k, copy previously killed line from 
        #  inline editline.killed buffer to multiline sked.killed buffer
        if dmacs.prev_cmd == kill_line:
            ed.killed = [el.killed+'\n'] # cp el.killed to 1st line sked.killed
        else: # we just killed empty line of only \n
            ed.killed = [] # clear sked.killed
        el.killed = '' # clear el.killed, start over. NB string not list
        # Delete the empty killed line from the buffer ...
        edsel.d(None,None,True) # ... and append line to killed buffer
        restore_cursor_to_window()
        # Now buffer and display are right, but killed has extra \n line at end
        ed.killed.remove('\n') # remove '\n' line
    # inline kill line:
    elif inline: # weaker condition, must follow previous stronger if...
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot],
                                                ed.point, edsel.start_col)
        ed.saved = False
    # kill line that is part of a multiline sequence:
    elif not inline:
        edsel.d(None,None,True) # consecutive C_k, append line to killed buffer
        restore_cursor_to_window()

def kill_region(keycode):
    global inline
    inline = False
    dmacs.runcmd(keycode) # keycode is C_w here
    restore_cursor_to_window()

def yank(keycode):
    """
    Yank entire line(s) or yank word(s) within a line, depending on inline
    """
    if inline:
        ed.buffer[ed.dot], ed.point = el.runcmd(keycode, ed.buffer[ed.dot], 
                                                 ed.point, edsel.start_col)
        ed.saved = False                                                 
    else:
        dmacs.runcmd(keycode) # keycode is C_y here
        restore_cursor_to_window()

def refresh(keycode):
    'Define pmacs whole window refresh here so we dont use editline refresh'
    dmacs.runcmd(keycode) # keycode is C_l here
    restore_cursor_to_window() 

def append(keycode):
    dmacs.runcmd(key.cr) # calls dmacs append, which enters append mode.
    restore_cursor_to_window()

# Following code replaces request() from dmacs, which uses blocking input(),
# with another request() written here that uses editline(), so it can  be
# adapted to non-blocking async code.  The code here is still blocking, though.

# response that is updated and returned by request(prompt), other vars
response = str()  
respcol = 1 # column after prompt where first char of response goes
respoint = 0 # index into response
resprunning = False  # True when loop is running, accumulating characters
respfinish = None # Assign _finish function to run when response is complete

def runrequest():
    'Body of request() loop, editline can handle a single char c without blocking'
    global response, respoint, resprunning
    c = terminal.getchar()  # might block here waiting for next character
    k = keyseq.keyseq(c)
    if k: # keyseq returns '' if key sequence is not complete
        if k == key.cr:  # RET finishes entering response and returns
            resprunning = False
            if respfinish: respfinish() # might be None for backward compat.
        elif k == key.C_g: # Cancel
            response += '???' # dmacs.cancelled tests response.endswith('???')
            resprunning = False
            if respfinish: respfinish() # might be None for backward compat.            
        # FIXME? We could have history, navigate with C_p and C_n
        else:
            # NB ed.runcmd not el.runcmd here only, editcommand not editline 
            response, respoint = ec.runcmd(k, response, respoint, respcol)

def request(prompt):
    'Use editline(), not like dmacs version that calls blocking input()'
    global response, respoint, resprunning, respcol
    display.put_cursor(dmacs.promptline, 1)
    display.kill_whole_line()
    # terminal.set_line_mode() # Remain in char mode -- unlike dmacs
    # response = input(prompt) # input() is blocking, instead loop on each char
    response = ''
    respoint = 0 
    respcol = len(prompt) + 1
    display.putstr(prompt) 
    display.put_cursor(dmacs.promptline, respcol)
    resprunning = True
    while resprunning:
        runrequest() # blocks waiting for each character here
    if dmacs.cancelled(response):
        dmacs.inform('Cancelled')  # also puts cursor at tlines
        restore_cursor_to_window() # but we want it in the window
    else: 
        display.put_cursor(edsel.tlines, 1)
    # terminal.set_char_mode() # We were in char mode all along
    return response

# For async, we must split request_start and request_finish                                           
def request_start(prompt):
    'Use editline(), not like dmacs version that calls blocking input()'
    global response, respoint, resprunning, respcol
    display.put_cursor(dmacs.promptline, 1)
    display.kill_whole_line()
    # terminal.set_line_mode() # Remain in char mode -- unlike dmacs
    # response = input(prompt) # input() is blocking, instead loop on each char
    response = ''
    respoint = 0 
    respcol = len(prompt) + 1
    display.putstr(prompt) 
    display.put_cursor(dmacs.promptline, respcol)
    resprunning = True
    # FIXME? Here eventloop would make a circular import with pmacs!
    # if eventloop.piety.is_running(): return # yield to async eventloop
    # Only run the following getchar loop if async eventloop is *not* running    
    while resprunning:
        # runrequest now calls getchar, blocks waiting for each char
        runrequest() # This must be last statement in request_start
                      # because key.cr case calls request_finish
    # runrequest updates response, but return None here.    

def request_finish():
    # This has to be a separate function so it can be moved to _finish
    # response has been updated by sync or async when we get here
    if dmacs.cancelled(response):
        dmacs.inform('Cancelled')  # also puts cursor at tlines
        restore_cursor_to_window() # but we want it in the window
    else: 
        display.put_cursor(edsel.tlines, 1)
    # terminal.set_char_mode() # We were in char mode all along
    return response

# The following functions are copied from dmacs
# but here they use the request() defined right above in this module.
# They are entered into this module's keymap so we dob't use dmacs version
# fcns called via keymap here must have a keycode arg even if they don't use it

def request_search(): 
    if not dmacs.prev_cmd in (fwd_search, bkwd_search):
        response = request(f'Search string (default {ed.searchstring}): ')
        if response and not dmacs.cancelled(response): ed.searchstring = response
        return response # because caller always check cancelled(response)
    else:
        return ed.searchstring # callers always check cancelled(response)

def fwd_search(keycode):
    response = request_search() # might update ed.searchstring
    if dmacs.cancelled(response): return # response might indicate search cancelled
    edsel.restore_cursor_to_cmdline() # So 'not found' message appears there
    edsel.s()
    restore_cursor_to_window() # dmacs runcmd does this automatically
    
def bkwd_search(keycode):
    response = request_search()
    if dmacs.cancelled(response): return
    edsel.restore_cursor_to_cmdline() # So 'not found' message appears there    
    edsel.r()
    restore_cursor_to_window() # dmacs runcmd does this automatically

# Hide this fcn while we experiment with new version, below    
def Xswitch_buffer(keycode):
    # global mark # now use dmacs.mark
    response = request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    edsel.b(response)
    restore_cursor_to_window() # dmacs runcmd does this automatically

# New version adapted for async - split off switch_buffer_finish
def switch_buffer(keycode):
    global respfinish
    respfinish = switch_buffer_finish
    # request_start returns nothing, in sync mode does update response
    request_start(f'Switch to buffer (default {ed.prev_bufname}): ')
     
def switch_buffer_finish():
    global respfinish
    respfinish = None # see runrequest key.cr case, for backward compatibility
    response = request_finish() # request_finish returns response
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    edsel.b(response)
    restore_cursor_to_window() # dmacs runcmd does this automatically
        
def find_file(keycode):
    # global mark  # now use dmacs.mark
    filename = request('Find file: ')
    if not filename or dmacs.cancelled(filename): return #  type RET to cancel
    dmacs.mark = 0
    edsel.e(filename)
    restore_cursor_to_window() # dmacs runcmd does this automatically

def write_named_file(keycode):
    filename = request('Write file: ')
    if dmacs.cancelled(filename): return
    edsel.w(filename)
    restore_cursor_to_window() # dmacs runcmd does this automatically    
    
def python_cmd(keycode):
    'Get and run a single Python command'
    cmd = request('>>> ')
    if dmacs.cancelled(cmd): return
    pycall.pycall(cmd)
    restore_cursor_to_window() # dmacs runcmd does this automatically    
    
def replace_string(keycode):
    response = request(f'Replace string (default {ed.searchstring}): ') 
    if dmacs.cancelled(response): return
    if response: ed.searchstring = response
    response = request(
     f'Replace {ed.searchstring} with (default {ed.replacestring}): ')
    if dmacs.cancelled(response): return
    if response == '\\\\\\': ed.replacestring = '' # \\\ -> empty string
    elif response: ed.replacestring = response # replace previous default
    else: pass # use previous default
    # Tried to fix edsel.c arg list for in_region with lambda, didn't work so:
    def c1(start=None, end=None):
        edsel.c(ed.searchstring, ed.replacestring, start, end)
    dmacs.in_region(c1)
    restore_cursor_to_window() # dmacs runcmd does this automatically    

# This function is from viewer

def vdir(keycode):
    """
    Prompt for directory (default cwd), then list directory in viewer window
    """
    cwd = os.getcwd()
    path = request(f'List directory (default {cwd}): ') # pmacs not dmacs
    if dmacs.cancelled(path): return
    if not path: path = cwd
    viewer.lsl(path) # calls viewer_window
    restore_cursor_to_window() # dmacs runcmd does this automatically        
    

keymap = {
    key.C_n: next_line,
    key.C_p: prev_line,
    key.cr: open_line,  # open_line takes keycode arg - FIXME?
    key.delete: delete_backward_char,
    key.bs: delete_backward_char, 
    key.C_d: delete_char,
    key.C_k: kill_line,
    key.C_w: kill_region,
    key.C_y: yank,
    key.C_l: refresh,
    key.C_x + key.C_a: append, # Enter dmacs append mode, exit with .
    # key.C-o is now assigned in viewer.py
    #key.C_o: select_buffer, # select_buffer takes keycode arg - FIXME?
    # arrow keys, send ANSI escape sequences
    key.down: next_line,
    key.up: prev_line,
    # Functions copied from dmacs that use request() defined here.
    key.C_s: fwd_search,
    key.C_r: bkwd_search,
    key.C_x + 'b' : switch_buffer,
    key.C_x + key.C_f : find_file,
    key.C_x + key.C_w : write_named_file, # write file, prompt for filename
    key.M_y: python_cmd,
    key.M_percent: replace_string, # M-%    
    key.C_x + 'd' : vdir
    }

def keycmd(keycode):
    """
    Execute a single pmacs key command: dispatch on key k, run function
    """
    cmd = keymap[keycode]
    cmd(keycode)
    dmacs.prev_cmd = cmd
    # Note: A few cmd call el.runcmd we believe we needn't update el.prev_cmd

def clear_marker():
    edsel.put_marker(ed.dot, display.clear)
    display.put_cursor(edsel.tlines, edsel.start_col)  # was ..., 1) not 0)

def put_no_marker(bufline, attribs): 
    'Assign to edsel.put_marker to suppress marker while running pmacs'
    pass

def setup():
    global running
    dmacs.open_promptline()
    clear_marker()
    edsel.put_marker = put_no_marker
    restore_cursor_to_window()
    running = True # previous M-x exit may have set it False

def restore():
    dmacs.close_promptline()
    edsel.put_marker = saved_put_marker # initialized in except branch above
    edsel.put_marker(ed.dot, display.reverse)
    edsel.restore_cursor_to_cmdline()

def runcmd(c):
    global running, inline
    k = keyseq.keyseq(c)
    if k: # keyseq returns '' if key sequence is not complete
        if k == key.M_x:
            running = False
        elif k in keymap:
            keycmd(k)
        elif k in el.printing_chars or k in el.keymap:
            el.prev_cmd = dmacs.prev_cmd
            if ed.S() < 1: ed.buffer = ['\n','\n'] # initialize empty buffer   
            if ed.dot == 0: ed.dot = 1 # buffer[0] is always dummy '\n'
            ed.buffer[ed.dot], ed.point = el.runcmd(k, ed.buffer[ed.dot],
                                          ed.point, edsel.start_col)
            if k in el.printing_chars:
                ed.saved = False # k was inserted into buffer
            dmacs.prev_cmd = el.prev_cmd
            # key.C_k and inline are handled in kill_line, above
            if k in (key.M_d, key.C_u): # M_d kill_word, C_u discard line 
                inline = True
        elif k in dmacs.keymap:
            edsel.restore_cursor_to_cmdline()
            dmacs.runcmd(k)
            restore_cursor_to_window()
   
def rpm():
    """
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'. 
    rpm means 'raw pm' - this function requires terminal is already 
    in char mode ('raw' mode) and it does not restore line mode
    when it exits - so this rpm is the function to call from pysh,
    our custom Python shell.  Call pm (below) from the Python >>> prompt.
    """
    setup()
    while running:
        c = terminal.getchar() # blocking
        runcmd(c)
    restore() 

def pm():
    """ 
    pmacs editor: invoke editor functions with emacs control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'. 
    This function assumes terminal is in line mode.
    It sets terminal character mode on entry and restores line mode on exit.
    So call this function from standard Python >>> prompt.
    Call rpm ('raw' pm) when terminal is already in char mode.
    So call rpm from our custom pysh >> prompt.
    """
    terminal.set_char_mode() 
    rpm() # raw pm, assumes term is already in char mode, doesn't restore mode
    terminal.set_line_mode()

# Synonyms for pm, possibly more memorable: 'visual editor', 'display editor'
ve = pm   # visual editor
ved = pm  # visual editor
de = pm   # display editor
ee = pm   # editor


