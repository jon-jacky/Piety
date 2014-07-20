"""
edv - visual ui for ed
"""

from __future__ import print_function # for redirection

import ed
import ansi
import traceback

class Window(object):
    def __init__(self, first, last):
        "First, last are line numbers of top, bottom of command window"
        self.first = first
        self.last = last

    def update(self):
        "Print the stored response"
        #print ('update: %s' % self.response) #DEBUG
        if self.response:
            print('%s' % self.response)

command_first = 22
command_last = 24
command_window = Window(command_first, command_last)
print(ansi.decstbm % (command_first, command_last)) # set scrolling region
print(ansi.cup % (command_last, 1)) # put cursor at bottom

def update_windows():
    "Update all windows, top to bottom"
    command_window.update()

def ed_cmd(command):
    "Placeholder for ed.ed_cmd"
    #print('ed_cmd: %s' % command) # DEBUG
    if command == 'foo':
        command_window.response = '? error message'
    elif command == 'bar':
        command_window.response = 'status message'
    else:
        command_window.response = ''

def edv_cmd(command):
    """
    Process ed command, update display.
    This is is the commmand function passed to Piety Console constructor
    """
    # print output from ed_cmd is redirected to various buffers
    # status messages and error messages are redirected to command_window
    # ed.ed_cmd(command) # FIXME comment out for now
    ed_cmd(command) # DEBUG - use this placeholder for now
    update_windows()

def edv():
    """
    Top level edv command to invoke from python prompt or command line
    Won't cooperate with Piety scheduler, it calls blocking command raw_input
    """
    cmd = '' # anything but 'q', must replace 'q' from previous quit
    while not cmd == 'q':
        cmd = raw_input() # blocking. no prompt - maybe make prompt a parameter
        try:
            edv_cmd(cmd) # non-blocking
        except BaseException as e:
            print(ansi.decstbm_all) # restore full-screen scrolling
            print(ansi.cup % (command_last,1)) # put cursor at bottom
            traceback.print_exc() # looks just like unhandled exception
            exit()
    print(ansi.decstbm_all)
    print(ansi.cup % (command_last,1))

# Run the editor from the system command line: python edv.py
if __name__ == '__main__':
    edv()

