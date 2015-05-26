
console
=======

Modules used by terminal applications, including a pure Python
non-blocking alternative to Python *raw_input* or Unix *readline* 

- **command.py**: Skeleton command line application.  Collects a
  command (string), passes it to a handler (callable) to execute.  Can
  collect a command one character at a time without blocking, for
  cooperative multitasking.  Provides command history, rudimentary
  in-line editing similar to Unix *readline*.  Provides optional hooks
  for job control commands that bypass the application.  A *Command*
  instances can work in *reader* mode where it uses the function
  passed to the *reader* initializer argument to read input, or,
  alternatively, can work in *receiver* mode where it uses the 
  built-in *handle_key* method to accept input passed from a caller.  
  This module's *main* function demonstrates both alternatives.  See
  *scripts/console_tasks.py* and *scripts.twisted/console_tasks_receiver.py* 
  for more examples.

- **command.txt**: command summary for *command.py*, similar to Unix
   *readline*.  How to edit the command line and access its history
   in any application the uses *console.py*

- **key.py**: Collect, store, return single character or
    multi-character key sequences.  Can be used as a *reader* by *Command*.

Revised April 2015
