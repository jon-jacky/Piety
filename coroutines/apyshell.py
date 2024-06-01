"""
apyshell.py - Custom Python REPL in a coroutine.

Based on pyshell.py
"""

import aterminal, pyshell

async def apysh():
    """
    Custom Python REPL in a coroutine.  Based on pyshell.pysh.
    """
    pyshell.setup()
    while pyshell.running:
        c = await aterminal.agetchar()
        pyshell.runcmd(c)
    pyshell.restore()
  
