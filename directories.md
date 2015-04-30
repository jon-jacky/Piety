
Piety directories
=================

The Piety repository is organized into these directories:

- **applications**: miscellaneous applications.

- **bin**: shell scripts that configure Piety for Unix-like platforms.

- **console**: modules used by terminal applications, including a pure
    Python non-blocking alternative to *readline*.

- **doc**: notes and documents.

- **editors**: a line editor inspired by the classic Unix *ed*, and a
    new display editor *edd*.

- **scheduler**: modules that define and schedule tasks, jobs, and
    sessions.  This is the core of the Piety operating system.

- **scripts**: Python scripts that run applications as tasks or jobs
    under the Piety sheduler or other schedulers (such as Twisted).

- **select**: event loop for running Piety on a Unix-like host,
    used by modules in the *scheduler* directory.  We may add directories 
    for other platforms in the future.

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
Another page explains the [rationale](doc/structure.md) for this organization.

Revised April 2015

