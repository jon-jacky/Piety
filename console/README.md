
console
=======

Modules used by terminal applications:

- **command.py**: Skeleton command line application.
  Collects a command (string), passes it to a handler (callable) to execute.
  Can collect command without blocking, for cooperative multitasking.
  Provides command history, rudimentary in-line editing similar to Unix readline.
  Provides optional hooks for job control commands that bypass the application.

- **key.py**: Collect, store, return single character or
    multi-character key sequences.

Revised February 2015

