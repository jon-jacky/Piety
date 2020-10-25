"""
shellcmd.py - function to invoke shell command.
        See https://docs.python.org/3/library/subprocess.html
"""

import subprocess

def sh(command):
    """
    Invoke shell command, a string
    Capture command output and print it in the calling process, 
    so 'with redirect_stdout' works.
    """
    cp = subprocess.run(command, shell=True, text=True, capture_output=True)
    if cp.stdout:
        print(cp.stdout)
    if cp.stderr:
        print(cp.stderr)


