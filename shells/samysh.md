
samysh.py
=========

**[samysh.py](samysh.py)** provides a scripting facility for any command line program.
  It was created to run test scripts in the *[edo](../editors/edo.md)* line editor
  and the *[edsel](../editors/edsel.md)* and *[eden](../editors/eden.md)* display editors.

For example, the *[edo](../editors/edo.md)* editor (also
[here](../editors/edo.txt)) provides *samysh* scripting in its *X* command, 
which is used this way:

    X bufname echo delay

This command executes the editor or Python script in the named buffer 
with optional command echo (Boolean), delay seconds between script commands.

**samysh.py** provides four functions:

- *params* gets *echo* and *delay* parameters used by *show_command* and *run_script*
  (below).  Also gets buffer name used by *edo* *X_command* which uses *run_script*.

- *show_command* executes a single command with an optional echo and delay.
  This is helpful for seeing the command's effects, especially in
  programs that update a display, such as display editors.

- *run_script* runs an entire sequence (or script) of commands with optional echo and delay.
  The individual commands can be single characters, multi-character keycodes,
  or entire command lines.

- *add_command* adds one new command to a command line program. Use this to
  add the command the runs a script.

Revised June 3020

