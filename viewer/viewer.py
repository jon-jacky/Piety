"""
viewer.py  - Experiments with a viewer window beside the editor windows

The viewer has its own current buffer and its own window that are always
displayed and always available, which are implicitly selected by the 
commands (functions) defined in this module.

The editor current buffer and windows managed by the sked and edsel
modules, and the commands that use them, are unchanged, always
available, and work just as before.
"""

import key, dmacs, display, shell, render, console, sked as ed, edsel as fr
 
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
    Show *Buffers* list in viewer window.  Editor window keeps focus if it has it.'
    Overwrites N identifer imported from edsel.N() by 'from edsel import *'
    You can still invoke edsel.N() by providing edsel. prefix: edsel.N()
    """
    viewer_window(fr.N)

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
                
def buffer_key(): # C-x b
    """
    Imitates dmacs switch_buffer
    """
    response = dmacs.request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    b(response) # use correct buffer selection fcn for viewer or editor window

dmacs.keymap[key.C_x + '3'] = vwin
dmacs.keymap[key.C_x + '1'] = vclr_key
dmacs.keymap[key.C_x + 'v'] = ov
dmacs.keymap[key.C_x + 'o'] = edpanel_key
dmacs.keymap[key.C_l] = refresh

# Cursor motion in viewer window, while editor window has focus
dmacs.keymap[key.C_t] = vv
dmacs.keymap[key.M_t] = vrv
dmacs.keymap[key.M_n] = vl
dmacs.keymap[key.M_p] = vrl
dmacs.keymap[key.M_lp] = vtop
dmacs.keymap[key.M_rp] = vbottom

# Refresh viewer window while editor window has focus
dmacs.keymap[key.M_m] = vvrefresh

# Always display *Buffers* list in viewer window
# Overwrites C_x C_b key binding defined in dmacs.py
dmacs.keymap[key.C_x + key.C_b] = N # local N above, not edsel.N
     
