Piety scheduler
=====

The core of Piety is the scheduler, the function *piety.run* defined
here. It can run in any Python interpreter session.  It schedules
instances of the *piety.Task* class, also defined here.

To run tasks in Piety, import the *piety* module, create some *Task*
instances, then call *piety.run*.  See the examples in the *samples*
directory.  More details appear in docstrings.

Piety is event-driven.  Each Piety task instance is defined by an
*event*, a *guard*, a *handler*, and a *name*.  The scheduler may
invoke a task's handler when its event occurs and its guard is True.
Then the handler runs until it returns control to the scheduler.
There is no preemption.  This is called *cooperative multitasking*.

A handler can be any Python callable including a function, method,
generator or coroutine.  A guard can be any Python callable that
returns a Boolean value.  Events can include input becoming available
on a file or socket, or a timer tick. (In this version, Piety can
schedule on any event handled by the *select* system call.)

Files in this directory include:

- **piety**, scheduler core, defines *Task* class and *run* function
