
editors
=======

Text editors, including the line editor *ed.py* inspired by the
    classic *Unix ed*, and a new display editor *edsel*:

- **buffer.md**: description of *buffer.py*

- **buffer.py**: defines *Buffer* class used by *ed.py* and *edsel*

- **desoto.py**: run *edsel.py* display editor including *wyshka*
  enhanced shell and *samysh* script execution.  Use *console* module
  instead of Python builtin *input* to collect and edit input lines
  without blocking.  Contrast to *edsel* *main*.

- **ed.md**: description of *ed.py*.  REVISIONS STILL NEEDED

- **ed.py**: line editor inspired by the classic Unix editor *ed*.
  Uses Python builtin *input* to collect and edit command lines and inserted
  text lines.

- **ed.txt**: command summary for *ed.py*

- **edda.py**: run  *edo.py* line editor including *wyshka* enhanced shell
  and *samysh* script execution.  Use *console* module instead of
  Python builtin *input()* to collect and edit input lines.  Contrast
  to *ed.py* *main* function and *etty.py*.

- **eden.md**: description of *eden.py*.  REVISIONS MAY BE NEEDED.

- **eden.py**: run *edsel* display editor, with additional screen editing 
  commands.  Use *console* module instead of Python builtin *input* 
  to collect and edit
  input lines.  Contrast to *edsel* *main* function and *desoto*.
  MIGHT NOT WORK, WILL BE REVISED/FIXED IN THE FUTURE

- **edo.py**: *ed* + *wyshka*, *ed* with command interpreter that also
    provides Python + *samysh*, run script from buffer with optional
    echo and delay.

- **edsel.md**: description of *edsel.py*.  REVISIONS MAY BE NEEDED.

- **edsel.py**: display editor based on the line editor *ed.py* but
   import *edo*, *ed* + *wyshka* + *samysh* shell and scripting
   enhancements

- **edselc.py**: run *edsel* display editor, use *console*
  module instead of Python builtin *input* to collect and edit
  input lines.  Contrast to *edsel* *main* function and *eden*.
  MIGHT NOT WORK, ALREADY SUPERCEDED BY DESOTO.

- **etty.py**: run *ed.py* line editor, use *console*,
  module to collect and edit input lines.  Use
  non-default keymaps with *Command* class to provide retro
  printing-terminal-style editing and history.  Contrast to *ed.py*
  *main* function and *desoto*.  MIGHT NOT WORK.

- **frame.md**: description of *frame.py*, *updates.py*, and *updatecall.py*.

- **frame.py**: multiwindow display implemented by list of *window*
   instances, with a scrolling command region at the bottom of the
   display.  Used by *edsel*.

- **lines5.txt, lines20.txt, lines40.txt, lines120.txt**: sample text
    files for experimenting with the editor.

- **updatecall.py**: define function *update* to update display in
     *frame* by making and sending an *UpdateRec*.

- **updates.py**: define display operations *Op* and display update record 
  *UpdateRec* used to update display in *frame*.

- **window.py**: defines Window class used by *frame*

Revised December 2017
