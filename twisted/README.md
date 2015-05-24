
twisted
=======

Non-blocking event loop using the Twisted reactor.

The platform-independent *piety* module can import the *eventloop*
module from this directory.  The *bin/twisted_paths* command puts this
directory on the *PYTHONPATH*

NOTE: At this time *twisted/eventloop.py* only works with tasks that
    are triggered by the timeout event, for example in
    *scripts/embedded* and *scripts/eventloop*.  It DOES NOT WORK with
    tasks that use the standard input, for example in
    *scripts.twisted_eventloop/piety.twisted_eventloop*

Revised May 2015
