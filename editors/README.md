
editors
=======

Text editors, including the line editor *ed.py* inspired by the
    classic *Unix ed*, and a new display editor *edsel*.

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

- **edda.py**: defines the *ed* *Console* job that wraps the *ed.py*
  line editor, along with the *wyshka* enhanced Python shell and
  *samysh* script execution.  Contrast to the *ed.py* *main* function
  and *etty.py*.

- **eden.md**: description of *eden.py*.  REVISIONS MAY BE NEEDED.

- **eden.py**: run *edsel* display editor, with additional screen editing 
  commands.  Use *console* module instead of Python builtin *input* 
  to collect and edit
  input lines.  Contrast to *edsel* *main* function and *desoto*.
  MIGHT NOT WORK, WILL BE REVISED/FIXED IN THE FUTURE.

- **edo.md**: description of *edo.py*.

- **edo.py**: run *ed.py* line editor along with *wyshka* enhanced
  shell and *samysh* script execution.  Use Python builtin *input()*
  to collect and edit input lines with blocking.  Contrast to *ed.py*
  *main* function and *etty.py*.

- **edsel.md**: description of *edsel.py*.

- **edsel.py**: display editor based on the line editor *ed.py*.
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

- **updatecall.py**: define function *update* to update display in
     *frame* by making and sending an *UpdateRec*.

- **updates.py**: define display operations *Op* and display update record 
  *UpdateRec* used to update display in *frame*.

- **window.py**: defines Window class used by *frame*

Revised Jan 2018
