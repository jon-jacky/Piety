
breakpt
=======

The *breakpt* module defines and assigns a *breakpoint hook* that
makes it possible to use *Pdb* to debug the display editor *pmacs* while it
is running, without disturbing its window contents.

We do not use the debugger much in Piety.  We always have the Python REPL 
available, so invoking functions and examining global variables is usually 
sufficient to reveal what the code is doing.  But sometimes it is helpful
to examine the local variables within functions, and we need the debugger for that.
Our *breakpt* makes it easy to use the debugger in our usual workflow, without
interruping the editor in a long-running Python session.

To use the debugger, type the command *import breakpt* in the interactive 
Python REPL.   Then edit the module that contains the code you want to debug.
At the point in the code where you want to enter the
debugger, add a call to the builtin function *breakpoint*. Then reload that
module. 

Perform some editing operation that uses the code you want to debug.
When execution reaches the call to *breakpoint*, the cursor leaves the
display window and moves to the scrolling REPL region at the bottom of the 
terminal.  The debugger prompt *(Pdb)* appears there.  Now you can type
*pdb* commands. When you are finished using the debugger, type the *pdb* *c*
(continue) command. The debugger exits and the cursor moves back up into the
display window. The program resumes running normally. 

For example, debug the function *erase_bottom* in *edsel.py*.   This
function erases lines that may be left over after the end of the buffer at the
bottom of a window, after some editing operation makes the buffer shorter:

    def erase_bottom():
        """
        Erase any old lines left over between end of buffer and bottom of window.
        Leave cursor after last line erased.  Do not update any globals.
        """
        nlines = (wheight-1) - (wline(ed.dot)-wintop) # n of lines to window status line
        nblines = ed.S() - ed.dot  # n of lines to end of buffer
        nelines = nlines - nblines # n of empty lines at end of window
        ### breakpoint() # DEBUG Uncomment this line for breakpoint demo.  See breakpt.md.
        erase_lines(nelines) # Make empty lines at end of window.

This function is short and simple, so of course we got it wrong at first. We
thought we could find the error if we could see the values of the local
variables *nlines*, *nblines*, and *nelines*. So we put in a call to
*breakpoint* after all three were assigned, and ran the code by editing in a
buffer until we hit the breakpoint. In the debugger, we saw that the value
of *nlines* was negative -- obviously wrong! We realized we had forgotten to
subtract *wintop*. We exited the debugger, and in that same editor session
we immediately corrected the code, commented out the breakpoint, and ran the
code again to confirm the correction worked.

Here are more details about this fix:

To see this code working correctly, put the cursor in a window and scroll
down to the end of the buffer so there are some empty lines at the bottom of
the window. The file *test/lines40.txt* is good for this because it is easy
to tell which lines have been deleted and moved. Delete a few lines near the
end of the buffer with *C-k* (kill line) or *C-w* (cut). The lines following
the deletion move up, leaving more empty lines at the bottom of the window.

Activate our *breakpt* function. While display editing, type *M-x* to get to
the Python REPL. At the Python prompt, type the statement *import breakpt*.
Then type the function call *pm()* to return to display editing.

Now edit *edsel.py*, find the function *erase_bottom*, and uncomment the 
line with *breakpoint()* by removing the comment characters *#* from the 
beginning of the line.   Reload *edsel.py* by typing *C-x C-r* (reload).

Once again, put the cursor in a window and scroll down to the end of the
buffer, leaving some empty lines at the bottom of the window.   Delete
some lines near the end of the buffer.   This causes execution to reach
the breakpoint.  The remaining lines near the end of the window
move up, but the same lines also remain below them at the end of the window
They are not erased, because the breakpoint comes before the code that
erases them.

When execution reaches the breakpoint, the cursor moves from the window to
the scrolling REPL. The debugger runs, prints the location of the breakpoint
in the code, and prints the *(Pdb)* debugger prompt:

    > /home/jon/Piety/editors/breakpt.py(43)breakpt()
    -> pdb.set_trace() # Enter Pdb debugger, use Pdb commands until Pdb c (continue)
    (Pdb)    

Type the debugger command *w* (where) to print the function call stack:

    (Pdb) w
    ...
    ... other functions ...
    ...
    -> ed.d(start, end, append, display_d)
      /home/jon/Piety/editors/sked.py(410)d()
    -> move_dot(new_dot)
      /home/jon/Piety/editors/edsel.py(245)display_d()
    -> erase_bottom()
      /home/jon/Piety/editors/edsel.py(119)erase_bottom()
    -> breakpoint() # DEBUG Uncomment this line for breakpoint demo.  See breakpt.md.
    > /home/jon/Piety/editors/breakpt.py(43)breakpt()
    -> pdb.set_trace() # Enter Pdb debugger, use Pdb commands until Pdb c (continue)
    (Pdb) 
    
This shows that execution has stopped in our *breakpt* function, at the 
statement *pdb.set_trace()*.  We want to examine the local variables in 
*erase_bottom*, so we type the debugger command *u* (up) to move up the stack.
Then we type several *p* (print) commands to show the variable values.  See the
code for the meaning of these values:

    (Pdb) u
    > /home/jon/Piety/editors/edsel.py(119)erase_bottom()
    -> breakpoint() # DEBUG Uncomment this line for breakpoint demo.  See breakpt.md.
    (Pdb) p nlines
    9
    (Pdb) p nblines
    1
    (Pdb) p nelines
    8
    (Pdb)     

These all appear to be correct -- we fixed the error already.  Before we fixed
the error, *nlines* was negative number.

Now type the *c* (continue) command to exit the debugger, move the cursor
back up into the window, and resume running the program normally:

    (Pdb) c
    
However, the window contents do not update correctly, because the cursor
does not return to the correct location in the window, so subsequent code
does not have the intended effect.  The code does not record the location
of the cursor when the debugger is activated, so this is the best we can do.
Type the refresh command *C-l* to restore the correct window contents.

After running this demonstration, be sure to return to the *erase_bottom*
function in the *edsel.py* buffer again to comment out the *breakpoint()*
call. Otherwise, you will hit the breakpoint again every time you delete
lines from any buffer.

After we hit a breakpoint, we can use debugger commands to examine the stack,
move up and down the stack, and examine local variables in each function
call on the stack, all without disturbing window contents. However, it is
not useful to step through code.  Statements that send commands
to update the display window will not work as intended, because the cursor
is not in the window, it is in the scrolling REPL region.  The commands will
merely scramble the REPL region, rendering it illegible.

Revised Oct 2024

