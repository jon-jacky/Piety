
frame.py
========

**frame.py** manages a multiwindow display implemented by list of
*window* instances, with a scrolling command region below the windows
at the bottom of the display.

**frame.py** provides the display for the *edsel* and *eden* display
editors.

**frame.py** does not require any particular application program to be
present (it does not import *ed*, *edsel*, or any others), so it can
act as a display server to any application (or several).  In fact,
different programs can simultaneously use different windows on the
same display.  So *frame* can act as a text-only tiling window
manager.

Programs update the window arrangement and the contents of windows
by calling the *frame.update* function.

The *frame* module provides functions and data but no classes.  We
expect there will only be a single frame instance in a session, so a
module suffices.

In this version of *frame*, the display always shows a vertical stack of
windows (or one window).  It is only possible to split a window
horizontally, not vertically.

Revised Mar 2018
