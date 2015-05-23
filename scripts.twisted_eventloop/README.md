
scripts.twisted_eventloop
=========================

This directory contains Python scripts that run applications as tasks
or jobs, using an event loop from the Twisted framework instead of the
event loop from Piety.

This is similar to the experiment in the *scripts.twisted* directory,
but here the body of the event loop called by Twisted *reactor.run* is
in the separate *twisted/eventloop* module, instead of in this script,
(as in the *scripts.twisted* experiment).   

The purpose of this experiment is to package the Twisted event loop in
an *eventloop* module in the same way as the usual Piety event loop,
so we can choose the twisted event loop instead of the usual event
loop simply by importing *eventloop* from *twisted/eventloop.py*
instead of *select/eventloop.py*.

To import *twisted/eventloop* instead of the usual *select/eventloop*.
put the *twisted* directory on your *PYTHONPATH* instead of the
*select* directory.  A convenient way to achieve this is to run tje
*bin/twisted_paths* command instead of the usual *bin/paths*.

It was necessary to revise some scripts:

- **console_tasks_receiver_eventloop.py**: Similar to *scripts.twisted/console_tasks_receiver.py*,
  except it also assigns *piety.eventloop.application = console*
  Here *piety.eventloop* is imported from *twisted/eventloop.py*.  This assigment is
  needed to enable Twisted to invoke the intended Piety job.

- **piety.twisted_eventloop**: Similar to *scripts/piety*, but here 
  *piety.run* executes the Twisted *reactor.run* event loop
  imported from *twisted/eventloop* instead of the usual Piety event loop.
  Also uses *console_tasks_receiver* and *writer_tasks*.  

- **writer_tasks.py**: Creates writer tasks used by the *embedded* and
    *piety* scripts.  The same file as *scripts/writer_tasks.py*,
    copied here so it is easy to import.

Revised May 2015
