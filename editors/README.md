
editors
=======

Text editors, including a line editor inspired by the classic *Unix ed*, and a
    new display editor *edsel*:

- **buffer.py**: defines Buffer class used by *ed.py* and *edsel.py*

- **ed.md**: description of *ed.py*

- **ed.py**: line editor inspired by the classic Unix editor *ed*

- **ed.txt**: command summary for *ed.py*

- **edc.py**: *ed.py*, using the *command* and *key* modules from the
    *console* directory instead of Python *input*.  This configuration
    reads commmand lines and input lines without blocking, one
    character at a time.

- **edsel.py**: display editor based on *ed.py*.

- **edsel.md**: description of *edsel.py*.

- **edselc.py**: *edsel.py*, using the *command* and *key* modules from the
    *console* directory instead of Python *input*.  This configuration
    reads commmand lines and input lines without blocking, one
    character at a time.

- **line5.txt, line20.txt**: sample text files for experimenting with
    the editor.

- **window.py**: defines Window class used by *edsel.py*

Revised May 2016
