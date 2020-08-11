"""
ed_frame.py - wrap functions in ed.py to update display

"""

import ed, frame

# save a reference to each of these before we reassign them
ed_prepare_input_mode = ed.prepare_input_mode
ed_set_command_mode = ed.set_command_mode
    
def prepare_input_mode(cmd_name, start, end):
    ed_prepare_input_mode(cmd_name, start, end)
    frame.input_mode()

def set_command_mode():
    ed_set_command_mode()
    frame.command_mode()

