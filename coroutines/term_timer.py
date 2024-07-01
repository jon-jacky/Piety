"""
term_timer.py - Demonstrate interleaving of aterminal reader and atimer task
                 in asycnio event loop.

...$ python3 -im term_timer
>

Then at the > prompt, type abc.  Do not type <RET> (RETURN or ENTER).  When
5 seconds have passed, the first timer message  appears:

...$ python3 -im term_timer
> abcA 1 2024-06-19 17:07:35.823368 

Then on the next line, type def and wait for next timer message.  And so on 
until all 5 timer messages have appeared.  Then type pqr<RET>.  The program
prints all the characters you typed:

...$ python3 -im term_timer
> abcA 1 2024-06-19 17:07:35.823368
defA 2 2024-06-19 17:07:40.827853
ghiA 3 2024-06-19 17:07:45.834841
jklA 4 2024-06-19 17:07:50.840380
mnoA 5 2024-06-19 17:07:55.845229
pqr
abcdefghijklmnopqr
>>> 

"""

import aterminal, atimers 

ta = aterminal.loop.create_task(atimers.atimer(5,5,'A'))

aterminal.main()
