
window.py
=========

**window.py** defines the *Window* class for line-oriented display editors.

Each window displays a range of lines (a segment) of a text buffer.

Each window includes a final status line that shows the name of the
buffer that the window is displaying, the location of the segment
in the buffer, and other information.

Window contents are not stored in *Window* objects, only in text buffers.
*Window* methods render buffer contents directly to the display.
*Window* objects only store the location of the window on the display,
and the location of the window's segment (displayed lines) in the buffer.

In the present version, *Window* objects only store the vertical location 
of the window. All windows are aligned on the left edge of the display.
The display shows a vertical stack of windows (or one window).

All updates from the *window* module involve a whole line or sequence of 
lines from a buffer. Updates within a line are handled by the *console* or 
*edsel* modules, which use the *display* module to write and update that 
line, directly on the display, without using this *window* module. Or, 
updates within a line might even be handled by the Python built-in 
function *input*, which also writes directly to the display. The line 
being edited by *console*, *edsel*, or the Python *input* function  is not 
yet part of a buffer so it cannot be handled by the *window* module.

This module attempts to avoid rewriting lines that are already up-to-date 
on the display, that have been put there already by previous updates from 
the *window* module, or have been put there by the *console* or *edsel* 
modules or the Python *input* function.  

More than one window might be visible at the same time, showing different 
buffers or different segments (locations) in  the same buffer.    There is 
always one window called the *focus* window, which contains the line 
called *dot* where the the user's typing is inserted, and where many 
commands take effect.

In the typical situation where the user types line after line into  the 
focus window, dot moves down toward the bottom of the window after each 
line,  and all the lines above dot remain unchanged.  Only the lines below 
dot need to be rewritten as they are all pushed down (or up after a line 
is deleted).  When dot reaches the bottom of the window, the entire window 
is rewritten to scroll dot up to the middle of the window.

When a buffer's  contents change, all the windows for that buffer  might 
update.   There are different methods for  updating the focus window and 
the other  windows.   The focus  window must always be updated such that 
dot remains  within the window as the user edits at dot or moves dot 
around in the buffer, but we attempt  to minimize updates to other 
windows  for that same buffer.   A non-focus window might partially or 
totally overlap with text inserted or deleted at dot; in those  cases the 
minimal number of lines in that window are changed. It is typical 
to place a window at a location far from dot, so its contents should 
remain unchanged while editing at dot or moving dot.  If  a window's 
segment does not contain any  changed lines, no lines in the window  need 
to be updated.  However,  the location of the window's segment within the 
buffer may change due to insertions  or deletions at dot,  even when 
lines within  the segment do not change.  In that case, the window's 
status line must change because it shows the segment's location.

The focus window contains a visible *cursor* at dot to indicate where 
typed text is inserted or deleted, when the editing session is in an 
insert mode.  In other modes, the focus window contains a *marker* to 
indicate dot, the line where many commands take effect.  In these other modes,
the cursor is in the command line in the scrolling command region.
The marker always appears in column 1, but the cursor may appear in any
column.  The other windows do not show a cursor nor a marker.

Managing multiple windows, including creating, deleting, positioning, and 
sizing windows, selecting the focus window, keeping track of the editing 
mode, and placing the cursor and  the marker, is controlled from the 
*frame* module, which calls methods in this module.  The *frame* module 
calls appropriate methods for each window,   depending on whether that 
window is the focus window.

Applications that use multiple windows should call functions in *frame*
(not in the *window* or *display* modules) to update the display.

Revised Feb 2020
