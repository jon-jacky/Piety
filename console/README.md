
Console
========

Modules that define commands to enable Piety development and other
personal computing activities using only Python running Piety in the
console terminal, without depending on a host OS to provide a desktop
with multiple windows, the system shell, and other utilities.

[Files](#Files)   
[Commands](#Commands)   

### Files ###

- **console.py**: Python wrappers for the host shell, some particular shell
        commands, and Python help, that redirect command output to
        editor buffers.

- **redirect.py**:  Redirect command output to editor buffers,
              so the buffers can act much like terminal windows with
              scroll back.

### Commands ###

The *console* module provides a function *sh*, which runs any
shell command string, and functions for particular shell commands: 
*pwd*, *cd*, *ls*, *lsl*, *lslt*, and *man*.  It also provides
a *help* function.

The *cd* and *ls* functions can take an optional argument, a path string
(usually a directory) as an argument. The *ls* functions call the shell
commands *ls -C, ls -l, ls -lt*, respectively. The *man* function takes
the topic string as an argument, for example *man('ls')*. The *help*
function takes a Python object (not a string) as an argument, for
example *help(str)*.

The *pwd*, *cd*, and *help* functions call specific functions in the Python
standard library. The *sh*, *ls*, and *man*, functions run the host shell
in a subprocess.

The *sh*, *pwd*, *cd*, and *ls* commands all append their command string
and command output to the single *Console* buffer. Each call to *man*
and *help* creates a new buffer *topic.man* or *topic.help* that holds
the manual text or help text on just that topic.

Revised Apr 2025

