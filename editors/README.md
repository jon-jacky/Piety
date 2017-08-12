
editors
=======

Text editors, including the line editor *ed.py* inspired by the
    classic *Unix ed*, and new display editors *edsel* and *eden*:

- **buffer.md**: description of *buffer.py*

- **buffer.py**: defines *Buffer* class used by *ed.py* and *edsel*

- **ed.md**: description of *ed.py*

- **ed.py**: line editor inspired by the classic Unix editor *ed*.
  Uses Python builtin *input* to collect and edit command lines and inserted
  text lines.

- **ed.txt**: command summary for *ed.py*

- **edc.py**: run *ed.py* line editor, use *console*
  module instead of Python builtin *input* to collect and edit
  input lines.  Contrast to *ed.py* *main* function and *etty*.

- **eden.md**: description of *eden.py*.

- **eden.py**: run *edsel* display editor, with additional screen editing 
  commands.  Use *console* module instead of Python builtin *input* 
  to collect and edit
  input lines.  Contrast to *edsel* *main* function and *edselc*.

- **edsel.py**: display editor based on *ed.py*.  Uses Python builtin
  *input* to collect and edit input lines.

- **edsel.md**: description of *edsel.py*.

- **edselc.py**: run *edsel* display editor, use *console*
  module instead of Python builtin *input* to collect and edit
  input lines.  Contrast to *edsel* *main* function and *eden*.

- **etty.py**: run *ed.py* line editor, use *console*,
  module to collect and edit input lines.  Use
  non-default keymaps with *Command* class to provide retro
  printing-terminal-style editing and history.  Contrast to *ed.py*
  *main* function and *edc*.

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

Revised Aug 2017
