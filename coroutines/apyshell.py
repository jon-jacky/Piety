"""
apyshell.py - Custom Python REPL in a coroutine.

Based on pyshell.py
"""

import aterminal
import pyshell as sh

async_ps1 = '>>>> ' # prompt, different from CPython >>> and pyshell '>> ' #DEBUG
async_start_col = 5  # for '>>>> '

async def apysh():
    """
    Custom Python REPL in a coroutine.  Based on pyshell.pysh.
    """
    saved_ps1 = sh.ps1 # usually '>> '
    saved_start_col = sh.start_col # usually 3 
    sh.ps1 = async_ps1 # '>>>> ' - HACK, avoid making ps1 arg to runcmd
    sh.start_col = async_start_col # 5 
    sh.setup()
    while sh.running:
        c = await aterminal.agetchar()
        sh.runcmd(c)
    sh.restore()
    sh.ps1 = saved_ps1  
    sh.start_col = saved_start_col

