"""
pyshell.py - Custom Python REPL that uses our editline instead of builtin input.

We need this to support tasking.  It enables other tasks writing to
the terminal to interleave with typing commands at our REPL, and enables us
to restore the cursor to the correct position in the command line after
another task moves it.

pyshell defines the pysh function, which is the actual custom REPL.
The module and the function have different names so we can 'import pyshell'
then 'from pyshell import pysh'  then 'reload pyshell' without name conflict.

'pyshell' is pronounced pie shell.  'pysh' rhymes with fish.
"""

import terminal, key, keyseq, display
import edsel as fr # fr for frame
import editline as el
from pycall import pycall # uses Python library code.InteractiveConsole
 
cmd = '' # Python command
point = 0 # index of cursor in cmd
continuation = False  # True when Python continuation line expected

ps1 = '>> '  # first line prompt, different from CPython >>>
ps2 = '.. '  # continuation line prompt
prompt = ps1 # initally.  prompt is global so we can inspect it in the REPL.
start_col = 3 # index of start of cmd on line, allowing for prompt ps1 or ps2

def pysh():
    """
    Custom Python REPL that uses our editline instead of builtin input function
    so other tasks can interleave and we can restore cursor in Python cmd line.
    'pysh' rhymes with fish.
    """
    global cmd, point, prompt, continuation # make global , we can read in REPL
    terminal.set_char_mode()
    display.putstr(ps1) # >> prompt
    el.refresh(cmd, point, start_col) # following prompt on same line
    continuation = False # True when continuation line expected
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.cr:  # RET finishes entering cmd and runs Python cmd
                display.next_line()
                # TK: Add cmd to history
                if cmd == 'exit()':  # Trap here, do *not* exit Python
                    cmd = ''  # otherwise cmd is exit() at next pysh() call...
                    point = 0 # ... and point is 5
                    break       
                else:
                    continuation = pycall(cmd) # Run the Python cmd
                    cmd = ''
                    point = 0
                    prompt = ps2 if continuation else ps1
                    # display.next_line() # displays extra blank line ...
                    fr.restore_cursor_to_cmdline() # ... use this instead
                    display.putstr(prompt)
                    el.refresh(cmd, point, start_col) # after prompt, same line
            # TK: elif C-p or C-n or up or down arrow, retrieve cmd from history
            else:
                cmd, point = el.runcmd(k, cmd, point, start_col)                    
    terminal.set_line_mode()
    print() # advance to next line for Python prompt

