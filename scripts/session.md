
session.py
==========

**[session.py](session.py)** creates a Piety *Session* instance with four *Console*
jobs: the [pysh](../shells/pysh.py) Python shell, the [ed](../editors/ed.md) line editor,
the [edda](../editors/edda.md) display editor, and the
[edsel](../editors/edsel.md) display editor.

### Running and pausing jobs ###

Here is a typical session, that shows how to invoke each job.  The
*pysh* job (a Python interpreter) runs at startup
(the *pysh* Python prompt is two brackets *>>* to distinguish
it from the standard Python prompt with three brackets *>>>*).
Invoke the other
jobs from the Python prompt by calling their *main* methods, with the
same syntax you use for a standalone program:
*ed.main()* etc.  Exit from each job to return to the Python interpreter.

    ... $ python3 -im session
    >> dir()
    ... ed ... edsel ... edm ... edda ... pysh ...
    ... fg ... frame ... jobs ... main ...
    >> ed.main('README.md')
    ... edit in README.md ...
    :q
    >> import datetime
    >> edda.main(c=12)
    ... display editor appears with 12 lines in command region,  shows README.md
    ... continue editing README.md
    :q
    >> datetime.datetime.now()
    ... datetime module is still imported
    >> edsel.main()
    ... continue editing README.md
    :q
    >> exit()
    ... exit from pysh to standard Python interpreter
    >>> exit()
    ... exit from Python
    ...$

You never actually exit from a job, you just suspend it.
Each job (including the Python interpreter)
preserves its state between invocations, so work in progress can be resumed.
The line editor *ed* and the display editors *edda*
and *edsel* share the same state including editor buffers and insertion points.
Also, *edda* and *edsel* share window state.

If *session* exits for any reason,
control returns to the standard Python intepreter (with the *>>>* prompt).
You can resume the session by typing *main()*, the state of every job will be intact.
  
## Job control ##

The *session* module also demonstrates job control, including the
*job* function that lists the jobs, the *^Z* command for suspending a job
and the *fg* (foreground) function that resumes the most recently
suspended job:

    ...$ python3 -im session

    # Initally the pysh job is in the foreground

    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307fac8>   ed       State.loaded
    <console.Console object at 0x10307ff98>   edda    State.loaded
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Running ed brings it to the foreground and puts pysh in the background

    >> ed.main()
    :!jobs()
    <console.Console object at 0x10307fac8>   ed       State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307ff98>   edda    State.loaded
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Exiting ed makes it suspended and returns pysh to the foreground

    :q
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <console.Console object at 0x10307ff98>   edda    State.loaded
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Running edda brings it to the foreground

    >> edda.main()
    :!jobs()
    <console.Console object at 0x10307ff98>   edda    State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Typing ^Z to stop edda makes it suspended

    :^Z
    Stopped
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307ff98>   edda    State.suspended
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Typing fg() brings the suspended edda job back to the foreground

    >> fg()
    :!jobs()
    <console.Console object at 0x10307ff98>   edda    State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

    # Quitting edda makes it suspended and puts pysh back in the foreground

    :q
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307ff98>   edda    State.suspended
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <edsel.Console object at 0x1030d3908>   edsel     State.loaded

### API and data structures ###

You can access the editor API and data structures from the Python prompt
by prefixing them with *edm.* ("*ed* module"): *edm.n()* etc.
We have to use this module name to distinguish it from the *ed* job.

You can access the storage API and data structures by prefixing them
with *st.*: *st.buffers* etc.

You can access the display API and data structures by prefixing them
with *frame.*: *frame.windows* etc.

The three editor jobs have the *[wyshka](../shells/wyshka.py)* shell built-in,
so you can use the Python command line without exiting the editor, by prefixing
each Python command with an exclamation point, or by using just an
exclamation point to switch the editor command line to Python.

Revised Oct 2020
