"""
shellcmd.py - function to invoke shell command.
        See https://docs.python.org/3/library/subprocess.html
"""

import subprocess

def shell(command):
    """
    Invoke shell command, a string
    Capture command output and print it in the calling process, 
     so 'with redirect_stdout' works.
    Call print on each line of output, to work with our writer module.
    """
    cp = subprocess.run(command, shell=True, text=True, capture_output=True)
    if cp.stdout:
        for line in cp.stdout.splitlines():
            print(line)
    if cp.stderr:
        for line in cp.stderr.splitlines():
            print(line)
            


