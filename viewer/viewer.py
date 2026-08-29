"""
viewer.py  - Experiments with a viewer window beside the editor windows

The viewer has its own current buffer and its own window that are always
displayed and always available, which are implicitly selected by the 
commands (functions) defined in this module.

The editor current buffer and windows managed by the sked and edsel
modules, and the commands that use them, are unchanged, always
available, and work just as before.
"""

import os, sys
import key, dmacs, display, shell, render, console, get
import sked as ed, edsel as fr
import traceback
from redirect import redirect # for printing traceback in a buffer
 
# Define and initialize global variables
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables,
# so we retain buffer contents and other state when we reload.
 
try:
    _ = vkey # If this is already defined, this module was already imported.
except:
    # vkey is index of viewer window in fr.windows. 
    # All editor window keys are >= 0
    vkey = -1 
    # saved_focus is index of editor window in fr.windows
    # before and after viewer window is selected.
    saved_focus = 0 #  assigned in ov(), restored in oe()
    viewer_displayed = False
    leftedge = 81      
    rmargin = 60 # for Debian Linux console viewer - may be reassigned.
    width = 64 #  for Debian Linux console viewer on Chromebook
                
def viewer_focus():
    'Return True when the viewer window has the focus'
    return viewer_displayed and fr.start_col > 1
    
def display_border():
    """
    Draw viewer panel borders: left edge and empty status line
    """
    display.put_cursor(1, leftedge)
    for iline in range(fr.flines - 1): # 0 indexed, preserve status line
        display.put_cursor(iline + 1, leftedge) # terminal lines 1 indexed
        display.render('|', display.reverse) # L edge window border
        display.kill_line() # end of line to window R edge
    display.put_cursor(fr.flines, leftedge)
    display.render('|' + (width-1)*' ', display.reverse) # empty status liee.
    
def vrefresh():
    """
    Draw viewer panel border then populate with buffer contents and status line..
    """        
    if not viewer_focus():
        print('? viewer window does not have focus\r\n', end='')
        return
    display_border()
    fr.refresh() # this works only if viewer window has focus

def ov():
    """
    Switch focus from editor to viewer buffer and window.
    """
    global saved_focus
    if viewer_focus():
        print('? viewer window already has focus\r\n', end='')
        return
    # save_window calls save_buffer
    fr.save_window(fr.focus) # viewer does not change editor focus window.
    # viewer buffer name is stored in its window record
    ed.rmargin = rmargin # assign viewer panel rmargin to current buffer
    # restore_window calls restore_buffer with bufname found in window record
    # must save editor window focus first
    saved_focus = fr.focus # restore fr.focus in oe()
    fr.restore_window(vkey) # viewer window, assigns fr.width etc.
    shell.width = fr.width # for formatting ls and man output to fit in viewer
    render.width = fr.width # for formatting web pages

def oe():
    """
    Switch focus from viewer back to same previous editor buffer and window.
    """
    if not viewer_focus():
        print('? editor panel already has focus\r\n', end='')
        return
    # save_window calls save_buffer
    fr.save_window(vkey) # viewer window bufname etc. may change, not geometry    ed.save_buffer()
    # restore_window calls restore_buffer
    fr.restore_window(saved_focus) # editor focus saved in ov()
    ed.rmargin = fr.rmargin # assign editor panel rmargin to current buffer 
    shell.width = fr.width # for formatting ls and man output to fit in editor
    render.width = fr.width # for formatting web pages
    
def vwin():
    """
    Create empty viewer panel in the frame to the right of the editor windows.
    then populate viewer panel with restored viewer border and  window contents.
    This function requires that edsel win() has already been called to
    set whole frame's vertical dimensions and editor panel width in left side.
    When this fcn is called, edsel current window must be in left side panel.
    This fcn fits viewer panel into space remaining to right of editor panel.
    so editor panel ed.width determines new viewer panel width.
    Then in the viewer panel makes a new viewer buffer the ed current buffer,
     and makes a new viewer window the edsel current window and displays it.  
    """
    global leftedge, width, rmargin, viewer_displayed
    if viewer_displayed:
        print('? viewer window is already displayed\r\n', end='')
        return
    leftedge = fr.width + 1 # left edge viewer panel
    start_col = leftedge + 2  # Where viewer window text begins 
    width = fr.termcols - fr.width - 2 # width of viewer window text
    rmargin = width - 4 # sked uses width - 8, but viewer is narrower
    shell.width = width # for formatting ls and man output to fit in viewer
    render.width = width # for formatting web pages

    # Initialze viewer window record in edsel.windows.
    # Viewer window remains on the screen and its geometry never changes:
    #  start_col, width, wintop, wheight
    # Other items do change with editing: buftop, bufname, dot, point
    fr.windows[vkey] = { 'start_col': start_col, 'width': width,
                          'wintop': 1, 'wheight': fr.flines,
                          'buftop': 1, 'bufname': 'scratch.txt',
                          'dot':1, 'point': 0} 
    # Now make viewer window the current window and display it.
    ov()
    viewer_displayed = True
    vrefresh() # calls update_status, which calls restore_cursor_to_cmdline
                          
def vclr():
    """
    Erase viewer window contents including border and status line.
    """
    global viewer_displayed
    if not viewer_displayed:
        print('? viewer panel is not displayed\r\n', end='')
        return
    if not viewer_focus():
        print('? viewer window does not have focus\r\n', end='')
        return
    for iline in range(fr.flines): # 0 indexed, clear status line also
        display.put_cursor(iline + 1, leftedge) # terminal lines 1 indexed
        display.kill_line()
    display.put_cursor(fr.tlines, 1) 
    oe()
    del(fr.windows[vkey])
    viewer_displayed = False
    
# Disable editor functions that don't or shouldn't work in viewer window
# 'from viewer import *' in the REPL replaces edsel fcns with these

def o2():
    'Disable editor function that does not work in viewer window'
    if viewer_focus():
        print("? can't split viewer window\r\n", end='')
        return
    fr.o2()

# FIXME?  # C-x o does *not* map to on() in this module, nor does any other key
# Instead C-x o maps to edpanel_key which calls oe or fr.on
def on():
    'Disable editor function that does not work in viewer window'
    if viewer_focus():
        print("? only one viewer window\r\n", end='')
        return
    fr.on()

def o1():
    'Disable editor function that does not work in viewer window'
    if viewer_focus():
        print("? already only one viewer window\r\n", end='')
        return
    fr.o1()

def refresh():
    if viewer_focus():
        vrefresh()  # refresh viewer panel including border
    else:
        fr.refresh() # refresh current window in editor panel

# Run commands in viewer window while focus remains in current editor window.
  
def viewer_window(cmd):
    """
    Execute cmd in viewer window if present.  Editor window keeps focus.
    Must be able to use the same cmd in editor window or viewer window.
    """
    if not viewer_displayed: # run cmd in editor window
        cmd()
    elif viewer_focus(): # run cmd in viewer window
        cmd()
    else: # switch to viewer window just to run cmd, return focus to editor
        ov()
        cmd()
        oe()            
     
def vvrefresh():
    'Refresh viewer panel. Editor window keeps focus if it has it.'
    viewer_window(refresh)

def vv():
    'Scroll viewer window down.  Editor window keeps focus if it has it.'
    viewer_window(fr.v)
    
def vrv():
    'Scroll viewer window up.  Editor window keeps focus if it has it.'
    viewer_window(fr.rv)

def vl():
    'Next line in viewer window.  Editor window keeps focus if it has it.'
    viewer_window(fr.l)

def vrl():
    'Previous line in viewer window.  Editor window keeps focus if it has it.'
    viewer_window(fr.rl)

def vtop():
    'Top of buffer in viewer window.  Editor window keeps focus if it has it.'
    viewer_window(lambda: fr.p(1))

def vbottom():
    'Bottom of buffer in viewer window.  Editor window keeps focus if it has it.'
    viewer_window(lambda: fr.p(ed.S()))

def N():
    """
    Show *Buffers* list in viewer window, without .html .htxt web buffers.
    Editor window keeps focus if it has it.
    """
    viewer_window(render.N)

def W():
    """
    Show *Buffers* list in viewer window, showing only .htxt web buffers. 
    Editor window keeps focus if it has it.
    """
    viewer_window(render.W)

# Console functions
# Overwrites console function names imported by 'from console import *'
# You can still invoke console.sh('...') etc. by proviing console.  prefix
# viewer_window cmd must have no args - use lambda to absorb args into cmd

def sh(cmd):
    viewer_window(lambda: console.sh(cmd))

def cd(path):
    viewer_window(lambda: console.cd(path))
    
def pwd():
    viewer_window(console.pwd)
    
def ls(path='.'):
    viewer_window(lambda: console.ls(path))

def lsl(path='.'):
    viewer_window(lambda: console.lsl(path))
    
def lslt(path='.'):
    viewer_window(lambda: console.lslt(path))
    
def man(topic):
    viewer_window(lambda: console.man(topic))

def help(topic):
    viewer_window(lambda: console.help(topic))

            
# Browser functions
# Overwrites browser function names imported by 'from browser import *'
# You can still invoke browser.grx() etc. by providing browser. prefix

# Browser get and render,  gr() with exception handler
#  that displays traceback in *Errors* buffer in viewer window.
# This replaces gr() defined in render.py that has simpler exception handler.

def print_traceback(traceback_string):
    """
    Print lines from multiline tb_string returned by traceback.format_exc.
    Works with redirect_stdout to our text buffers.
    Imitates code in our python/pyhelp.py and unix/shell.py
    """
    for line in traceback_string.splitlines():
        print(line)

def gr(url):
    'Get and Render web page at url'
    render.gr_tb = 'No traceback' # must reinitiazlie each time
    try:
        get.g(url)
        render.r(url)
    except BaseException as e:
        render.gr_tb = traceback.format_exc() # returns string, does not print tb
        # print(render.gr_tb) # for now, just print it wherever cursor is
        viewer_window(lambda: redirect('*Errors*', 
                                lambda: print_traceback(render.gr_tb), 
                                'Traceback from render.gr(): '))
 
def grx(this_window):
    """
    Get and Render web page at URL eXtracted from current line in current buffer.'
    Display page in current (usually viewer) window if this_window == True
    Display page in editor window if this_window == False
    """
    # Must get URL from current (viewer) buffer 
    #  before editor_window() changes to editor buffer
    url = get.xurl(ed.buffer[ed.dot])
    if url: # url is '' if not URL found on line
        if this_window: # viewer window
            gr(url) # use gr in this module with its exception handler
        else:            
            editor_window(lambda: gr(url))
    
def grfx(this_window):
    """
    Get and Render web page at next Footnote eXtracted from current line.
    If viewer has focus, display that web page in the current editor buffer.
    """
    # Must get footnote and URL from current (viewer) buffer 
    #  before editor_window() changes to editor buffer
    n = get.fnrefnum() # n is next footnote on current line, or 0 if none
    if n:
        url = get.fnurl(n) # url at footnote n, or '' if footnote n not found
        if this_window: # viewer window
            gr(url)
        else:            
            editor_window(lambda: gr(url))

def hnpage(item_number):
    'Get the HN item (page) with the given integer (not string) item number'
    gr(render.hnitem + str(item_number))
      
# Functions invoked by keycodes - conditional depending on viewer state

def vclr_key(): # C-x 1
    if viewer_focus():
        vclr() # delete viewer window
    else:
        fr.o1()  # on editor panel: delete other window, one remains

def edpanel_key(): # C-x o
    if viewer_focus():
        oe()  # switch from viewer panel to editor window
    else:
        fr.on() # on editor panel: switch to other editor window

def file_key(): # C-x C-f
    """
    Imitates dmacs find_file
    """
    filename = dmacs.request('Find file: ')
    if dmacs.cancelled(filename): return
    dmacs.mark = 0
    e(filename) # use correct file load fcn (above) for viewer or editor window

# vdir has been moved from this viewer module to pmacs module

def buffer_key(): # C-x b
    """
    Imitates dmacs switch_buffer
    """
    response = dmacs.request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    b(response) # use correct buffer selection fcn for viewer or editor window

# Functions invoked in editor window by keycode in viewer window

def editor_window(cmd):
    """
    Execute cmd in editor window if viewer has focus.  Editor gets focus.                                                        
    """
    if not viewer_displayed: # run cmd in editor window
        cmd()
    elif not viewer_focus(): # run cmd in editor window
        cmd()
    else: # switch to editor window to run cmd
        oe()
        cmd()
        # ov() return focus to viewer - NOT! editor keeps focus

def loader(this_window):
    """
    Load contents indicated by the current line in the buffer.
    The current line might be a buffer name, file name, or directory name.
    If current line names a buffer, show the buffer contents in a window.
    If the current line names a file, load the file into a buffer and display
    it in a window.  If the current line names a directory, display 
    it in the viewer window.    
    If this_window == True, load contents into the current window,
     usually the viewer window.
    If this_window == False, load contents into the other window,
     an editor window
    """
    #print(f'In loader, this_window: {this_window}') # DEBUG
    #breakpoint() # DEBUG
    if ed.bufname == '*Buffers*' or ed.bufname == '*WebPages*':
        # All lines in *Buffers* have same format so this should always work
        # Code based on sked.py select_buffer():
        # Get the buffer name from the current (viewer) window
        # buffer name starts in col 1, continues to first space, can be any length.
        bname = ed.buffer[ed.dot][1:].partition(' ')[0]
        # Load the buffer into a window.
        if this_window: # usually viewer window
            fr.b(bname)
        else: # other window, an editor window
            editor_window(lambda: fr.b(bname))
    elif ed.bufname == '*Console*':
        # Get file name from the current (viewer) window
        # File name is from ls -l command, word at 0-based index 8 on line
        # Not all lines in *Console* are from ls -l so we must check format
        words = ed.buffer[ed.dot].split()
        # Check if line is dir listing line: 9 words starting with permissions
        if len(words) == 9 and set(words[0]).issubset(set('drwx-')):
            permissions = words[0]
            fname = words[-1]
            if permissions[0] != 'd': # This line does *not* name a directory
                # Load the selected file into a window.
                # fname is just file basename, must prefix directory path
                if this_window: # viewer window
                    fr.e(shell.lspath + '/' + fname)
                else: # other window, an editor window
                    editor_window(lambda: fr.e(shell.lspath + '/' + fname))
            else: # This line names a directory
                #  List the selected directory in the viewer window
                # print(f'{fname} is a directory') # DEBUG
                # This call to lsl updates shell.lspath to add this directory
                # display directory list in current window, usually viewer
                # FIXME: M_o on subdirectory line prints subdirectory at bottom 
                #  of viewer window (right) BUT moves cusor to editor (wrong)
                # Always display directory in viewer window, ignore this_window
                lsl(shell.lspath + '/' + fname) # selecting fname ../ works too
        else: 
            pass # Line is not in ls -l format. FIXME? print msg in REPL             
    # FIXME?  Following sections always display in current window
    elif get.xurl(ed.buffer[ed.dot]): # There is a URL on this viewer line
        # Get and render web page from URL on viewer line.
        # NB: grx redundantly calls get.xurl again
        grx(this_window) # This is viewer.grx defined here, not get.grx
    elif get.fnrefnum(): # There is a footnote on this viewer line
        # Get and render web page from footnote on viewer line.
        # NB: grfx redundantly calls get.frnrefun again
        grfx(this_window) # This is viewer.grfx defined here, not get.grfx
    else:
        pass # Possibly more cases to come
 
# save_reload() with exception handler
#  that displays traceback in *Errors* buffer in viewer window.
# This replaces save_reload() in dmacs.py that has simpler exception handler.

def save_reload():
    'Write out buffer, reload module, so file and module stay consistent.'
    dmacs.sr_tb = 'No traceback' # must reinitiazlie each time
    try:
        fr.w()
        dmacs.reload_buffer() # synchronization?  Does w() finish before reload() begins?
    except BaseException as e:
        dmacs.sr_tb = traceback.format_exc() # returns string, does not print tb
        # print(sr_tb) # for now, just print it wherever cursor is
        viewer_window(lambda: redirect('*Errors*', 
                                lambda: print_traceback(dmacs.sr_tb), 
                                'Traceback from save_reload(): '))

# Next, sys.excepthook: catch-all handler for exceptions not handled elsewhere

# DEBUG All global so we can inspect in REPL
type = None
value = None
tb = None
tb_no = 0
tb_str = ''
tb_list = []

def print_traceback_list(traceback_list):
    """
    Print lines from multiline tb_list returned by traceback.format_exception
    Works with redirect_stdout to our text buffers.
    Imitates code in our python/pyhelp.py and unix/shell.py
    """
    for line in traceback_list:
        print(line)
   
def traceback_window(type_arg, value_arg, tb_arg): # don't shadow traceback module
        global type, value, tb, tb_no, tb_str, tb_list
        type = type_arg
        value = value_arg        
        tb = tb_arg
        tb_no += 1
        tb_list = traceback.format_exception(type_arg, value_arg, tb_arg)
        tb_str = ''.join(tb_list) + '\n\n' # extra blank lines at the bottom
        viewer_window(lambda: redirect('*Errors*', 
                                lambda: print_traceback(tb_str),
                           'Traceback printed by Piety custom sys.excepthook'))
        dmacs.terminal.set_line_mode() # restore echo after crash
         
sys.excepthook = traceback_window
   
# DEBUG for testing excepthook
def crash(): 1/0
def deep_crash(): crash()
dmacs.keymap[key.C_z] = deep_crash 
                                 
dmacs.keymap[key.C_x + '3'] = vwin
dmacs.keymap[key.C_x + '1'] = vclr_key # if viewer_focus: vlcr() else: fr.o1()
dmacs.keymap[key.C_x + '2'] = o2 # o2 in this module, not fr.o2
dmacs.keymap[key.C_x + 'v'] = ov
# C-x o does *not* map to on() in this module, nor does any other key
# Instead C-x o maps to edpanel_key which calls oe in this module  or fr.on
dmacs.keymap[key.C_x + 'o'] = edpanel_key
dmacs.keymap[key.C_l] = refresh

# Cursor motion in viewer window, while editor window has focus
dmacs.keymap[key.C_t] = vv # scroll page down
dmacs.keymap[key.M_t] = vrv # scroll page up
dmacs.keymap[key.M_n] = vl  # next line
dmacs.keymap[key.M_p] = vrl # prev ine
dmacs.keymap[key.M_lp] = vtop  # top of buffer
dmacs.keymap[key.M_rp] = vbottom # bottom of buffer

# Refresh viewer window while editor window has focus
dmacs.keymap[key.M_m] = vvrefresh

# Always display *Buffers* list in viewer window
# Overwrites C_x C_b key binding defined in dmacs.py
dmacs.keymap[key.C_x + key.C_b] = N # local N above, not edsel.N

# Save and reload buffer 
dmacs.keymap[key.C_x + key.C_r] = save_reload # local save_reload above

# Visit file, prompt for file name, NOT like Emacs, but analogous to C-x b
# NOT!  We'll just stick to emacs keycodes when there is one.
# dmacs.keymap[key.C_x + 'f'] = dmacs.find_file

# Visit file, prompt for file name, compatible with Emacs
dmacs.keymap[key.C_x + key.C_f] = dmacs.find_file

# Prompt for directory (default cwd) then display file list in viewer window
# This assignment is not needed here - new vdir is defined in pmacs.py
# and C_x d is assigned in pmacs.keymap there.
#pmacs.keymap[key.C_x + 'd' ] = vdir # pmacs keymap, use pmacs.request
 
# Load contents named on line into this window, usually the viewer
dmacs.keymap[key.C_o ] = (lambda: loader(this_window=True))

# Load contents named on line into other widow, usually an editor window
dmacs.keymap[key.M_o] = (lambda: loader(this_window=False))

# C-x C-b - list buffers without webpages, C-x C-w list .html buffers
dmacs.keymap[key.C_x + key.C_b] = N # N defined above, not edsel.N or browser.NM
dmacs.keymap[key.C_x + 'w' ] = W # W defined above, not browser.W 
  
def quit():
    """
    Ask for confirmation, then exit Piety and Python.
    Clear the viewer window and restore full screen scrolling.
    """
    unsaved = ed.unsaved()
    if unsaved:
        print('These buffers have unsaved content:')
        print(' '.join(unsaved))          
        answer = input(
'Are you SURE you want to quit Piety and Python, losing all unsaved work? ')
    else:
        answer = input('Are you SURE you want to quit Piety and Python? ')
    if not answer.lstrip()[0] in ('yY'): return
    if viewer_displayed: vclr() # clear viewer panel
    fr.clr()  # restore full screen scrolling
    exit() # exit python
 
