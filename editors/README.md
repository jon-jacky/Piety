
editors
=======

Text editors, including a line editor inspired by the classic *Unix ed*, and a
    new display editor *edsel*:

- **buffer.py**: defines Buffer class used by *ed.py* and *edsel.py*

- **ed.md**: description of *ed.py*

- **ed.py**: line editor inspired by the classic Unix editor *ed*
  Uses Python *input()* to collect and edit command lines and inserted
  text lines.

- **ed.txt**: command summary for *ed.py*

- **edc.py**: run *ed.py* line editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty.py*.

- **eden.py**: run *edsel.py* display editor, with additional screen editing 
  commands.  Use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *edselc.py*.

- **edsel.py**: display editor based on *ed.py*.  Uses Python builtin
  *input()* to collect and edit input lines.

- **edsel.md**: description of *edsel.py*.

- **edselc.py**: run *edsel.py* display editor, use *command*, *lineinput*, and
  *key* modules instead of Python builtin *input()* to collect and edit
  input lines.  Contrast to *edsel.py* *main* function and *eden.py*.

- **etty.py**: Run *ed.py* line editor, use *command*,
  *lineinput*, and *key* modules to collect and edit input lines.  Use
  non-default keymap with *Command* class to provide retro
  printing-terminal-style editing and history.  Contrast to *ed.py*
  *main* function and *edc.py*.

- **line5.txt, line20.txt**: sample text files for experimenting with
    the editor.

- **window.py**: defines Window class used by *edsel.py*

Revised October 2016
