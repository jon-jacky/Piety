"""
pyshell.py - Custom Python REPL that uses our editline instead of builtin input.

We need this to support tasking.  It enables other tasks writing to
the terminal to interleave with typing characters at our REPL, and enables us
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
import pmacs

from pycall import pycall # uses Python library code.InteractiveConsole
 
cmd = '' # Python command
point = 0 # index of cursor in cmd
continuation = False  # True when Python continuation line expected

ps1 = '>> '  # first line prompt, different from CPython >>>
ps2 = '.. '  # continuation line prompt
prompt = ps1 # initally.  prompt is global so we can inspect it in the REPL.
start_col = 3 # index of start of cmd on line, allowing for prompt ps1 or ps2

# prompt and continuation are global so we can read them in the REPL

history = [''] # list of command strings, most recent at index 0
i_cmd = -1 # integer index into history, code will assign to 0 or greater
max_cmds = 100 # maximum number of commands in history.  20 is not enough!
  
# cmd_mode is needed to restore terminal cursor after it is used by a task. 
cmd_mode = True  # True in Python REPL, False when editing in display window.

def tpm():
    """
    tpm "tasking pmacs"
    From the pysh Python REPL, use the tpm() command to clear the cmd_mode flag
    and begin the pmacs editor for editing buffers display windows.
    Exit from display editing with M-x: set cmd_mode flag and return to REPL.
    tpm() must be issued from pysh REPL not standard Python REPL
    because it assumes terminal is already in char mode.
    """
    global cmd_mode
    cmd_mode = False
    pmacs.rpm() # raw pmacs - assumes terminal is already in char mode
    cmd_mode = True


def refresh_retrieved(cmd, point, start_col):
    """
    HACK replacement for el.refresh , for commands retrieved from history.
    For some reason we don't understand, el.refresh does not work correctly
    when applied to commands just retrieved fron history by C-p or C-n.
    It offsets the command text one character to the left, but puts the
    cursor at the intended location -- so inline editing doesn't work right.
    We compensate by putting +1 in the call to display.move_to_column.
    """
    display.move_to_column(start_col+1) # +1 to push cmd back to right place
    display.putstr(cmd.rstrip('\n')) # el.refresh has line not cmd
    display.kill_line() # remove any leftover text past line
    el.move_to_point(point, start_col)

def pysh():
    """
    Custom Python REPL that uses our editline instead of builtin input function
    so other tasks can interleave and we can restore cursor in Python cmd line.
    To exit pysh, type 'exit()' or ctrl-d.  'pysh' rhymes with fish.
    """
    global cmd, point, prompt, continuation, history, i_cmd
    terminal.set_char_mode()
    display.putstr(ps1) # >> prompt
    el.refresh(cmd, point, start_col) # following prompt on same line
    continuation = False # True when continuation line expected
    while True:
        c = terminal.getchar()
        k = keyseq.keyseq(c)
        if k: # keyseq returns '' if key sequence is not complete
            if k == key.cr:  # RET finishes entering cmd and runs Python cmd
                history.insert(0,cmd)
                if len(history) > max_cmds: history.pop()
                i_cmd = 0
                display.next_line()
                if cmd == 'exit()':  # Trap here, do *not* exit Python
                    cmd = ''  # otherwise cmd is exit() at next pysh() call...
                    point = 0 # ... and point is 5
                    break       
                else:
                    continuation = pycall(cmd) # Run the Python cmd
                    cmd = ''
                    point = 0
                    i_cmd = -1 # code will assign it to 0 or greater
                    prompt = ps2 if continuation else ps1
                    fr.restore_cursor_to_cmdline()
                    display.putstr(prompt)
                    el.refresh(cmd, point, start_col)
            elif k == key.C_d:  # ^D exits, alternative to 'exit()'
                cmd = ''  # no command on line
                point = 0
                break       
            elif k in (key.C_p, key.up):
                if i_cmd < len(history)-1: i_cmd += 1
                cmd = history[i_cmd]
                point = len(cmd)
                refresh_retrieved(cmd, point, start_col)
            elif k in (key.C_n, key.down):
                if i_cmd >= 0: i_cmd -= 1  # reaches -1 after most recent...
                if i_cmd < 0: cmd = ''   # ... then set cmd empty
                cmd = history[i_cmd]
                point = len(cmd)
                refresh_retrieved(cmd, point, start_col)
            else:
                cmd, point = el.runcmd(k, cmd, point, start_col) # edit cmd
    terminal.set_line_mode()
    print() # advance to next line for Python prompt

