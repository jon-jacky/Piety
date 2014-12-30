Piety samples
=============

Sample applications to run under the Piety scheduler.  For directions,
see the docstrings in each module, and the *.md* files.  Some tests are
under *Piety/tests*, some demonstrations are under *Piety/scripts*.

These applications are self-contained: they do not depend on modules
in any other Piety directories.  Any of these applications could be moved
out to their own repositories.

The *pysh* Python shell is in this directory because *ed* and 
*edd* here use it.  It does not depend on any Piety scheduling machinery,
it is just another self-contained application.

- **ed.py**: text editor inspired by the classic Unix editor *ed*

- **ed0.py**: functions and data structures used by *ed* and *edd*

- **ed.md**: description of *ed.py*

- **ed.txt**: command summary for *ed.py*

- **edd.py**: display editor based on *ed.py*

- **ansi_display.py**: update display using ANSI codes, used by edd.py

- **edd.md**: description of *edd.py*

- **pysh.py**: callable Python shell, used by ed.py and edd.py

- **writer.py**: write to files to demonstrate interleaving concurrency

Revised December 2014
