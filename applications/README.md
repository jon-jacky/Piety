
applications
============

Miscellaneous applictions:


Sample applications to run under the Piety scheduler, and some library
modules they use.  Applications include a Python shell, two editors,
and a file writer.  For directions, see the docstrings in each module,
and the *.md* files.  Each application can be run from its *main*
method: *python ed.py* etc.  Additional tests and demonstrations are
under *Piety/tests* and *Piety/scripts*.

To be a *Piety* application, a program must provide all of if its
functionality in one or more *handlers* that can be called by the Piety
scheduler.  Each handler must complete its work quickly, then exit.
The handlers must not block waiting for input (or anything else).

To be a Piety *application*, a program must be self-contained: it must

- **writer.py**: write to files to demonstrate interleaving concurrency.

Revised February 2015
