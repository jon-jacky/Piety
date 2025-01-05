"""
host.py - Functions that invoke the host operating system.
        These use Python standard libraries that are suposed to be portable 
        so the same functions should would work on different operating systems.
"""        

import subprocess

def sh(command):
    """
    Invoke shell command, a string
    See https://docs.python.org/3/library/subprocess.html
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

