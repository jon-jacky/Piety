
bin
===

Shell scripts that configure Piety on Unix-like platforms.

Put this directory on your execution *PATH*.  Or, install its contents
in some directory that is on your *PATH* (for details, see *paths* in
this directory).

To select a Piety configuration, execute one of the following
scripts, or put the commands from the script into your *.profile* or
*.bashrc*:

- **paths**: assigns paths for running Piety on a Unix-like host with
  a VT-100 compatible terminal and the event loop based on *select*.

- **asyncio_paths**: similar to *paths*, except it puts the *asyncio* 
  directory instead of the *select* directory on the *PYTHONPATH*.  Use
  this command instead of *paths* to use the *asyncio* event loop instead
  of the event loop based on Unix *select*.

Revised June 2015
