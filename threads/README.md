
threads
=======

Experiments with tasking and concurrency using Python threads.

These experiments run in our [pmacs](../editors/README.md) editor,
which we start here from the script in *tm.py* rather than
*pm.py*.  The name *tm* is supposed to suggest "tasking *pmacs*".
The *tm* script loads all the modules used by *pmacs*, some additional
modules that support the tasking experiments, and starts our custom 
*pysh* (rhymes with fish) Python interpreter.

To start editing in a display window, type the function call *tpm()* at
the *pysh* prompt >>, instead of the *pm()* call you type at the standard
Python prompt >>>.   To return to the *pysh* command prompt, type M-x
(meta x, hold the alt key and type x), just as you do in  any *pmacs*
session.
   
### Files ###

- **threads_1.txt**: Directions for experiments with Python threading
   using the functions in *timers.py* and *writer.py*.  These experiments
   run with the standard Python interpreter and reveal its limitations.

- **threads_2.py**: Script that runs the code explained in *threads_2.txt*.
 
- **threads_2.txt**: Directions for experiments with Python threading
  using functions in *timer* and *writer* with out custom *pysh* interpreter.
  Here we show two threads rapidly updating two buffers
  in two windows, while we type at our *pysh* interpreter to control  the threads.

- **threads_3.py**: Script that runs the code explained in *threads_3.txt*.

- **threads_3.txt**: Directions for further experiments with Python threading
  using functions in *timer* and *writer* with the *pysh* interpreter.
  Here we show a thread updating a buffer in one window,
  while we edit text in another buffer in its window, or type at our *pysh*
  interpreter.

- **timers.py**: Functions to run in tasking experiments, that print
   timestamps at intervals.

- **tm.py**: script that loads modules for threading experiments, including
  editors, *writer*, *timers*, classes and functions from *threading*, and
  then starts our custom *pysh* Python interpreter.

Revised Jun 2024

