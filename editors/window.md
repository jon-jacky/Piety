
window.py
=========

**window.py** defines the *Window* class for line-oriented display editors.

Each window displays a range of lines (a segment) of a text buffer.

Each window includes a final status line with information about its contents.

Window contents are not stored in *Window* objects, only in text buffers.
*Window* methods render buffer contents directly to the display.

All updates from the *window* module
involve a whole line or group of lines from a buffer.
Updates within a line are handled by the *console* or *edsel* modules,
which use the *display* module to write and update that line,
directly on the display, without using this *window* module.
Or, updates within a line might even be handled by the Python
built-in function *input*, which also writes directly to the display.
The line being edited by *console*, *edsel*, or the Python *input* function 
is not yet part of a buffer so it cannot be handled by the *window* module.

This module attempts to avoid rewriting lines that are already
up-to-date on the display, that have been put there already by
previous updates from the *window* module, or have been put there by the
*console* or *edsel* modules or the Python *input* function.  Therefore some
methods only update the lines below the lines where insertions and
deletions occur: they might have to be moved down or up after
insertions or deletions.

Revised Feb 2020
