
Piety bin directory
=====================

This directory contains shell scripts that configure Piety for
various platforms.

To conveniently use Piety, this directory should be on your execution
*PATH*.  Or, its contents should be installed in some directory that
is on your execution *PATH*.  See *paths* in this directory:

- **paths**: assigns paths for running Piety on a Unix-like host with 
  a VT-100 compatible terminal.  To configure
 Piety, execute this script, or put the commands from this script into
 your *.profile* or *.bashrc*. 

- **twisted_paths**: similar to *paths*, except it adds the *twisted* 
  directory instead of the *select* directory to the *PYTHONPATH.  Use
  this command instead of *paths* to use the Twisted event loop instead
  of the usual Piety event loop based on Unix *select*.

Revised January 2015
