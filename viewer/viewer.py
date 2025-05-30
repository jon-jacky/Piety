"""
viewer.py  - Experiments with a viewer window beside the editor windows

The viewer has its own current buffer and its own window that are always
displayed and always available, which are implicitly selected by the 
commands (functions) defined in this module.

The editor current buffer and windows managed by the sked and edsel
modules, and the commands that use them, are unchanged, always
available, and work just as before.
"""

import key, dmacs, display, shell, render, sked as ed, edsel as fr # frame
 
# Define and initialize global variables
# but only the *first* time this module is imported in a session.
# Then we can reload this module without re-initializing those variables,
# so we retain buffer contents and other state when we reload.
 
try:
    _ = leftedge # If this is already defined, this module was already imported.
except:
    # Defaults, some may be reassigned by vwin() below.
    leftedge = 81 # left edge, viewer border
    startcol = leftedge + 2 # where viewer text begins
    width = 64 # for 146 col Debian Linux console on Lenovo IdeaPad3 Chromebook
    rmargin = width - 4 # viewer panel rmargin
    buftop = 1 # line in buffer that appears at top of window
    bufname = 'scratch.txt' # viewer buffer name, key into ed.buffers
    dot = 1 # current line in ed.buffer where cursor is, text is inserted, etc.
    point = 1 # colum in current line where cursor is, text is inserted, etc.
    saved_dot = dot
    saved_point = point
    editor_bufname = ed.bufname
    viewer_displayed = False
    
def viewer_focus():
    'Return True when the viewer window has the focus'
    return viewer_displayed and fr.start_col > 1
    
def restore_viewer():
    """
    Restore viewer window dimensions to edsel current window.
    There is always just one viewer window that occupies entire frame height,
    so the vars are global here.  No need for a save_viewer, just one window.
    """
    fr.start_col = start_col  # assgined in vwin
    fr.width = width # assigned in vwin
    fr.wintop = 1 # viewer window always starts at top of terminal window
    fr.wheight = fr.flines # number of lines in entire frame
    fr.buftop = buftop

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

def vvrefresh():
    """
    Refresh viewer panel while using editor panel
    """
    if viewer_focus():
        print('? viewer window already has focus\r\n', end='')
        return 
    ov()
    vrefresh()
    oe()
   
def ov():
    """
    Switch focus from editor to viewer buffer and window.
    """
    global editor_bufname
    if viewer_focus():
        print('? viewer window already has focus\r\n', end='')
        return
    editor_bufname = ed.bufname # editor current buffer, must restore in oe()
    ed.save_buffer() 
    fr.save_window(fr.focus) # viewer does not change editor focus window.
    ed.restore_buffer(bufname, fr.print_nothing) # viewer bufname and buffer
    ed.rmargin = rmargin # assign viewer panel rmargin to current buffer
    restore_viewer() # viewer window, assigns fr.width etc.
    shell.width = fr.width # for formatting ls and man output to fit in viewer
    render.width = fr.width # for formatting web pages

def oe():
    """
    Switch focus from viewer back to same previous editor buffer and window.
    """
    global bufname
    if not viewer_focus():
        print('? editor panel already has focus\r\n', end='')
        return
    ed.save_buffer()
    bufname = ed.bufname # buffer we just saved
    ed.restore_buffer(editor_bufname, fr.print_nothing) # bufname saved in oe()
    ed.rmargin = fr.rmargin # assign editor panel rmargin to current buffer 
    fr.restore_window(fr.focus) # viewer did not change editor focus window
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
    global leftedge, start_col, width, rmargin, viewer_displayed
    if viewer_displayed:
        print('? viewer window is already displayed\r\n', end='')
        return
    leftedge = fr.width + 1 # left edge viewer panel
    start_col = leftedge + 2  # Where viewer window text begins 
    width = fr.termcols - fr.width - 2 # width of viewer window text
    rmargin = width - 4 # sked uses width - 8, but viewer is narrower
    shell.width = width # for formatting ls and man output to fit in viewer
    render.width = width # for formatting web pages
    
    viewer_displayed = True
    # Now make viewer window the current window and display it.
    ov()
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
    viewer_displayed = False
    
def v_display_restore_buffer(bname):
    """
    Copied, edited from edsel dsiplay_restore_buffer
    Display effect of ed restore_buffer function, fill entire window
    BUT do not update saved windows! viewer must not affect save editor windows..
    """
    ed.restore_buffer(bname, fr.print_nothing)
    # save_window_bufinfo() # NOT! viewer must not affect save editor windows
    fr.recenter()

def v_display_e(iline):
    """
    Copied, edited from edsel dsiplay_restore_buffer
    Display effect of ed e(dit) fcn: display new buffer contents around iline
    BUT do not update saved windows! viewer must not affect save editor windows.
    """
    ed.move_dot(iline)
    # save_window_bufinfo() # NOT! viewer must not affect saved editor windows
    fr.recenter()

def ve(fname):
    """
    Load and display file in viewer window.  Create buffer for loaded file.
    Based on sked e(), fixed so viewer window fcns don't affect editor windows.
    Fixes are hacks but we don't have to change code in sked.py or edsel.py.
    """
    if not viewer_focus():
        print('? viewer window does not have focus\r\n', end='')
        return 
    saved_prev_bufname = ed.prev_bufname
    ed.e(fname, v_display_e, v_display_restore_buffer) # assigns ed.prev_bufname
    ed.prev_bufname = saved_prev_bufname # *don't* save viewer window bufname

def vb(bname=None):
    """
    Restore and display buffer in viewer window. buffer already created by ve().
    Based on sked e(), fixed so viewer window fcns don't affect editor windows.
    Fixes are hacks but we don't have to change code in sked.py or edsel.py.
    """
    if not viewer_focus():
        print('? viewer window does not have focus\r\n', end='')
        return 
    saved_prev_bufname = ed.prev_bufname
    ed.b(bname, v_display_restore_buffer) # assigns ed.prev_bufname - shouldn't
    ed.prev_bufname = saved_prev_bufname # *don't* save viewer window bufname
        
def vv(nlines=None):
    """ 
    Scroll viewer window down, when current window is an editor window
    edsel v() should work in the viewer when viewer window is the current window.
    """
    if viewer_focus():
        print('? viewer window already has focus\r\n', end='')
        return 
    ov()
    fr.v()
    oe()

def vrv(nlines=None):
    """ 
    Scroll viewer window up, when current window is an editor window
    edsel rv() should work in viewer when viewer window is the current window.
    """
    if viewer_focus():
        print('? viewer window already has focus\r\n', end='')
        return 
    ov()
    fr.rv()
    oe()

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

def e(fname):
    'Disable editor function that should not be used in viewer window'
    if viewer_focus():
        print('? use ve(...) not e(...) in viewer window\r\n', end='')
        return
    fr.e(fname)

def b(bname=None):
    'Disable editor function that should not be used in viewer window'
    if viewer_focus():
        print('? use vb(...) not b(...) in viewer window\r\n', end='')
        return
    fr.b(bname)

# Functions invoked by keycodes - conditional depending on viewer state

def vwin_key(): # C-x 3
    if not viewer_displayed:
        vwin()  # display viewer window
    elif not viewer_focus():
        ov() # switch from editor panel to viewer window
            
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

def vrefresh_key(): # C-l
    if viewer_focus:
        vrefresh()  # refresh viewer panel including border
    else:
        fr.refresh() # refresh current window in editor panel

def file_key(): # C-x C-f
    """
    Imitates dmacs find_file
    """
    filename = dmacs.request('Find file: ')
    if dmacs.cancelled(filename): return
    dmacs.mark = 0
    if viewer_focus():
        ve(filename)
    else:
        fr.e(filename)
                
def buffer_key(): # C-x b
    """
    Imitates dmacs switch_buffer
    """
    response = dmacs.request(f'Switch to buffer (default {ed.prev_bufname}): ')
    if dmacs.cancelled(response): return
    dmacs.mark = 0 # But we don't reset mark when we change buffer by change window
    if viewer_focus():
        vb(response)
    else:
        fr.b(response)
               
dmacs.keymap[key.C_x + '3'] = vwin_key
dmacs.keymap[key.C_x + '1'] = vclr_key
dmacs.keymap[key.C_x + 'o'] = edpanel_key
dmacs.keymap[key.C_l] = vrefresh_key
dmacs.keymap[key.C_x + key.C_f] = file_key
dmacs.keymap[key.C_x + 'b'] = buffer_key

