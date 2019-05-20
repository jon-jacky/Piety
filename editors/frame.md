
frame.py
========

**frame.py** manages a multiwindow display implemented by list of
*window* instances, with a scrolling command region below the windows
at the bottom of the display.

**frame.py** provides the display for the *edda* and *edsel* display
editors.

**frame.py** provides *update*, the only function that applications
  call to update the arrangement and contents of the windows.  The
  first argument of *update* is a value of the *Op* enumeration
  defined in the *updates* module, that specifies which update
  operation to perform.  The remaining arguments are keyword arguments
  that provide the parameters of the update.

**frame.py** does not require any particular application program to be
present (it does not import *ed*, *edda*, or any others), so it can
act as a display server to any application (or several).  In fact,
different programs can simultaneously use different windows on the
same display.  So *frame* can act as a text-only tiling window
manager.

**frame.py** provides functions and data but no classes.  We
expect there will only be a single frame instance in a session, so a
module suffices.

The present version of *frame* always shows a vertical stack of
windows (or one window).  It is only possible to split a window
horizontally, not vertically.

Revised Mar 2018
