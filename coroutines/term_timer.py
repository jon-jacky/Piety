"""
term_timer.py - Demonstrate interleaving of aterminal reader and an atimer task
                in an asyncio event loop.  Directions in term_timer.txt
""" 

import aterminal, atimers 

ta = aterminal.loop.create_task(atimers.atimer(5,5,'A'))

aterminal.main()

