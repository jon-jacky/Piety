
textframe.py
============

The *textframe* module joins the storage modules *text* and *buffer* to
the display module *frame* so that changes to the text update the display.
The *text* and *buffer* modules themselves do not update the display, in
order to keep them simple and flexible, and so they can be used by programs
like *ed.py* that do not use the display.

The *textframe* module wraps functions in *text* and methods in *buffer*
(and also a few functions in *ed.py*) to call display code in *frame*.
The display editor *edda* (which is used by *edsel*) imports and uses
*textframe*.

The *textframe module provides an *enable* function that turns on display
updates and a *disable* function that turns them off.

The storage modules could be adapted to a different display scheme than
*frame* by writing a similar wrapper module.

- *NOTE*: In the current version, the *textframe enable* and *disable*
  functions are not completely effective. *Buffer* instances created
  when the display is disabled do not update the display even after
  *enable*, and instances created when the display is enabled continue to
  update even after *disable*.   We have not yet decided on the best way
  to fix this.

Revised Oct 2020

  

