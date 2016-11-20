
console
=======

Modules used by terminal applications, including a non-blocking
alternative to Python *input*, with command line editing and history
similar to Unix *readline*.

- **console.py**: defines *Console* class, a skeleton command line
  application.  A *Console* instance collects a command (string),
  passes it to a handler (callable) to execute.  Can collect a command
  one character at a time without blocking to permit cooperative
  multitasking (unlike Python *input*, which blocks until the command
  is complete).  Provides command history and editing similar to Unix
  *readline* (but no tab completion).  Provides hooks for optional job
  control commands that bypass the application.

  *Console* can work with *LineInput* (see below) to provide command
  line editing.  Minimal line editing is provided in the *command*
  module.

  A *Console* instance can work in *reader* mode where it uses the
  function passed to the *handler* initializer argument to read input,
  or, alternatively, can work in *receiver* mode where it uses the
  built-in *handle_key* method to accept input passed from a caller.
  This module's *main* function demonstrates both alternatives.

  This *console* module has some similarities to the Python standard
  library *cmd* module, but does not provide the same API.

- **console.txt**: command summary for *Console* with *LineInput*,
   similar to Unix *readline*.  How to edit the command line and
   access its history in any application the uses *console.py*.

- **key.py**: defines *Key* class that can collect, store, return
    single character or multi-character key sequences.  Can be used as
    a *reader* by *Console*.

- **lineinput.py**: Defines *LineInput* class that provides editing
  for *Console* (or any other module that might need it).

Revised November 2016
