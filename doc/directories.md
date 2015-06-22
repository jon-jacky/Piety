
Piety directories
=================

The Piety repository is organized into these directories:

- **applications**: miscellaneous applications.

- **asyncio**: Non-blocking event loop using Python 3 *asyncio*, used
   by *piety.run*.  An alternative to *select* (below).

- **bin**: shell scripts that configure Piety for Unix-like platforms.

- **console**: modules used by terminal applications, including a pure
    Python non-blocking alternative to *readline* and *input*.

- **doc**: notes and documents.

- **editors**: a line editor inspired by the classic Unix *ed*, and a
    new display editor *edd*.

- **piety**: defines *Task*, *Job*, *Session*, *schedule*, and *run*
    (the non-blocking event loop).  This is the core of the Piety
    operating system.

- **scripts**: Python scripts that run applications as tasks or jobs
    under a non-blocking event loop

- **select**: Non-blocking event loop using Unix *select*, used by *piety.run*.
   An alternative to *asyncio* (above).

- **shell**: Python shell, *pysh*.

- **test**: shell scripts and modules that test code in other
     directories.

- **unix**: modules for running Piety on a Unix-like host.
     We may add directories for other platforms in the future.

- **vt_terminal**: modules for running Piety terminal applications on
    a VT-100 compatible terminal or terminal emulator program (for
    example *xterm*).  We may add directories for other terminal types in
    the future.

Each directory contains a *README* file with more information.
Another page explains the [rationale](modules.md) for this organization.

Revised June 2015

