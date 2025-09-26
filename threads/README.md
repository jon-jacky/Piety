
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

NOTE added Sep 2025: Some of these demos no longer work. In particular,
in *threads_3* editing in the *scratch.txt* window while the timer
thread updates the *a.txt* window no longer works --- the cursor in
*scratch.txt* returns to column 1 on each timer tick, and control characters
are not processed correctly.   Also, in *threads_2*, typing commands at the
Python REPL can result in scrambling the two windows that display the 
two timer threads.  

Apparently, changes I made since Summer 2024 have broken the threads demos.
I spent some time trying to fix this but was unsuccessful. Meanwhile, I
have decided to concentrate on *asyncio* and event loops instead of
threads, so at this time I have no further plans to try to fix this.
   
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

Revised Sep 2025

