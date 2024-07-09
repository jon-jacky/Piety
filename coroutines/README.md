
coroutines
==========

Experiments with tasks using Python coroutines and the *asyncio* event loop.

### Files ###

- **apyshell.py**: Custom Python shell that can be used from the *asyncio* 
  event loop.
 
- **aterminal.py**: Read characters from the terminal in the *asyncio* event loop.

- **atimer_script.py**: Demonstrate the Python shell and timer tasks interleaving
  in the Piety event loop.

- **atimer_script.txt**: Explanation and directions for *atimer_script.py*.
 
- **atimers.py**: Coroutine that prints timestamps at intervals, to run
  in tasking experiments.

- **edsel_script.py**: Display interleaving timer tasks in two editor windows.

- **edsel_script.txt**: Explanation and directions for *edsel_script.py*.

- **piety.py**: Start an interactive Python shell running in an *asyncio* event loop 
  named *piety*.  Import a function named *run* to run scripts from that 
  shell, which can use that *piety* event loop.

- **piety.txt**: Explanation and directions for *piety.py*.

- **term_timer.py**: Demonstate interleaving of *aterminal* reader and 
  an *atimer* task in an *asyncio* event loop.

- **term_timer.txt**: Explanation and directinos for *term_timer.py*.

- **timers.py** - Demonstrate interleaving timer tasks in short-lived *asyncio* 
  event loops  without a Python shell.

- **timers.txt**: Explanation and directions for *timers.py*.
     
Revised Jul 2024
 
