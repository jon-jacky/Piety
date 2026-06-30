
piety
=====

Piety provides concurrency with a Python *asyncio* event loop.  Tasks 
are implemented by Python *coroutines* or *readers* (event handlers) that
run in an event loop.

Piety provides readers for *pysh*, its custom Python shell, and *pmacs*, its
Emacs-like editor.  These enable the shell and the editor to run without 
blocking in an event loop, so other tasks can run concurrently, as you 
type commands in the shell or edit text in the editor.  You can control
other tasks from the shell and display task output in editor windows.

<img src="../screenshots/vedsel_script.png"
 alt="vedsel_script.py running in the Piety desktop" width=67% height=67%>

More to come ...

### Files ###

- **aiotimers.py**:  Demonstrations of *asyncio* tasking, that run in the
    Piety desktop.

- **aiotimers.md**:  Directions and explanations of the demonstrations in
    *aiotimers.py*

- **apm.py**: Script to start the *pmacs* editor in an *asyncio* event loop.

- **apmacs.py**: Adapt the *pmacs* editor to run in an *asyncio* event loop.  

- **apyshell.py**: Adapt the *pysh* custom Python shell to run in an *asyncio*
  event loop.
 
- **eventloop.py**: Creates the Piety *asyncio* event loop but does 
    not start it.

Modules and documentation files for older demos that do not run in the
Piety desktop are described in [piety0.md](piety0.md).
    
Revised Jun 2026

 
