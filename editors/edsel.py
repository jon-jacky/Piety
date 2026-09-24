"""
edsel.py - Piety display editor.
           
Command the edsel editor by typing control keys or calling Python functions.
edsel does not call blocking functions like Python input(), so it can
run from an asyncio event loop.
"""

import os # for vdir
import terminal, key, keyseq, display, dmacs, pycall
import frame as fr, editline as el
import editcommand as ec # only used in runrequest 
import viewer # for lsl in vdir
import sked as edlib # edlib not ed so we can define a function ed() here.

# To prevent importing the eventloop module into edsel,
# import the disable_eventloop module before importing this edsel module.

import sys
eventloop_enabled = True # default
if 'disable_eventloop' in sys.modules:
    eventloop_enabled = False
    # don't import eventloop
else:
    import eventloop     

# Define and initialize global variables used by edsel functions,
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables.
try:
    _ = saved_put_marker # if already defined, then edsel was already imported
except:
    inline = True # kill (cut) and yank (paste) within a single line
    # Now use fr.start_col throughout, can use both editor and viewer panels
    # start_col = 0 is WRONG WRONG WRONG! - frame.py sets start_col = 1 -!
    # start_col is used to put_cursor, and terminal column numbers are 1-based
    # unlike Python strings, including buffer text lines, which are 0-based.
    # start_col = 0  # default 0, no prompt or etc. at left margin # WRONG!
    saved_put_marker = fr.put_marker # so we can restore after put_no_marker
         
running = True # red main loop is running, set False to exit.

# helper functions

def reset_point():
    'Possibly move edlib.point if needed when dot moves to another line'
    linelen = len(edlib.buffer[edlib.dot])
    if edlib.point > linelen:
        edlib.point = linelen - 1 # -1 to put point before final \n

def restore_cursor_to_window():
    # reset_point() # no longer needed here, each edsel fcn maintains edlib.point
    # point+1 to make put_cursor call consistent with editline move_to_column
    # fr.start_col so it works in  editor windows and also viewer window.
    # NOT ... edlib.point + 1, no +1 needed, fr.start_col is already 1
    display.put_cursor(fr.wline(edlib.dot), 
                       fr.start_col + min(edlib.point, fr.width-1))

# Some functions do not use keycode arg but caller keycmd requires it to be there.

def next_line(keycode):
    'Move to next line, same column, or end of line if next line is too short'
    fr.restore_cursor_to_cmdline() # so any error message appears in REPL
    fr.l() # advances dot
    reset_point() # move to end of line if next line is too short
    restore_cursor_to_window()

def prev_line(keycode):
    'Move to previous line, same col, or end of line if prev line is too short'
    fr.restore_cursor_to_cmdline()
    fr.rl() # decrements dot
    reset_point() # move to end of line if previous line is too short
    restore_cursor_to_window()

def select_buffer(keycode):
    if edlib.bufname == '*Buffers*':
        fr.select_buffer()
        restore_cursor_to_window()
        
def open_line(keycode):
    """
    Split line at point, replace line in buffer at dot
    with its prefix, append suffix after line at dot.
    Preserve indentation: add as many spaces as needed before suffix line
     to match indentation of prefix line.
    Pad prefix with spaces to right window edge to work with viewer panel.
    """
    suffix = edlib.buffer[edlib.dot][edlib.point:] # including final \n
    edlib.buffer[edlib.dot] = edlib.buffer[edlib.dot][:edlib.point] + '\n' # leave prefix on dot
    if edlib.point < fr.width:
        fr.blank_line(fr.width - len(edlib.buffer[edlib.dot])) # pad with spaces
    # Auto-indent suffix line to same indentation as prefix line.
    nspaces = 0
    while edlib.buffer[edlib.dot][nspaces] == ' ': nspaces += 1 # count leading spaces
    edlib.buffer[edlib.dot+1:edlib.dot+1] = [ nspaces*' ' + suffix ] # indent by nspaces
    edlib.point = nspaces # put cursor at first char after leading spaces, 0-indexed
    edlib.dot += 1
    if fr.in_window(edlib.dot):
        fr.update_below(edlib.dot)
        fr.update_status() # so line number increments, saved updates
    else:
        fr.recenter()  # calls fr.refresh, fr.update_status
    restore_cursor_to_window()

# The following functions supercede and wrap functions in other modules

def join_prev():
    'Join this line to previous. At first line do nothing.'
    if edlib.dot > 1:
        edlib.point = len(edlib.buffer[edlib.dot-1])-1 # don't count \n
        fr.j(edlib.dot-1, edlib.dot) # defaults in edlib.j join dot to dot+1

def delete_backward_char(keycode):
    """
    If point is not at start of line, delete preceding character.
    Otherwise join to previous line.  At start of first line do nothing.
    """
    if edlib.point > 0:
        # Calls el.delete_backward_char, thanks to keycode DEL key.bs
        edlib.buffer[edlib.dot], edlib.point = el.runcmd(keycode, edlib.buffer[edlib.dot],
                                                edlib.point, fr.start_col) 
        edlib.save = False
    else: 
        join_prev() # see above
        restore_cursor_to_window()

def join_next():
    'Join next line to this one. At last line do nothing.'
    if edlib.dot < edlib.S():
        fr.j() # defaults in edlib.j join dot to dot+1

def delete_char(keycode):
    """
    If point is not at end of line, delete character under cursor.
    Otherwise join next line to this one.  At end of last line do nothing.
    """
    if edlib.point < len(edlib.buffer[edlib.dot].rstrip('\n')):
        # Calls el.delete_char, thanks to keycode C_d
        edlib.buffer[edlib.dot], edlib.point = el.runcmd(keycode, edlib.buffer[edlib.dot],
                                                edlib.point, fr.start_col)
        edlib.saved = False
    else:
        join_next() # see above
        restore_cursor_to_window()

def kill_line(keycode):
    """
    In inline mode, kill line from the cursor up to but not including final \n
     save killed segment in editline.killed buffer for subsequent yank.
    In multline mode, kill entire line including final \n
     save consecutive killed lines in skedlib.killed buffer for subsequent yank.
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
    if edlib.buffer[edlib.dot] == '\n' and inline: 
        inline = False # Enter multiline mode
        # If this is second consecutive C_k, copy previously killed line from 
        #  inline editline.killed buffer to multiline skedlib.killed buffer
        if dmacs.prev_cmd == kill_line:
            edlib.killed = [el.killed+'\n'] # cp el.killed to 1st line skedlib.killed
        else: # we just killed empty line of only \n
            edlib.killed = [] # clear skedlib.killed
        el.killed = '' # clear el.killed, start over. NB string not list
        # Delete the empty killed line from the buffer ...
        fr.d(None,None,True) # ... and append line to killed buffer
        restore_cursor_to_window()
        # Now buffer and display are right, but killed has extra \n line at end
        edlib.killed.remove('\n') # remove '\n' line
    # inline kill line:
    elif inline: # weaker condition, must follow previous stronger if...
        edlib.buffer[edlib.dot], edlib.point = el.runcmd(keycode, edlib.buffer[edlib.dot],
                                                edlib.point, fr.start_col)
        edlib.saved = False
    # kill line that is part of a multiline sequence:
    elif not inline:
        fr.d(None,None,True) # consecutive C_k, append line to killed buffer
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
        edlib.buffer[edlib.dot], edlib.point = el.runcmd(keycode, edlib.buffer[edlib.dot], 
                                                 edlib.point, fr.start_col)
        edlib.saved = False                                                 
    else:
        dmacs.runcmd(keycode) # keycode is C_y here
        restore_cursor_to_window()

def refresh(keycode):
    'Define edsel whole window refresh here so we dont use editline refresh'
    dmacs.runcmd(keycode) # keycode is C_l here
    restore_cursor_to_window() 

def append(keycode):
    dmacs.runcmd(key.cr) # calls dmacs append, which enters append mode.
    restore_cursor_to_window()

# Following code replaces request() from dmacs, which uses blocking input(),
# with new request_start() and request_finish() here that use editline(), 
# so they can work with non-blocking async code.  

# response that is updated and returned by request(prompt), other vars
response = str()  
respcol = 1 # column after prompt where first char of response goes
respoint = 0 # index into response
resprunning = False  # True when loop is running, accumulating characters
respfinish = None # Assign _finish function to run when response is complete

history = [] # List of past filename, bufname, searchstring etc.
i_cmd = -1 # index into history, code will assign to 0 or greater
max_cmds = 100 # maximum number of strings in history.  20 is not enough!

def runrequest():
    'Body of request() loop, editline can handle a single char c without blocking'
    # This resembles pyshell.py runcmd
    global response, respoint, resprunning, history, i_cmd
    c = terminal.getchar()  # might block here waiting for next character
    k = keyseq.keyseq(c)
    if k: # keyseq returns '' if key sequence is not complete
        if k == key.cr:  # RET finishes entering response and returns
            resprunning = False
            history.insert(0,response)
            if len(history) > max_cmds: history.pop()
            i_cmd = 0
            if respfinish: respfinish() # might be None for backward compat.
        elif k == key.C_g: # Cancel
            response += '???' # dmacs.cancelled tests response.endswith('???')
            resprunning = False
            if respfinish: respfinish() # might be None for backward compat.            
        # history code copied from  pyshell.py runcmd
        elif k in (key.C_p, key.up):
            if i_cmd < len(history)-1: i_cmd += 1
            response = history[i_cmd]
            respoint = len(response)
            el.refresh(response, respoint, respcol)
        elif k in (key.C_n, key.down):
            if i_cmd >= 0: i_cmd -= 1  # reaches -1 after most recent...
            if i_cmd < 0: cmd = ''   # ... then set cmd empty
            response = history[i_cmd]
            respoint = len(response)
            el.refresh(response, respoint, respcol)
        else:
            # NB edlib.runcmd not el.runcmd here only, editcommand not editline 
            response, respoint = ec.runcmd(k, response, respoint, respcol)

# For async, we must split request_start and request_finish                                           
def request_start(prompt, finish_fcn):
    'Use editline(), not like dmacs version that calls blocking input()'
    global response, respoint, resprunning, respcol
    global respfinish
    respfinish = finish_fcn
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
    # DEBUG below
    # print(f'request_start: async {eventloop.piety.is_running()}, prev_cmd {dmacs.prev_cmd}, requesting {requesting}, response {response}, searchstring {edlib.searchstring}, request_start')           
    # yield to async eventloop if needed:
    if eventloop_enabled and eventloop.piety.is_running(): return 
    # Only run the following getchar loop if async eventloop is *not* running    
    while resprunning:
        # runrequest now calls getchar, blocks waiting for each char
        runrequest() # This must be last statement in request_start
                      # because key.cr case calls request_finish
    # runrequest updates response, but return None here.    

def request_finish():
    # This has to be a separate function so it can be moved to _finish
    # response has been updated by sync or async when we get here
    global respfinish
    respfinish = None # see runrequest key.cr case, for backward compatibility
    if dmacs.cancelled(response):
        dmacs.inform('Cancelled')  # also puts cursor at tlines
        restore_cursor_to_window() # but we want it in the window
    else: 
        display.put_cursor(fr.tlines, 1)
    # terminal.set_char_mode() # We were in char mode all along
    # DEBUG below
    # print(f'request_finish: async {eventloop.piety.is_running()}, prev_cmd {dmacs.prev_cmd}, requesting {requesting}, response {response}, searchstring {edlib.searchstring}, request_finish')                   
    return response

# The following functions are copied from dmacs
# but here they use the request() defined right above in this module.
# They are entered into this module's keymap so we dob't use dmacs version
# fcns called via keymap here must have a keycode arg even if they don't use it

search_fcn = None  # fr.s forward or fr.r backward, assigned in search()
requesting = False # Used in search and search_finish

def search(keycode):
    global search_fcn, requesting
    search_fcn = fr.s if keycode == key.C_s else fr.r
    if not dmacs.prev_cmd == search:
        request_start(f'Search string (default {edlib.searchstring}): ', 
                        search_finish)
        requesting = True                         
    else:
        search_finish() # We already have search string

def search_finish():
    global response, requesting
    if requesting:
        response = request_finish() 
        if dmacs.cancelled(response): return
        if response: edlib.searchstring = response # if '', keep old searchstring
        requesting = False
    # else we already have searchstring
    # DEBUG below
    # print(f'search_finish: async {eventloop.piety.is_running()}, prev_cmd {dmacs.prev_cmd}, requesting {requesting}, response {response}, searchstring {edlib.searchstring} search_finish')               
    fr.restore_cursor_to_cmdline() # So 'not found' message appears there
    search_fcn() # fr.s forward or fr.r backward, assigned in search()
    restore_cursor_to_window() # dmacs runcmd does this automatically

# New version adapted for async - split off switch_buffer_finish
def switch_buffer(keycode):
    # request_start returns nothing, in sync mode does update response
    request_start(f'Switch to buffer (default {edlib.prev_bufname}): ',
                    switch_buffer_finish)
     
def switch_buffer_finish():
    response = request_finish() # request_finish returns response
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    fr.b(response)
    restore_cursor_to_window() # dmacs runcmd does this automatically
        
def find_file(keycode):
    request_start('Find file: ', find_file_finish)
    
def find_file_finish():
    filename = request_finish()    
    if not filename or dmacs.cancelled(filename): return #  type RET to cancel
    dmacs.mark = 0
    fr.e(filename)
    restore_cursor_to_window() # dmacs runcmd does this automatically

def write_named_file(keycode):
    request_start('Write file: ', write_named_file_finish)
    
def write_named_file_finish():
    filename = request_finish()    
    if dmacs.cancelled(filename): return
    fr.w(filename)
    restore_cursor_to_window() # dmacs runcmd does this automatically    
    
def python_cmd(keycode):
    'Get and run a single Python command'
    request_start('>>> ', python_cmd_finish)
    
def python_cmd_finish():
    cmd = request_finish()
    if dmacs.cancelled(cmd): return
    pycall.pycall(cmd)
    restore_cursor_to_window() # dmacs runcmd does this automatically    
    
def replace_string(keycode):
    """
    replace_string has to request both searchstring and replacestring, 
    so we split the function into *three* fcns not just two.
    This fcn requests the search string, then passes control to the second fcn,
    which request the replace string.
    """
    request_start(f'Replace string (default {edlib.searchstring}): ',
                                request_replacestring) 
                                
def request_replacestring():
    """   
    This is the second function in replacestring,
    which assigns edlib.searchstring and requests replacestring,
    and passes control to the third function, replace_string_finish.
    """
    response = request_finish() # response is the searchstring
    if dmacs.cancelled(response): return # don't request replacestring
    if response: edlib.searchstring = response
    request_start(f'Replace {edlib.searchstring} with (default {edlib.replacestring}): ',
                    replace_string_finish)
                    
def replace_string_finish():
    """
    This is the third and final function in replace_string,
    which assigns edlib.replacestring and performs the replacement.
    """
    response = request_finish() # response is the replacestring                    
    if dmacs.cancelled(response): return  # don't attempt replacement
    if response == '\\\\\\': edlib.replacestring = '' # \\\ -> empty string
    elif response: edlib.replacestring = response # replace previous default
    else: pass # use previous default
    # Tried to fix fr.c arg list for in_region with lambda, didn't work so:
    def c1(start=None, end=None):
        fr.c(edlib.searchstring, edlib.replacestring, start, end)
    dmacs.in_region(c1)
    restore_cursor_to_window() # dmacs runcmd does this automatically    

# This function is from viewer

def vdir(keycode):
    """
    Prompt for directory (default cwd), then list directory in viewer window
    """
    cwd = os.getcwd() # needed for prompt    
    request_start(f'List directory (default {cwd}): ', vdir_finish)

def vdir_finish():
    cwd = os.getcwd() # default
    path = request_finish()
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
    # Functions copied from dmacs that use request_start, _finish defined here.
    key.C_s: search, # forward search, computed from keycode in search()
    key.C_r: search, # backward search, computed from keycode in search()
    key.C_x + 'b' : switch_buffer,
    key.C_x + key.C_f : find_file,
    key.C_x + key.C_w : write_named_file, # write file, prompt for filename
    key.M_y: python_cmd,
    key.M_percent: replace_string, # M-%    
    key.C_x + 'd' : vdir
    }

def keycmd(keycode):
    """
    Execute a single edsel key command: dispatch on key k, run function
    """
    cmd = keymap[keycode]
    cmd(keycode)
    dmacs.prev_cmd = cmd
    # Note: A few cmd call el.runcmd we believe we needn't update el.prev_cmd

def clear_marker():
    fr.put_marker(edlib.dot, display.clear)
    display.put_cursor(fr.tlines, fr.start_col)  # was ..., 1) not 0)

def put_no_marker(bufline, attribs): 
    'Assign to fr.put_marker to suppress marker while running edsel'
    pass

def setup():
    global running
    dmacs.open_promptline()
    clear_marker()
    fr.put_marker = put_no_marker
    restore_cursor_to_window()
    running = True # previous M-x exit may have set it False

def restore():
    dmacs.close_promptline()
    fr.put_marker = saved_put_marker # initialized in except branch above
    fr.put_marker(edlib.dot, display.reverse)
    fr.restore_cursor_to_cmdline()

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
            if edlib.S() < 1: edlib.buffer = ['\n','\n'] # initialize empty buffer   
            if edlib.dot == 0: edlib.dot = 1 # buffer[0] is always dummy '\n'
            edlib.buffer[edlib.dot], edlib.point = el.runcmd(k, edlib.buffer[edlib.dot],
                                          edlib.point, fr.start_col)
            if k in el.printing_chars:
                edlib.saved = False # k was inserted into buffer
            dmacs.prev_cmd = el.prev_cmd
            # key.C_k and inline are handled in kill_line, above
            if k in (key.M_d, key.C_u): # M_d kill_word, C_u discard line 
                inline = True
        elif k in dmacs.keymap:
            fr.restore_cursor_to_cmdline()
            dmacs.runcmd(k)
            restore_cursor_to_window()
   
def red():
    """
    edsel editor: invoke editor functions with control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'. 
    red means 'raw ed' - this function requires terminal is already 
    in char mode ('raw' mode) and it does not restore line mode
    when it exits - so this red is the function to call from pysh,
    our custom Python shell.  Call ed (below) from the Python >>> prompt.
    """
    setup()
    while running:
        c = terminal.getchar() # blocking
        runcmd(c)
    restore() 

def ed():
    """ 
    edsel editor: invoke editor functions with control keys.
    Exit by typing M_x (that's alt X), like emacs 'do command'. 
    This function assumes terminal is in line mode.
    It sets terminal character mode on entry and restores line mode on exit.
    So call this function from standard Python >>> prompt.
    Call red ('raw' ed) when terminal is already in char mode.
    So call red from our custom pysh >> prompt.
    """
    terminal.set_char_mode() 
    red() # raw ed, assumes term is already in char mode, doesn't restore mode
    terminal.set_line_mode()


