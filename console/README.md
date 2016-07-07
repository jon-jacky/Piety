
console
=======

Modules used by terminal applications, including a non-blocking
alternative to Python *input*, with command line editing and history
similar to Unix *readline*.

- **command.py**: Skeleton command line application.  Collects a
  command (string), passes it to a handler (callable) to execute.  Can
  collect a command one character at a time without blocking to permit
  cooperative multitasking (unlike Python *input*, which blocks until
  the command is complete).  Provides command history and editing
  similar to Unix *readline* (but no tab completion).  Provides hooks
  for optional job control commands that bypass the application.

  A *Command* instance can work in *reader* mode where it uses the
  function passed to the *handler* initializer argument to read input,
  or, alternatively, can work in *receiver* mode where it uses the
  built-in *handle_key* method to accept input passed from a caller.
  This module's *main* function demonstrates both alternatives.

  This *command* module has some similarities to the Python standard
  library *cmd* module, but does not provide the same API.

- **command.txt**: Command summary for *command.py*, similar to Unix
   *readline*.  How to edit the command line and access its history
   in any application the uses *command.py*.

- **key.py**: Collect, store, return single character or
    multi-character key sequences.  Can be used as a *reader* by *Command*.

- **printing**: Script to demonstrate *Command* with its *keymap* modified to
      support a printing terminal.

Revised July 2016
