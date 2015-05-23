
scripts.twisted
===============

This directory contains Python scripts that run applications as tasks
or jobs, using an event loop from the Twisted framework instead of the
event loop from Piety.

This experiment demonstrates that Piety applications, tasks, and jobs
can run unchanged with a different event loop from a different
framework.  It was necessary to revise some scripts:

- **console_tasks_receiver.py**: Similar to *scripts/console_tasks.py*.
  It is necessary to use this module insted because Twisted requires
  that application *Command* instances be used in receiver mode (not
  reader mode as is usual in Piety).  
  Twisted code reads the input and then passes it to that instance's
  handler, which takes the input as a parameter.

- **piety.twisted**: Similar to *scripts/piety*, but uses the Twisted
  *reactor.run* method instead of Piety *piety.run* to concurrently
  run the console jobs and writers.  The body of the event loop
  called by Twisted *reactor.run* is in this module (not in a
  separate *eventloop* module as is usual in Piety).
  Also uses *console_tasks_receiver* and *writer_tasks*.  

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.  The same file as *scripts/writer_tasks.py*,
    copied here so it is easy to import.

Revised May 2015
