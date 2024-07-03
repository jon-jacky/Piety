
coroutines
==========

Experiments with tasks using Python coroutines and the asyncio event loop.

### Files ###

- **apyshell.py**: Custom Python shell that can be used from the asyncio 
  event loop.
 
- **aterminal.py**: Read characters from the terminal in the asyncio event loop.

- **atimer_script.py**: Script that demonstrates *atimer* tasks running with 
  the Python shell in the *piety* event loop.  Must be started from *piety_script*.
  Directions are in the module header.

- **atimers.py**: Coroutine that prints timestamps at intervals, to run
  in tasking experiments.

- **piety.py**: Script that starts the Python shell in the asyncio event 
  loop, here called *piety*, for interactive use.  Directions are in the
  module header.

- **piety_script.py**: Script that starts the Python shell in the asyncio
  even loop, here called *piety*, for running other scripts: *atimer_script*
  etc.  Directions are in the module header.

- **term_timer.py**: Demonstate interleaving of *aterminal* reader and 
  *atimers* task in the asyncio event loop.  Directions are in the 
  module header.

- **timers.py**: Script that runs code explained in *timers.txt*.

- **timers.txt**: Directions for demonstrating interleaving timer tasks using
  *atimers*.
     
Revised Jul 2024
 
