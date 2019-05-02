
samysh.py
=========

**[samysh.py](samysh.py)** provides a scripting facility for any command line program.
  It was created to run test scripts in the *[edo](../editors/edo.md)* line editor
  and the *[edsel](../editors/edsel.md)* and *[eden](../editors/eden.md)* display editors.

**samysh.py** provides three functions:

- *show_command* executes a single command with an optional echo and delay.
  This is helpful for seeing the command's effects, especially in
  programs that update a display, such as display editors.

- *run_script* runs an entire sequence (or script) of commands with optional echo and delay.
  The individual commands can be single characters, multi-character keycodes,
  or entire command lines.

- *add_command* adds one new command to a command line program. Use this to
  add the command the runs a script.

The *[edo](../editors/edo.py)* editor (explained
[here](../editors/edo.md)) demonstrates how to use *samysh*.

Revised May 2019

