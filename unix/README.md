
unix
====

This directory contains Python modules for running Piety on a
Unix-like host operating system (including Linux and Mac OS X).

To run Piety on a Unix-like host operating system, put this directory
on the PYTHONPATH.  To run on a different kind of host, put modules
with the same module names and function names in a different directory
with a different name (*windows* for example) and put that directory
on the PYTHONPATH instead.

### Files ####

- **shell.py** - Python functions that wrap shell commands, so you can invoke
                the shell without exiting the Python session or using
                the host desktop.
                
- **terminal.py** - functions to set terminal character mode or line mode,
                       read/write a single character or a string.
                       
- **terminal_util.py** - function to get terminal dimensions: number of
                        lines, columns.
 
Revised Mar 2025

