Piety samples
=============

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
not depend on the Piety scheduler (it must not import modules from the
*piety* directory). Therefore, any of these applications can be used
without Piety, and could be moved out of the Piety repository to
another repository.

The applications here can be run from the command line, without using
the Piety scheduler at all: *$ python ed.py* etc.  In that
case, the application runs its *main* function, which replaces the
Piety scheduler with a loop that gets input using a blocking read
(usually *raw_input*), then passes it to the handler.  (The *main*
function cannot be a Piety handler because it blocks waiting for input,
and does not exit quickly --- it takes over the Python session until
the application exits.)

To run these applications with the Piety scheduler, use commands in
*Piety/scripts*.

Notes on some of the modules follow.

Shell application:

- **pysh.py**: callable Python shell.  It is in this directory because
*ed.py* and *edd.py* here use it.  It does not depend on any Piety scheduling
machinery, it is just another self-contained application.  Its
handler is returned by *mk_shell()*.  It has a *main* method.

Editor applications:

- **ed.py**: text editor inspired by the classic Unix editor *ed*.
  Its handler is *cmd*.  It has a *main* function.

- **edd.py**: display editor based on *ed.py*.  Its handlers are *cmd*,
  *init_display*, and *restore_display*.  It has a *main* function.

- **ed0.py**: library of functions and data structures used by *ed.py*
    and *edd.py*

- **ed.md**: description of *ed.py*

- **ed.txt**: command summary for *ed.py*

- **edd.md**: description of *edd.py*

Other applications:

- **writer.py**: write to files to demonstrate interleaving concurrency.
  Defines the *Writer* class, whose *write* method is the handler.
  It has a *main* function.

Libraries:

- **key.py**: collect single-character keys and multi-character key
   sequences, such as as ANSI control sequences.

Revised January 2015
