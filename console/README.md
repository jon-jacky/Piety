
console
=======

Modules used by terminal applications.

- **console.py**: defines the *Console* class, a wrapper that adapts
  a terminal application for cooperative multitasking.  A *Console*
  instance is a Piety job that can be scheduled by a *Session*
  instance.

  A *Console* instance collects a line (string), then passes it to an
  application handler (callable) to process.  It collects the line
  one character at a time without blocking to permit cooperative
  multitasking (unlike Python *input*, which blocks until the line
  is complete).  It provides command history and in-line editing similar to
  Unix *readline* (but no tab completion).  It provides hooks for job
  control.

  The editing keycodes and their effects are configured by a table.

  *Console* works with *GetKey* (see below) to read keycodes.

- **console.txt**: command summary for *Console* with *Key*,
   similar to Unix *readline*.  How to edit the command line and
   access its history in any application the uses *console*
   with the *key* module, and the built-in default table.

- **console_debug.md**: Directions for using *console_debug* and
    *console_task*.

- **console_debug.py**: Instrumented version of **console.py**.
    Imports *getkey_debug* and *display_debug*.

- **console_task.py**: Tests a *Console* object running as a task under
    the Piety scheduler.  Imports the instrumented *console_debug*.

- **getkey.py**: defines *GetKey* class that can collect, store, and return
    single character or multi-character keycodes, used by *Console*.

- **getkey_debug.py**: Instrumented version of *getkey.py*, 
    imported by *console_debug*.

- **getkey_task.py**: Like the test in *getkey.py* *main()*,
    but runs as a task under the Piety scheduler.

Revised Jan 2023
