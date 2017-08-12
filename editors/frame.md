
frame.py
========

**frame.py** manages a multiwindow display implemented by list of
*window* instances, with a scrolling command region below the windows
at the bottom of the display.

**frame.py** provides the display for the *edsel* and *eden* display
editors.  It could provide the display for other programs also.
In fact, different programs can simultaneously use different windows
on the same display.  So *frame* can act as a text-only tiling window
manager.

Programs update the window arrangement and the contents of windows by
calling the *update* function in the *updatecall* module to pass an
*UpdateRecord* to the *update* function in *frame*.  This has the
effect of uncoupling application programs such as *edsel* from
*frame*.  Now *frame* does not require any particular application
program to be present (it does not import any), so it can act as a
display server to any application (or several).  Likewise, application
programs do not import *frame*, but only import *updatecall*, so they
could send updates to a different display server.  The *UpdateRecord*
is defined independently of any particular application or display server.

Here *edsel* imports *updates* (which defines *UpdateRecord*) and
*updatecall* (which sends the record), but *frame* only imports
*updates*.  We  separate *updatecall* from *updates* to avoid circular
imports with *frame*.

Updates are processed synchronously.  An *UpdateRecord* is not a
completely self-contained description of a display update; it refers
to locations in the buffer associated with a window.  So, if window
updates are not synchronized with buffer updates, window
contents could become inconsistent.

The *frame* module provides functions and data but no classes.  We
expect there will only be a single frame instance in a session, so a
module suffices.

In this version of *frame*, the display always shows a vertical stack of
windows (or one window).  It is only possible to split a window
horizontally, not vertically.

Revised Aug 2017
