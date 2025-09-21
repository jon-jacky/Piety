"""
eventloop.py - Creates BUT DOES NOT START an asyncio event loop named
 piety that responds to terminal keystrokes. Our shells and editors run
 in this event loop, and it can also run other asyncio tasks.

This event loop is named piety because it is essential for running
asyncio tasks along with the functioning terminal in the Piety system.

This script creates BUT DOES NOT START the piety event loop. To start
the event loop, after this script type these commands at the standard
Python REPL: 

  >>> from eventloop import * 
  ... 
  >>> piety.create_task(...)
  ...
  >>> piety.run_forever() 
  
This gives you the opportunity to create tasks for this event loop to run
before you start it -- then those tasks will also start when you
call run_forever() 

After you type the piety.run_forever() command, you will see no prompt.
Type RETURN to show the prompt.   It shows four darts >>>> to indicate
that the REPL is now running in the piety event loop.  You may have to 
type RETURN once again to start any tasks that run from the event loop.

Alternatively, you can type piety_start() at the >>> prompt.  Then
the ansyncio prompt >>>> will appear immediately.  (Note that is 
and underscore _ not a dot).

To stop the event loop and pause all the tasks it is running, type ^D or
exit() at the >>>> prompt. NOw you see the >>> prompt again to indicate
you are running in the standard Python REPL.  You can restart the event
loop and resume the tasks by typing the piety.run_forever() or piety_start()
command again.

Although this module is essential for using asyncio in Piety, it does
not contain any async code -- it does not use the keywords async or
await. Tasks that run in this event loop do use the async and await
keywords. But the code in this module that handles keystrokes is just a
handler, not a task.
 
This module is based on the earlier piety.py. We renamed it to
eventloop.py here to avoid the inconveniences that arise when a module
has the same name as one of its contents: if you write 'from piety
import *' then piety refers only to the eventloop, you can no longer use
piety to refer to the module itself.

We also removed piety.run_forever() from this script so you can create
other tasks before starting the event loop.
  
Also, we no longer do 'from import run' here. It makes more sense to
import run before we run this module, so we can use to it run this very
module.
  
We are keeping the old piety.py module because it appears in some older
scripts and documentation.
 
The Python asyncio library uses the name event_loop, which is different
from our name eventloop.
"""

import sys, asyncio
import pyshell, apyshell, apmacs
 
def handler():
    if pyshell.cmd_mode:
        apyshell.apysh() # async shell
    else:
        apmacs.apmrun()  # async display editor foreground job       

piety = asyncio.get_event_loop() 
piety.add_reader(sys.stdin, handler)

def piety_start():
    """
    Alternative to piety.run_forever() 
    so you don't need to type RET to get the >>>> asyncio shell prompt
    """
    apyshell.setup()
    apyshell.running = True
    piety.run_forever()
    
