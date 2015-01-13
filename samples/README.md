Piety samples
=============

Sample applications to run under the Piety scheduler, and the
libraries they use.  Applications include a Python shell, two editors,
and a file writer.  For directions, see the docstrings in each module,
and the *.md* files.  Each application can be run from its *main*
method: *python ed.py* etc.  Applications can also be run with a
wrapper that provides *readline*-like functionality in a nonblocking
interface to the Piety scheduler: *python edc.py* etc.  Additional
tests and demonstrations are under *Piety/tests* and *Piety/scripts*.

To be a *Piety* application, a program must provide all of if its
functionality in one or more *handlers* that can be called by the Piety
scheduler.  Each handler must complete its work quickly, then exit.
The handlers must not block waiting for input (or anything else).

To be a Piety *application*, a program must be self-contained: it must
not depend on the Piety scheduler, or on any other Piety directories.
(That is, it must not import any Piety scheduler modules or modules
from other Piety directories).  Therefore, any of these applications
can be used without Piety, and could be moved out of the Piety
repository to another repository.

The applications here can be run from the command line, without using
the Piety scheduler at all: *$ python ed.py* etc.  In that
case, the application runs its *main* function, which replaces the
Piety scheduler with a loop that gets input using a blocking read
(usually *raw_input*), then passes it to the handler.  (The *main*
function cannot be a Piety handler because it blocks waiting for input,
and does not exit quickly --- it takes over the Python session.)

This directory also contains the *command* module, which provides the
*Command* class, a wrapper to adapt terminal applications to the Piety
scheduler.  It also provides an example of each application wrapped
in a *Command* instance.  

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

- **terminal.py**: Set characteor or line mode, read and write single
   characters or strings with or without extra processing.  Used by
   *key.py* and *command.py*.  OS-dependent, only works on Unix-like systems.

- **vt_keyboard.py**: define symbolic names for ASCII characters and
    ANSI control sequences, used by *key.py* and *command.py*

- **key.py**: collect single-character keys and multi-character key
   sequences, such as as ANSI control sequences

- **ansi_display.py**: update terminal display using ANSI control
    sequences, used by *edd.py* and *command.py*

Wrapper:

- ***command.py**: provides the *Command* class, an interface to the
  Piety scheduler that provides *readline*-like functionality in a
  nonblocking interface to the Piety scheduler

Wrapped applications:

- **pyshc.py**: *pysh* Python shell wrapped in a *Command* instance.

- **edc.py**: *ed* line editor in a *Command* instance.

- **eddc.py**: *edd* line editor in a *Command* instance.

Revised Jan 2015
