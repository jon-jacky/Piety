
editors
=======

Text editors

- **frame.py**: Display editor that uses the same commands as *sked*.

- **frameinit.py**: Define and initialize global variables used by *frame*.

- **sked.py**: Line editor inspired by the classic Unix *ed*.

- **skedinit.py**: Define and initialize global variables used by *sked*.

## sked ##

Commands are just functions. To edit, call the functions from the Python REPL.
To begin editing without the display, start a Python session, then: import sked 
Then: from sked import *, to get function names into the REPL, so you can
use them without the sked module name prefix.

## frame ##

For each command in sked that produces no display output, there is
a command here in frame with the same name that produces display output.
There are also window commands win and clr that are not present in sked.

To turn on display editing, in the REPL: import frame, then:
from frame import *, then: win(24).  Here 24 is the number of lines
in the window, you can use another number.

To turn off display editing, in the REPL: clr(), then: from sked import *

Revised Apr 2023
