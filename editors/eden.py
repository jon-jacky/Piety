"""
eden.py - run *edsel.py* display editor, with additional screen
 editing commands, see eden.md.  Use *console* module instead of
 Python builtin *input* to collect and edit input lines.  Contrast
 to *edsel.py* *main* function and *edselc.py*.
"""

import edc, edsel, console as con

c_command, buf, dot = False, None, 0

# This do_command implements the additional screen editing commands
# described in eden.md
def do_command(chars):
    'Handle new eden commands here, pass other commands to edsel'
    global c_command, buf, dot
    chars = chars.lstrip()

    # command mode, 'c' with no address range, c(hange) just one line
    if edsel.ed.command_mode and chars == 'c':
        c_command = True
        buf = edsel.ed.buf
        dot = buf.dot
        console.initline = buf.lines[dot].rstrip() # strip \n at eol
        console.initpoint = 0
        # FIXME ed.cmd_name is gone, and edsel no longer imports ed.
        edsel.ed.cmd_name = 'c' # needed by edsel functions, following
        edsel.ed.command_mode = False 
        win = edsel.frame.win
        edsel.display.put_cursor(win.wline(dot), 1)
        # FIXME shouldn't the preceding two lines call Op.input like this:
        # buf.dot -= 1 # compensate for wdot+1 in frame Op.input
        # edsel.update(edsel.Op.input)
        # No, doesn't quite work because Op.input calls win.update_for_input

    # inline c command finished, assign updated line and update
    elif not edsel.ed.command_mode and c_command:
        buf.lines[dot] = console.command.line + '\n'
        edsel.ed.command_mode = True
        c_command = False    
        buf = edsel.ed.buf
        edsel.update(edsel.Op.command)

    # pass all other commands to edsel
    else:
        edsel.do_command(chars)

console = con.Console(prompt=':', do_command=do_command,
                      stopped=(lambda command: edsel.ed.quit),
                      mode=edc.ed_command_mode,
                      specialmodes=edc.ed_specialmodes)

# In ed x command use eden do_command here that calls edsel.do_command 
#  which calls edsel.update_display
edsel.ed.x_cmd_fcn = do_command

def main():
    if not edsel.frame.windows: # initialize first window only once
        edsel.frame.init(edsel.ed.buf, cmd_h_option=12) # edsel inits ed.buf
    edsel.startup(c=12)
    console.run()
    edsel.cleanup()

if __name__ == '__main__':
    main()
