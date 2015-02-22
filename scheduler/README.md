
scheduler
=========

Modules that define and schedule tasks, jobs, and sessions.  This is
the core of the Piety operating system:

- **job.py**: Wrapper for application to provide hooks for job control
    from *session*.

- **piety.py**: Piety scheduler and event loop.  Defines the *Task*
   class and *run* function.  To run tasks in Piety, import the
   *piety* module, create some *piety.Task* instances, then call
   *piety.run*.

- **session.py**: Manage multiple jobs (applications) in one task.

See also the more detailed explanations [here](../doc/scheduler.md).

Revised February 2015

