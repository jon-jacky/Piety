
console
=======

Modules used by terminal applications, including a pure Python
non-blocking alternative to *readline*:

- **command.py**: Skeleton command line application.
  Collects a command (string), passes it to a handler (callable) to execute.
  Can collect command without blocking, for cooperative multitasking.
  Provides command history, rudimentary in-line editing similar to Unix readline.
  Provides optional hooks for job control commands that bypass the application.

- **command.txt**: command summary for *command.py*, similar to Unix
   *readline*.  How to edit the command line and access its history
   in any application the uses *console.py*

- **key.py**: Collect, store, return single character or
    multi-character key sequences.

For more about *command* and *key*, see [here](../doc/command.md).

Revised February 2015
