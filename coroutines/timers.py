# timers.py

# Demonstrate interleaving timer tasks in the asycio event loop.

# To run this script:
# . ~/Piety/bin/paths 
# python3 -i 
# >>> import timers

import asyncio as aio
loop = aio.get_event_loop()
print(loop)
print(aio.all_tasks(loop))

from atimers import atimer
ta = loop.create_task(atimer(5,5,'A'))
print(ta)
print(aio.all_tasks(loop))

loop.run_until_complete(ta)
print(aio.all_tasks(loop))
print()

# Set up tasks to interleave

ta = loop.create_task(atimer(5,1,'A'))
tb = loop.create_task(atimer(10,0.5,'B'))
print(aio.all_tasks(loop))

loop.run_until_complete(ta)
print(aio.all_tasks(loop))

# The other task hasn't completed yet.
 
loop.run_until_complete(tb)
print(aio.all_tasks(loop))
 

 
