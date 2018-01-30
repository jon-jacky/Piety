
Piety directories
=================

The Piety repository is organized into these directories:

- **applications**: small applications for demonstrating *piety.run*.

- **asyncio**: Non-blocking event loop using Python 3 *asyncio*, used
   by *piety.run*.  An alternative to *select* (below).

- **bin**: shell scripts that configure Piety for Unix-like platforms.

- **console**: modules used by terminal applications, including 
    one that defines the *Console* class, a wrapper that adapts
    a terminal application for cooperative multitasking.

- **doc**: notes and documents.

- **editors**: a line editor inspired by the classic Unix *ed*, and a
    new display editor *edsel*.

- **piety**: defines *Task*, *Job*, *Session*, and imports *eventloop*, 
  which defines *schedule* and *run*, the non-blocking event loop.
  This is the core of the Piety operating system.

- **scripts**: Python modules that test and demonstrate Piety,
    running applications as tasks or jobs with *piety.run*,
    or with simple blocking *while* loops.

- **select**: Non-blocking event loop using Unix *select*, used by *piety.run*.
   An alternative to *asyncio* (above).

- **shells**: Callable Python shells: *pysh*, a plain Python shell,
    *wyshka*, which can alternate between a Python shell and an 
    application shell, and *samysh*, which can execute commands 
    with an optional echo and delay.

- **test**: shell scripts and modules that test code in other
     directories.

- **unikernel**: an unfinished experiment to build a NetBSD Rumprun
    unikernel for running Piety.

- **unix**: modules for running Piety on a Unix-like host.
     We may add directories for other platforms in the future.

- **util**: miscellaneous utilities that are not
    platform-dependent or configuration-dependent, that are used by
    modules in more than one directory.

- **vt_terminal**: modules for running Piety terminal applications on
    a VT-100 compatible terminal or terminal emulator program (for
    example *xterm*).  We may add directories for other terminal types in
    the future.

Each directory contains a *README* file with more information.
Another page explains the [rationale](doc/modules.md) for this organization.

Revised Jan 2018
