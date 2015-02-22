
vt_terminal
===========

This directory contains Python modules for running terminal
applications on a VT-100 compatible terminal, whose keyboard sends
ASCII control codes and ANSI control sequences, and whose display
responds to ANSI control sequences.  Most terminal emulator programs
such as *xterm* are VT-100 compatible.

To run terminal applications on a VT-100 compatible terminal, put this
directory on the PYTHONPATH.  To run on a different kind of terminal,
put modules with the same module names and the same function names in
a different directory with a different name (*framebuffer* for
example) and put that directory on the PYTHONPATH instead.

Revised February 2015
