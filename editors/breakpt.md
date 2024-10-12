
breakpt
=======

The *breakpt* function here makes it possible to use *Pdb* to debug the display
editor *pmacs* while it is running.

To use the debugger, type the command *import breakpt* in the interactive 
Python REPL.   Then edit the module that contains the code you want to debug --
typically *edsel.py*. At the point in the code where you want to enter the
debugger, add a call to the builtin function *breakpoint*. Then reload that
module. 

Perform some editing operation that uses the code you want to debug.
When execution reaches the call to *breakpoint*, the cursor leaves the
display window and moves to the scrolling REPL region at the bottom of the 
terminal.  The debugger prompt *(Pdb)* appears there.  Now you can type
*pdb* commands.   When you are finished using the debugger, Type the *pdb*
*c* (continue) command.   The debugger exits and the program resumes
running normally.   The cursor moves back up into the display window.

For example, debug the function *erase_bottom* in *edsel.py*.   This
function erases lines that may be left over after the end of the buffer at the
bottom of a window, after some editing operation makes the buffer shorter.
This function is short and simple, so of course we got it wrong at first
-- we omitted wintop from the first line of code in the function body.
We put a call to *breakpoint* in this function, which is now commented out.

To see this code work while editing in *pmacs*, put the cursor in a window and
scroll down to the end of the buffer so there are some
empty lines at the bottom of the window. The file *test/lines40.txt* is good
for this because it is easy to tell which lines have been deleted and moved.
Delete a few lines near the end of the buffer with *C-k* (kill line) or *C-w*
(cut). Notice that the lines following the deletion move up, leaving more empty
lines at the bottom of the window.

Activate our *breakpt* function by typing the command *import breakpt* 
in the Python REPL.

Now edit *edsel.py*, find the function *erase_bottom*, and uncomment the 
line with *breakpoint()* by removing the comment characters *#* from the 
beginning of the line.   Reload *edsel.py* by typing *C-x C-r* (reload).

Once again, put the cursor in a window and scroll down to the end of the
buffer, leaving some empty lines at the bottom of the window.   Delete
some lines near the end of the buffer.   The remaining lines at the end
move up, but they also remain at the end of the window -- they are not 
erased, because the breakpoint comes before the code that erases them.

The cursor moves to the scrolling REPL.  The debugger runs, prints the location
of the breakpoint in the code, and prints the prompt:

    > /home/jon/Piety/editors/breakpt.py(43)breakpt()
    -> pdb.set_trace() # Enter Pdb debugger, use Pdb commands until Pdb c (continue)
    (Pdb)    

Type the debugger command *w* (where) to print the function call stack:

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
Then we type *p* (print) commands to show the variable values.  See the
code for the meaning of these values.

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

Now type the *c* (continue) command to exit the debugger, move the cursor
back up into the window, and resume running the program normally:

    (Pdb) c
    
However, the window contents do not update correctly, because the cursor
does not return to the correct location in the window, so subsequent code
does not have the intended effect.  The code does not record the location
of the cursor when the debugger is activated, so this is the best we can do.
Type the refresh command *C-l* to restore the correct window contents.

Revised Oct 2024

