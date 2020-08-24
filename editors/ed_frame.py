"""
ed_frame.py - wrap functions in ed.py to update display

"""

import ed, frame

# Save a reference to each of these before we reassign them.
# This is necessary to restore unwrapped fcns, also to break infinite recursion.
ed_l = ed.l
ed_p_lines = ed.p_lines
ed_prepare_input_mode = ed.prepare_input_mode
ed_set_command_mode = ed.set_command_mode

# define wrapped functions
    
def prepare_input_mode(cmd_name, start, end):
    ed_prepare_input_mode(cmd_name, start, end) # not ed.prepare_input_mode
    frame.input_mode()

def set_command_mode():
    ed_set_command_mode()
    frame.command_mode()

# Enable/disable display by assigning/restoring wrapped/uwrapped fcns in ed

def enable():
    'Enable display by assigning wrapped functions in ed'
    ed.l = ed.l_noprint
    ed.p_lines = ed.p_lines_noprint
    ed.prepare_input_mode = prepare_input_mode
    ed.set_command_mode = set_command_mode

def disable():
    'Disable display by restoring unwrapped functions in ed'
    ed.l = ed_l
    ed.p_lines = ed_p_lines
    ed.prepare_input_mode = ed_prepare_input_mode
    ed.set_command_mode = ed_set_command_mode

