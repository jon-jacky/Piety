
coroutines
==========

Experiments with tasks using Python coroutines and the *asyncio* event loop.

All of these scripts assume you have already assigned *PYTHONPATH* by running
this command:

   ...$ . ~/Piety/bin/paths

The initial dot . in this command is essential.  This command assumes 
the top level *Piety* directory is in your home directory.

### Files ###

- **aterminal.py**: Read characters from the terminal in the *asyncio* event loop.

- **atimers.py**: Coroutines that print timestamps at intervals, 
 to run in tasking experiments. 

- **term_timer.py**: Demonstate interleaving of *aterminal* reader and 
  an *atimer* task in an *asyncio* event loop.

- **term_timer.txt**: Explanation and directinos for *term_timer.py*.

- **timer_loops.py** - Demonstrate interleaving timer tasks in short-lived *asyncio* 
  event loops  without a Python shell.

- **timer_loops.txt**: Explanation and directions for *timer_loops.py*.
     
Revised Jul 2024
 
