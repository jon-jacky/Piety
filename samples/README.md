Piety samples
=============

Sample applications to run under the Piety scheduler.  For directions,
see the docstrings in each module, and the *.md* files.  Some tests are
under *Piety/tests*, some demonstrations are under *Piety/scripts*.

To be a Piety application, a program must provide all of if its
functionality in a *handler* that can be called by the Piety
scheduler.  (Or, in several different handlers.)  The handler must
complete its work quickly, then exit (return control to the Piety
scheduler).  The handler must not block waiting for input (or anything
else).

All of these programs provide such a handler.  Nevertheless, they are
all self-contained: they do not depend on the Piety scheduler, or on
any other Piety directories.  (That is, they do not import any Piety
scheduler modules or modules from other Piety directories).
Therefore, any of these applications could be moved out of the Piety
repository to other repositories.

The applications here can be run from the command line, without using
the Piety scheduler at all: *$ python <application>*.  In that
case, the application runs its *main* function, which replaces the
Piety scheduler with a loop that gets input using a blocking read
(usually *raw_input*), then passes it to the handler.  (The *main*
function is *not* the handler because it blocks waiting for input.)

Notes on some of the modules follow.

Shell application:

- **pysh.py**: callable Python shell.  It is in this directory because
*ed.py* and *edd.py* here use it.  It does not depend on any Piety scheduling
machinery, it is just another self-contained application.  Its
handler is returned by *mk_shell()*.  It has a *main* method.

Editor applications:

- **ed.py**: text editor inspired by the classic Unix editor *ed*.
  Its handler is *cmd*.  It has a *main* method.

- **edd.py**: display editor based on *ed.py*.  Its hander is *cmd*.
  It has a *main* method.

- **ed0.py**: library of functions and data structures used by *ed.py*
    and *edd.py*

- **ed.md**: description of *ed.py*

- **ed.txt**: command summary for *ed.py*

- **edd.md**: description of *edd.py*

Libraries:

- **ansi_display.py**: update terminal display using ANSI codes, used
    by *edd.py*

- **vt_keyboard.py**, **key.py**, **line.py**: support terminal
    keyboard input with history and editing, similar to Unix
    *readline*.  Can optionally be used with any terminal
    applications, including *pysh*, *ed*, and *edd*.  The applications
    do not import these modules, instead they are coordinated by the
    Piety *console* module.  See examples in the *scripts* directory.

Other:

- **writer.py**: write to files to demonstrate interleaving concurrency.
  Defines the *Writer* class, whose *write* method is the handler.
  It has a *main* function.

Revised Jan 2015
