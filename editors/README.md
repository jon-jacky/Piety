
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

- **ed_command.py**: run *ed.py* editor, use *command* and *key* modules instead
  of Python *input()* to get command line.  But do not use *Command* class
  to specialize terminal behavior for modes.  Contrast to *etty.py*.

- **edsel.py**: display editor based on *ed.py*.  Uses Python *input()*
  to collect and edit command lines and inserted text lines.

- **edsel.md**: description of *edsel.py*.

- **edsel_command.py**: run *edsel* editor, use *command* and *key* modules
  instead of Python *input()* to get command line.  But do not use
  *Command* class to specialize terminal behavior for modes.  Contrast
  to *eden.py*.

- **etty.py**: line editor based on *ed.py*.  Uses command* and *key*
  modules to collect and edit command lines and inserted text lines.
  Uses *Command* class to specialize terminal behavior for modes.
  Uses keymaps to provide retro printing-terminal-style
  in-line editing and history.  Contrast to *ed_command.py*.

- **line5.txt, line20.txt**: sample text files for experimenting with
    the editor.

- **window.py**: defines Window class used by *edsel.py*

Revised October 2016
