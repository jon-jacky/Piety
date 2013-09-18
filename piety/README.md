piety
=====

The **piety** directory contains the Piety operating system code: the
scheduler, the console, and some utilities.

### Scheduler ### 

The core of the Piety operating system is the scheduler module *piety*.
The scheduler itself is the function *piety.run*. It can run in any
Python interpreter session.  It schedules instances of the
*piety.Task* class, also defined in this module.

To run tasks in Piety, import the *piety* module, create some *Task*
instances, then call *run*.  See the examples in the *samples*
directory.  More details appear in docstrings.

Piety is event-driven.  Each Piety *Task* instance is defined by an
*event*, a *guard*, a *handler*, and a *name*.  The scheduler may
invoke a task's handler when its event occurs and its guard is True.
Then the handler runs until it returns control to the scheduler.
There is no preemption.  This is called *cooperative multitasking*.

A handler can be any Python callable including a function, method,
generator or coroutine.  A guard can be any Python callable that
returns a Boolean value.  Events can include input becoming available
on a file or socket, or a timer tick. (In this version, Piety can
schedule on any event handled by the *select* system call.)

### Console ###

The *console* module contains a skeleton command line application.
It defines a class *Console*, with a *getchar* method that gets a single
character typed at the console keyboard, and adds it to a command line
(usually).  When *getchar* gets a line terminator character, it calls a
command function and passes the command line to it.  *Getchar* also
handles some editing functions and other control keys.

The *getchar* method is non-blocking when it is scheduled by the Piety
scheduler.  Other Piety tasks can run while the user is entering the
command line.

The command function is passed as an argument to the *Console*
constructor, so this same class can act as the front end to any
command line application.

### Terminal ###

To use *getchar*, the console must be put into single-character mode,
by calling the *setup* function in the *terminal* module.  The
*restore* function returns to the previous mode.


### Modules ###

These are the modules in the *piety* directory.  For more details see
their docstrings.

- **piety**, scheduler, defines *Task* class and *run* function

- **console**, skeleton command line application

- **terminal**, utilities used by *console*
