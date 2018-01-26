
run_timestamps.py
=================

**run_timestamps.py** demonstrates many features of the Piety system.
It uses the Piety scheduler to run the three jobs created by
*session.py*, concurrently with two timestamp tasks.  Each timestamp
task uses the print function to update an editor buffer.  You can
see these buffers update in their windows as you edit in another window
or in the command line.   

Here is a sample session that demonstrates this.  Here *>>* is the
Python prompt and *:* is the *edsel* display editor command
prompt, you type the commands that follow.

    ... $ python3 run_timestamps.py
    .   ts1                  0  ts1
    .   ts2                  0  ts2
    . * main                 1  None
    >> edsel()

*edsel* screen with one window appears

    :o2
    :b ts1
    . * ts1                 61  ts1
    :o2
    :b ts2
    . * ts2                105  ts2
    :o
    :o

(above) create two new windows that show timestamps updating, then traverse to
the original *main* window.

    :a
    Here is a new line ...
    Here is another 
    .
    :

(above) append lines of text in the *main* window, then exit append mode
and get back to the *edsel* command prompt.

Some interesting commands to type at the *edsel* command prompt:

 - *b ts1* - in the focus window, display the buffer that contains the
 timeout messages from ts1task.  This window updates each time the 
 task generates a new message, even when another window gets focus
 and updates as its text is edited.

Some interesting Python commands to type at the *edsel* command prompt
(prefix command with !) or at the Python prompt:

 - *jobs()* - show information about jobs

 - *piety.tasks()* - show information about tasks

 - *ts1task.enabled=piety.false* - disable *ts1task* so *ts1* buffer stops updating

 - *ts1task.enabled=piety.true* -  enable *ts1task* so *ts1* buffer resumes updating

 - *ts1task.enabled=alternate* - run *ts1task* handler on alternate timeout events 

 - *piety.cycle.period=0.1* - cause *ts1* buffer to update ten times a second

 - *piety.cycle.period=1.0* - cause *ts1* buffer to resume updating once a second

 - *edsel.frame.window.Window.nupdates=9990* - advance counter
    shown near right edge of status line.

 - *edsel.frame.refresh()* - refresh all windows and the command
    line.  This is also provided by the *edsel* *L* command.

 - *session.editor.console.command.point* - print index in command line or
    text line where next typed character will appear.

**run_timestamps.py** can also demonstrate all the commands provided
by *[session.py](session.md)*.

Revised Jan 2018
