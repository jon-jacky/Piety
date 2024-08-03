
pmacs_script
============

*pmacs_script.py* demonstrates several Piety features.

*pmacs_script.py* shows our   custom Python shell *pysh* and our Emacs-like
editor *pmacs* running without  blocking in a Python *asyncio* event loop,
while a timer task runs concurrently, as you  type commands in the shell
or edit text in the editor.  Timer messages appears in an editor window, and you
can control the speed of the timer from the shell -- or stop it and
create another one.

Just follow these directions:

First you must assign *PYTHONPATH* by running this command at the system 
command prompt:

     ...$ . ~/Piety/bin/paths

The initial dot . in this command is essential.  This command assumes 
the top level *Piety* directory is in your home directory.

Then make sure you are in the *~/Piety/piety* directory.  This is needed
for the Piety *run* command.

    ...$ cd ~/Piety/piety

Run the *piety.py* script at the system command prompt to start the
Piety event loop:

    ...$ python3 -m piety
    >>>>

Our *pysh* custom Python interpreter command prompt appears: *>>>>*.  It has
four darts, not three, to distinguish it from the standard Python prompt. It
works much like the standard Python interpreter.  Any Python statement should
work as usual.  You can use all the same inline editing commands, and retrieve
commands from its history.

Confirm that the Piety event loop is running.  The name of this event loop is also
*piety*:

    >>>> piety
    <_UnixSelectorEventLoop running=True closed=False debug=False>    

Confirm that no tasks are yet running.  The *pysh* shell is not a task, it is
just a *reader* (a keyboard event handler):

    >>>> asyncio.all_tasks(piety)
    set()

Run *pmacs_script* to start the *pmacs* editor and the timer task.   If your
default directory is not *~/Piety/piety*, you must type the path to that
directory here: 

    >>>> run('pmacs_script.py')
    a.txt, 0 lines

Two editor windows appear in the terminal.  The upper window, showing  the
*pmacs* editor buffer *a.txt*, shows messages written by the timer task
appearing once per second.  The lower window, showing editor buffer
*scratch.txt*, is empty, with a cursor at the beginning of the first line.

Type some text into the lower window and confirm that the timer messages continue
appearing, without interfering with your typing.   The *pmacs* editor works as 
usual.

There is a *pysh* prompt *>>>>* at the bottom of the terminal window.  To 
put the cursor there, type the command *M-x* ("meta x") by holding down the
keyboard *alt* key while you type the *x* key.  

Confirm the timer task is running.

    >>>> asyncio.all_tasks(piety)
    {<Task pending name='Task-1' coro=<ATimer.atimer() running at
    /home/jon/Piety/coroutines/atimers.py:43> wait_for=<Future pending
    cb=[Task.task_wakeup()]>>}

Again, the *pmacs* editor is not a task, it is just a *reader*.

Examine the timer object and confirm that the timer interval is one second:

    >>>> ta
    <atimers.ATimer object at 0x7fb384d610>
    >>>> ta.delay
    1

Set the timer interval to 0.1 to print messages ten times a second.

    >>>> ta.delay = 0.1

See the messages appear rapidly in the *a.txt* window.   Let the task
run until 1000 messages appear.  Then it stops.  Confirm that the task
has exited.  You can just type the up-arrow key or C-p (*control p*, hold
down the *ctrl* key while typing *n*) to retrieve the previous *all_tasks* command.

    >>>> asyncio.all_tasks(piety)
    set()

Type this command to start another timer task.  It writes 1000 messages at
1 second intervals to *a.txt*, all labelled *A*.

    >>>> piety.create_task(ta.atimer(1000,1,'A',abuf))
    <Task pending name='Task-2' coro=<ATimer.atimer() running at
    /home/jon/Piety/coroutines/atimers.py:35>>

Messages again appear in the *a.txt* window.

To resume editing, type this command:

    >>>> apm()

Now the cursor returns to the *scratch.txt* widow, at the location  where you
left it.  You can  alternate *M-x*  and *apm()* commands to swtich between
typing Python commands to *pysh* and editing text in the window.

It is instructive to see how short you can make *ta.delay* -- how rapidly you 
can write messages in the timer window -- while still being able to edit
or type commands, without scrambling the any text.

You can stop the task before it writes 1000 messesages by assigning
*ta.run = False*:
 
    >>>> asyncio.all_tasks(piety)
    {<Task pending name='Task-6' coro=<ATimer.atimer() running at
    /home/jon/Piety/coroutines/atimers.py:43> wait_for=<Future pending
    cb=[Task.task_wakeup()]>>}
    >>>> ta.run
    True
    >>>> ta.run = False
    >>>> asyncio.all_tasks(piety)
    set()

To finish this experiment, type the *clr()* command to resume scrolling in
the terminal so the windows will scroll out of sight.   Then type *C-d* (hold
down *ctrl* while typing *d*) at the prompt to exit from Piety back to the
system command interpreter.

    >>>> clr()
    >>>> (C-d, does not echo)
    .... $

Instead of *C-d*, you can also type *exit()*.

Revised Aug 2024
 
