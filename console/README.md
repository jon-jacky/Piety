
console
=======

Modules used by terminal applications.

- **console.py**: defines the *Console* class, a wrapper that adapts
  a terminal application for cooperative multitasking.  A *Console*
  instance is a Piety job that can be scheduled by a *Session*
  instance.

  A *Console* instance collects a command (string), passes it to an
  application handler (callable) to execute.  Can collect a command
  one character at a time without blocking to permit cooperative
  multitasking (unlike Python *input*, which blocks until the command
  is complete).  Provides command history and line editing similar to
  Unix *readline* (but no tab completion).  Provides hooks for job
  control.

  *Console* works with *Key* (see below) to read keycodes.

- **console.txt**: command summary for *Console* with *Key*,
   similar to Unix *readline*.  How to edit the command line and
   access its history in any application the uses *console*
   with the *key* module.

- **key.py**: defines *Key* class that can collect, store, and return
    single character or multi-character keycodes, used by *Console*.

Revised Jan 2018
