
session.py
==========

**session.py**: Creates a *Session* instance with four *Console*
jobs: the *pysh* Python shell, the [ed](../editors/ed.md) line editor,
the [edsel](../editors/edsel.md) display editor, and the
[eden](../editors/eden.md) display editor.

Here is a typical session, that shows how to invoke each job.  The
*pysh* job (a Python interpreter) runs at startup.  Invoke the other
jobs from the Python prompt by name using function call syntax: *ed()* etc.,
(which invokes
each job's *__call__* method).  Exit from each job to return to the
Python interpreter.

    ... $ python3 -im session
    >> dir()
    ...
    >> ed('README.md')
    ... edit in README.md ...
    :q
    >> import datetime
    ...
    >> edsel(c=12)
    ... display editor appears with 12 lines in command region,  shows README.md
    ... continue editing README.md
    :q
    >> datetime.datetime.now()
    ... datetime module is still imported
    >> eden()
    ... continue editing README.md
    :q
    >> exit()
    ... exit from pysh to standard Python interpreter
    >>> exit()
    ... exit from Python
    ...$

Each job (including the Python interpreter)
preserves its state between invocations, so work in progress can be
resumed.  The line editor *ed* and the display editors *edsel*
and *eden* share the same state including editor buffers and insertion points.
Also, *edsel* and *eden* share window state.

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
    <console.Console object at 0x10307ff98>   edsel    State.loaded
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Running ed brings it to the foreground and puts pysh in the background

    >> ed()
    :!jobs()
    <console.Console object at 0x10307fac8>   ed       State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307ff98>   edsel    State.loaded
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Exiting ed makes it suspended and returns pysh to the foreground

    :q
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <console.Console object at 0x10307ff98>   edsel    State.loaded
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Running edsel brings it to the foreground

    >> edsel()
    :!jobs()
    <console.Console object at 0x10307ff98>   edsel    State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Typing ^Z to stop edsel makes it suspended

    :^Z
    Stopped
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307ff98>   edsel    State.suspended
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Typing fg() brings the suspended edsel job back to the foreground

    >> fg()
    :!jobs()
    <console.Console object at 0x10307ff98>   edsel    State.foreground
    <console.Console object at 0x10302cbe0>   pysh     State.background
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <eden.Console object at 0x1030d3908>   eden     State.loaded

    # Quitting edsel makes it suspended and puts pysh back in the foreground

    :q
    >> jobs()
    <console.Console object at 0x10302cbe0>   pysh     State.foreground
    <console.Console object at 0x10307ff98>   edsel    State.suspended
    <console.Console object at 0x10307fac8>   ed       State.suspended
    <eden.Console object at 0x1030d3908>   eden     State.loaded

**session.py** can also demonstrate the enhanced shell and scripting
provided by [edo.py](../editors/edo.md).

Revised Apr 2019
