
frame.py
========

**frame.py** manages a multiwindow display implemented by list of
*window* instances, with a scrolling command region below the windows
at the bottom of the display.

**frame.py** provides the display for the *edda* and *edsel* display
editors.

**frame.py** provides functions that client programs such as *edda*
and *edsel* can call to manage windows or update window contents.
Applications that use multiple windows should call functions in *frame*
(not in the *window* or *display* modules) to update the display.

**frame.py** does not require any particular application program to be
present (it does not import *edda*, *edsel*, or any others), so it can
act as a display server to any client application (or several).
Different programs can simultaneously use different windows on the
same display.  So *frame* can act as a text-only tiling window
manager.

More than one window might be visible at the same time, showing different 
buffers or different locations in  the same buffer.   When a buffer's 
contents change, all the windows for that buffer  might update.  There is 
always one window called the *focus* window, which contains the line 
called *dot* where the the user's typing is inserted, and where many
commands take effect.

There are different methods for  updating the focus window and the other 
windows.   The focus  window must  be updated such that dot always remains 
within the window, but we attempt  to minimize updates to other windows.

The focus window contains a visible *cursor* at dot to indicate where 
typed text is inserted or deleted, when the editing session is in an 
insert mode. In other modes, the focus window contains a *marker* to 
indicate dot, the line where many commands take effect.  In these other modes,
the cursor is in the command line in the scrolling command region.
The other windows do not show a cursor nor a marker.

The *frame* module maintains the editing *mode*. The *mode* variable is 
*Mode.command* when executing commands typed on the command line, and 
*Mode.display* or *Mode.input* when entering/editing text in a display 
window. It is possible to edit buffers and manage windows from the 
command line, so display window contents can change a lot in 
*Mode.command*.

In *Mode.command*, the terminal cursor where the user types input is in 
the command region at the bottom of the display, so we display the 
*marker* in the focus window to show where commands will take effect. 
The marker appears in the focus window at the first character of the line 
where insertion occurs, *dot*. In *Mode.display* and *Mode.input*, the 
marker is not displayed, because instead the terminal cursor where the 
user types input appears in the focus window at *point*, the character 
position where insertions occur.  The marker always appears in column 1,
but the cursor can appear in any column.

**frame.py** manages multiple windows,  including creating, deleting, 
positioning, and  sizing windows, selecting the focus window, keeping 
track of the editing mode, and placing  the cursor and  the marker. 
*frame.py* achieves its effects by calling  methods  and functions in the 
*window* and *display* modules. *frame*  calls appropriate methods for 
each window,   depending on whether that  window is the focus window.

**frame.py** provides functions and data but no classes.  We
expect there will only be a single frame instance in a session, so a
module suffices.

The present version of *frame* always shows a vertical stack of
windows (or one window).  It is only possible to split a window
horizontally, not vertically.

Revised Feb 2020
