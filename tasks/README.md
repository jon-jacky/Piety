
tasks
=====

Experiments with tasking and concurrency.

### Files ###

- **pyshell.py** - Defines ustom Python REPL *pysh* that uses our *editline* 
   instead of builtin *input*.  Enables other tasks that write to the
   terminal to interleve with typing commands at our REPL.

- **pyshell.txt**: Notes on further experiments with Python threading   using functions in *timer* and *writer* with the *pysh* REPL.- **threads.txt**: Notes on initial experiments with Python threading
   using the functions in *timers.py* and *writer.py*.

- **timers.py**: Functions to run in tasking experiments, that print
   timestamps at intervals.

- **tm.py**: script that loads modules for threading experiments, including
  editors, *writer*, *timers*, and classes and functions from *threading*.

- **writer.py**: Functions that put text into sked buffers and edsel windows,
             intended to be called from background tasks.

- **writer.txt**:  Notes on *writer.py*.


Revised Apr 2024

