
editors
=======

Text editors, including the line editor *ed.py* inspired by the
    classic *Unix ed*, a simple display editor *edsel*, and a more
    capable display editor *eden*.

There are several top-level editor programs here that can be invoked
from the system command shell or from the Python prompt.  These
programs have an onion-like structure where each program imports a
simpler program with fewer features, and adds a few features of its
own.  Ordered from the most features to the fewest, the editor
programs are:

- **Display editors**: *eden > desoto > edsel > edo > ed*

- **Line editors** with command line editing for display terminals: *edda > edo > ed*

- **Line editor** with command line editing teletype style: *etty > ed*

Files in this directory:

- **buffer.md**: description of *buffer.py*.

- **buffer.py**: defines *Buffer* class used by *ed.py*.

- **check.py**: check command line arguments and provide default
    argumentss for *ed.py*.

- **desoto.py**: defines the *edsel* *Console* job that wraps the *edsel.py*
  display editor, along with the *wyshka* enhanced Python shell and
  *samysh* script execution.  Contrast to the *edsel.py* *main* function.

- **ed.md**: description of *ed.py*.

- **ed.py**: line editor inspired by the classic Unix editor *ed*.
  Uses Python builtin *input* to collect and edit command lines and inserted
  text lines.

- **ed.txt**: command summary for *ed.py*

- **edda.py**: defines the *ed* *Console* job that wraps *edo.py* (the *ed.py*
  line editor, along with the *wyshka* enhanced Python shell and
  *samysh* script execution).  Contrast to the *edo.py* *main* function.

- **eden.md**: description of *eden.py*.

- **eden.py**: display editor based on *edsel* and *ed.py*.

- **edo.md**: description of *edo.py*.

- **edo.py**: run *ed.py* line editor along with *wyshka* enhanced
  shell and *samysh* script execution.  Use Python builtin *input()*
  to collect and edit input lines with blocking.  Contrast to *ed.py*
  *main* function and *etty.py*.

- **edsel.md**: description of *edsel.py*.

- **edsel.py**: simple display editor based on the line editor *ed.py*.
  Import *edo*, which runs *ed.py* along with *wyshka* enhanced
  shell and *samysh* script execution.  Use Python builtin *input()*
  to collect and edit input lines with blocking.

- **etty.md**: description of *etty.py*.

- **etty.py**: run *ed.py* line editor in a *Console*
  job to collect and edit input lines.  Use
  non-default keymaps with *Console* class to provide retro
  printing-terminal-style editing and history.  Contrast to *ed.py*
  *main* function and *edda*.

- **frame.md**: description of *frame.py*, *updates.py*, and *updatecall.py*.

- **frame.py**: multiwindow display implemented by list of *window*
   instances, with a scrolling command region at the bottom of the
   display.  Used by *edsel*.

- **lines5.txt, lines20.txt, lines40.txt, lines120.txt**: sample text
    files for experimenting with the editor.

- **parse.py**: command line parsing for *ed.py*.

- **updates.py**: define display operations enumeration *Op*.

- **view.py**: variables that are used by both *ed* and *edsel*, to
   configure code used by both programs to run with or without a
   display.

- **window.py**: defines Window class used by *frame*.

Revised Jan 2019
