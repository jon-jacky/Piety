
demo.py
=======

**[demo.py](demo.py)** demonstrates many features of the Piety system,
including concurrent tasks, job control, editors, a windowing system,
and an enhanced shell.

**demo.py** uses the Piety scheduler to run the four jobs created by
*[session.py](session.py)*, concurrently with two timestamp tasks.  Each timestamp
task updates an editor buffer.
You can see these buffers update in their windows as you edit in another window
or on the command line.

Here is a sample session that demonstrates this.  Here *>>* is
Piety's Python prompt (with two brackets, to distinguish it from
the standard Python prompt with three brackets *>>>*).
Here *:* is the editor command
prompt, you type the commands that follow.  First, start the script and
run the [edsel](../editors/edsel.md) display editor.
The *edsel* screen with one window appears:

    ... $ python3 -im demo
    .   ts1                   0  Text     (no file)
    .   ts2                   0  Text     (no file)
    . * main                  1  Text     (no file)
    >> edsel.main(c=12)
    ... edsel screen with 12-line scrolling region appears ...

Next, type commands at the *edsel* command prompt to create
two new windows that show timestamps updating, then traverse to
the original *main* window and edit.  The *o2* command splits the window,
*b ts1* makes *ts1* the current buffer (and displays it in the focus window),
and *o* moves the focus to the next window:

    :o2
    :b ts1
    . * ts1                 61  ts1
    :o2
    :b ts2
    . * ts2                105  ts2
    :o
    :o

Then, at the prompt, type the *edsel* *C* command to change to
display editing mode. (That's a capital *C*, it is case sensitive.)

    :C

The cursor moves into the *main* window.  Type and edit text
in the window in the usual way for [edsel](../editors/edsel).
Notice that the lines generated by the two timestamp
tasks keep appearing and
scrolling up in the *ts1* and *ts2* windows as you edit.

To exit display editing mode and return to the command prompt, type *^Z*.
(control-Z).

Some interesting commands to type at the *edsel* command prompt:

 - *b ts1* - in the focus window, display the buffer that contains the
 timeout messages from *ts1task*.  This window updates each time the
 task generates a new message, even when another window gets focus
 and updates as its text is edited.

Some interesting Python commands to type at the *Python* command prompt.
(The three editor jobs have the *[wyshka](../shells/wyshka.py)* shell built-in,
so you can use the Python command line without exiting the editor, by prefixing
each Python command with an exclamation point, or by typing just an
exclamation point on the command line by itself to switch to Python.)

 - *jobs()* - show information about jobs

 - *piety.tasks()* - show information about tasks

 - *ts1task.enabled=piety.false* - disable *ts1task* so *ts1* buffer stops updating

 - *ts1task.enabled=piety.true* -  enable *ts1task* so *ts1* buffer resumes updating

 - *ts1task.enabled=alternate* - run *ts1task* handler on alternate timeout events

 - *piety.cycle.period=0.1* - cause *ts1* buffer to update ten times a second

 - *piety.cycle.period=1.0* - cause *ts1* buffer to resume updating once a second

 - *edm.a('append line after dot')* - or any other call from the *ed* API.

### API and data structures ###

You can access the editor API and data structures from the Python prompt
by prefixing them with *edm.* ("*ed* module"): *edm.n()*, *edm.buffers* etc.
We have to use this module name to distinguish it from the *ed* job.

You can access the display API and data structures by prefixing them
with *frame.*: *frame.windows* etc.

### Bugs ###

The demonstration works as intended when you run the display editor
*edsel*.  It does not work when you run the display editor *edda*.
With *edda*, the cursor jumps to the beginning of the line
on each timer tick.   A partial explanation appears in the
comments in [demo.py](demo.py).   At this time we have not decided
on the best solution for this.

Revised May 2019