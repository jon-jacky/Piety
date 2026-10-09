"""
aedsel.py - Adapt our edsel editor to run in an asyncio event loop.  
            Define the asyncio reader function aedrun that handles each editor
            keystroke.  Define the function aed to resume the aedsel editor
            from the Piety shell command prompt (after first running the aed.py
            script to load the editor modules and create the initial window).
            Then define ed() to call edsel.ed() when event loop is not running
            and aedsel.aed() when event loop is running - so just typing ed()
            in the REPL always does the right thing.
""" 

import terminal, key, display, edsel, pyshell, apyshell

def aed():
   """
   aed() calls the edsel editor from the piety shell prompt in the asycio event loop.
   After this the editor responds to emacs keys.  Type M-x to return to the shell.
   """ 
   pyshell.cmd_mode = False
   edsel.setup()

# Make it so we can always type ed() whether or not eventloop is running.
def ed():
    if edsel.eventloop.piety.is_running():
        aed()
    else:
        edsel.ed()
 
def aedrun():
    """
    Run each time sys.stdin detects a new character 
    Call edsel runcmd, check for exit
    """
    c = terminal.getchar() # not blocking, asyncio calls aedrun when char is ready
    edsel.runcmd(c) # assigns running = False to exit
    if not edsel.running:
        pyshell.cmd_mode = True
        edsel.restore() # calls restore_cursor_to_cmdline
        display.next_line() # these 3 lines copied from pyshell.runcmd key.cr case
        pyshell.cmd = ''
        pyshell.point = 0
        pyshell.setup() # prints prompt and refreshes command line

# handler function  moved here from eventloop, to break import loop with pmacs
def handler():
    if pyshell.cmd_mode:
        apyshell.apysh() # async shell
    elif edsel.resprunning:
        edsel.runrequest()  # prompt/request/response
    else:
        aedrun()  # async display editor foreground job       
