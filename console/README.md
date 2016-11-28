
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

  *Console* works with *Key* and *InputLine* (see below) to read
  keycodes and edit the input line.

  This *console* module has some similarities to the Python standard
  library *cmd* module, but does not provide the same API.

- **console.txt**: command summary for *Console* with *Key* and *InputLine*,
   similar to Unix *readline*.  How to edit the command line and
   access its history in any application the uses *console*
   with the *inputline* and *key* modules.

- **key.py**: defines *Key* class that can collect, store, and return
    single character or multi-character keycodes.  It is the default
    *reader* argument of *Console.__init__* 

- **inputline.py**: Defines *InputLine* class that provides input and
    editing within a single line, used by *Console*.

Revised November 2016
