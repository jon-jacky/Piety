"""
apmacs.py - Adapt our pmacs Emacs-like editor to run in an asyncio event loop.  
            Define the asyncio reader function apmrun that handles each editor
            keystroke.  Define the function apm to resume the pmacs editor
            from the Piety shell command prompt (after first running the apm.py
            script to load the editor modules and create the initial window).
""" 

import terminal, key, display, pmacs, pyshell

def apm():
   """
   apm() calls the pmacs editor from the piety shell prompt in the asycio event loop.
   After this the editor responds to emacs keys.  Type M-x to return to the shell.
   """ 
   pyshell.cmd_mode = False
   pmacs.setup()
 
def apmrun():
    """
    Run each time sys.stdin detects a new character 
    Call pymacs runcmd, check for exit
    """
    c = terminal.getchar() # not blocking, asyncio calls apmrun when char is ready
    pmacs.runcmd(c) # assigns running = False to exit
    if not pmacs.running:
        pyshell.cmd_mode = True
        pmacs.restore() # calls restore_cursor_to_cmdline
        display.next_line() # these 3 lines copied from pyshell.runcmd key.cr case
        pyshell.cmd = ''
        pyshell.point = 0
        pyshell.setup() # prints prompt and refreshes command line


