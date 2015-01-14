
Piety vt_terminal directory
===========================

This directory contains Python modules for running Piety on a VT-100
compatible terminal, whose keyboard sends ASCII control codes and ANSI
control sequences, and whose display responds to ANSI control
sequences.  Most terminal emulator programs such as *xterm* are VT-100
compatible.

To run Piety on a VT-100 compatible terminal, put this directory
on the PYTHONPATH.  To run on a different kind of terminal, put modules
with the same names in a different directory with a different name
(*framebuffer* for example) and put that directory on the PYTHONPATH
instead.

Revised January 2015
