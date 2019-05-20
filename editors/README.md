
editors
=======

Text editors, including a line editor *ed.py* and a display editor *edsel*.

There are several editors here, a series of experiments beginning with *ed.py*
and culminating in *edsel*.  We expect to use *edsel* most of the time, but are
keeping the intermediate experiments as well.

The main steps in the sequence of increasing functionality are:
*ed.py* (line editor), *edie* (adds built-in Python interpreter),
*edo* (adds Python interpreter and
scripting), *edda* (adds display, but still provides only *ed* commands for
line editing), and *edsel* (adds display editing at any character position).

Another dimension arises from wrapping these programs in a
[Console](../console/README.md) object that collects input without blocking,
so they can run in the cooperative multitasking system,
[Piety](../piety/README.md).  Here *etty* wraps *ed*, *edna* wraps *edo*,
and *desoto* wraps *edda*.  *edsel* is already a *Console* object,
so it doesn't require a wrapper.

Several of the programs and modules here are described by
their own *.md* and *.txt* files (*ed.md* and *ed.txt* for *ed.py*, etc.)

Files in this directory:

- **buffer.md**: description of *buffer.py*.

- **buffer.py**: defines *Buffer* class used by *ed.py*.

- **check.py**: check command line arguments and provide default
    argumentss for *ed.py*.

- **desoto.py**: defines the *edda* *Console* job that wraps the *edda.py*
  display editor, along with the *wyshka* enhanced Python shell and
  *samysh* script execution.  Contrast to the *edda.py* *main* function.

- **ed.md**: description of *ed.py*.

- **ed.py**: line editor inspired by the classic Unix editor *ed*.

- **ed.txt**: command summary for *ed.py*

- **edda.md**: description of *edda.py*.

- **edda.py**: simple display editor based on the line editor *ed.py*
  with the *edo* enhancements.

- **edda.txt**: command summary for *edda.py*.

- **edie.py**: run *ed.py* line editor along with *wyshka* enhanced shell.
  contrast to *ed.py* and *edo.py*.

- **edna.py**: defines the *ed* *Console* job that wraps *edo.py* (the *ed.py*
  line editor, along with the *wyshka* enhanced Python shell and
  *samysh* script execution).  Contrast to the *edo.py*.

- **edo.md**: description of *edo.py*.

- **edo.py**: run *ed.py* line editor along with *wyshka* enhanced
  shell and *samysh* script execution.  Use Python builtin *input()*
  to collect and edit input lines with blocking.  Contrast to *ed.py*,
  *edie.py*, and *edna.py*.

- **edsel.md**: description of *edsel.py*.

- **edsel.py**: display editor based on *edda* and *ed.py*.

- **etty.md**: description of *etty.py*.

- **etty.py**: wraps *ed.py* in a *Console* object
  that uses non-default keymaps to make the terminal behave
  like an old-fashioned teletype. Contrast to *ed.py*
  *main* function and *edna*.

- **frame.md**: description of *frame.py* and *updates.py*

- **frame.py**: multiwindow display implemented by list of *window*
   instances, with a scrolling command region at the bottom of the
   display.  Used by *edda* *desoto* and *edsel*.

- **lines5.txt, lines20.txt, lines40.txt, lines120.txt**: sample text
    files for experimenting with the editor.

- **parse.py**: command line parsing for *ed.py*.

- **updates.py**: define display operations enumeration *Op*.

- **view.py**: defines variables that are used by *ed*, *edda*,
   *desoto* and *edsel*, to
   configure code in *ed* to run with or without a display.

- **window.py**: defines Window class used by *frame*.

Revised May 2019
