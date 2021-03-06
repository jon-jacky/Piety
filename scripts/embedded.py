"""
embedded.py - Start a Piety session running two concurrent file writer
tasks, but without an interactive interpreter.  Shows that Piety can
run in a 'headless' mode with no console, as is needed in some
embedded systems.

When you run this script, Piety schedules the tasks to write 10
messages to w0.txt and 5 messages to w1.txt, then Piety exits.  To
see the writers working, open a terminal window and type: tail -f
w0.txt.  In another terminal window: tail -f w1.txt.

To repeatedly schedule the tasks, start the command using python -i
embedded. When Piety exits, writing stops, and the Python prompt
appears, type main():

 $ python -i embedded
 ... w0 writes 10 messages, w1 writes five, then they stop ...
 >>> main()
 ... writers write, stop again ...
"""

import piety, writer_tasks 

# Piety Writer tasks in writer_tasks module don't appear explicitly here

def main():
    # we don't need to assign piety.done because we use nevents instead
    piety.run(nevents=10) # handle 10 clock ticks and exit

if __name__ == '__main__':
    main()
