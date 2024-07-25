
coroutines
==========

Experiments with tasks using Python coroutines and the *asyncio* event loop.

All of these scripts assume you have already assigned *PYTHONPATH* by running
this command:

   ...$ . ~/Piety/bin/paths

The initial dot . in this command is essential.  This command assumes 
the top level *Piety* directory is in your home directory.

### Files ###

- **apmacs.py**: Runs the *pmacs* editor in the *asyncio* event loop.

- **apyshell.py**: Custom Python shell that can be used from the *asyncio* 
  event loop.
 
- **aterminal.py**: Read characters from the terminal in the *asyncio* event loop.

- **atimer_script.py**: Demonstrate the Python shell and timer tasks interleaving
  in the Piety event loop.

- **atimer_script.txt**: Explanation and directions for *atimer_script.py*.
 
- **atimers.py**: Coroutine that prints timestamps at intervals, to run
  in tasking experiments.

- **edsel_script.py**: Display interleaving timer tasks in two editor windows.
  You can set the timer intervals and stop the tasks from the Python REPL.

- **edsel_script.txt**: Explanation and directions for *edsel_script.py*.

- **piety.py**: Start an interactive Python shell running in an *asyncio* event loop 
  named *piety*.  Import a function named *run* to run scripts from that 
  shell, which can use that *piety* event loop.

- **piety.txt**: Explanation and directions for *piety.py*.

- **pmacs_script.py**: Edit in one window while timer task updates the other.
  in the other.   You can set the timer intervals and stop the tasks from
  the Python REPL.

- **term_timer.py**: Demonstate interleaving of *aterminal* reader and 
  an *atimer* task in an *asyncio* event loop.

- **term_timer.txt**: Explanation and directinos for *term_timer.py*.

- **timer_loops.py** - Demonstrate interleaving timer tasks in short-lived *asyncio* 
  event loops  without a Python shell.

- **timer_loops.txt**: Explanation and directions for *timer_loops.py*.
     
Revised Jul 2024
 
