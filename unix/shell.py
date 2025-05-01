"""
shell.py - Python functions that wrap shell commands, so you can invoke
            the shell without exiting the Python session or using the
            host desktop.
            
This module provides a function sh(command), which runs any shell command,
and functions for particular shell commands: pwd, cd, man, ls -C, ls -l, ls -lt

The pwd and cd functions call specific functions in the Python standard library. 
The other functions run the host shell in a subprocess.

These functions all write shell command output on the standard output, so the
output can be redirected anywhere.
"""        

import subprocess, os, pydoc

width = 80  # width of command output for ls() and man() commands

def sh(command, shellenv=None):
    """
    Invoke shell command, a string, in a shell subprocess.
    shellenv is an optional environment to be used by the shell subprocess.
    See https://docs.python.org/3/library/subprocess.html
    Capture command output and print it on the calling process standard output,
     so 'with redirect_stdout' works.
    Call print on each line of output, to work with our writer module.
    """
    cp = subprocess.run(command, shell=True, text=True, capture_output=True,
                        env=shellenv)
    if cp.stdout:
        for line in cp.stdout.splitlines():
            print(line)
    if cp.stderr:
        for line in cp.stderr.splitlines():
            print(line)

def cd(path):
    """
    Change current directory to path, a string
    Uses os module chdir function so it does change the directory 
     of the Python session.  
    Invoking cd in a shell subprocess by sh('cd ...') does not.
    """
    os.chdir(path)

def pwd():
    """ 
    Print current working directory on stdout.
    Uses os module getcwd function, not a shell subprocess.
    """    
    print(os.getcwd())  # returns a string

def man(topic):
    """
    Print man page on topic, a string.
    Invokes the man command in a shell subprocess, writes output on stdout.    
    """
    manenv = os.environ.copy()
    manenv['MANWIDTH'] = str(width)
    sh('man ' + topic, shellenv=manenv)

def ls(path='.'):
    """
    Call the shell directory listing command ls -C for a compact listing.
    Argument is file or directory path string, default . the current directory. 
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh(f'ls -C -w {width} ' + path)

def lsl(path='.'):
    """
    Call the shell directory listing command ls -l for a long form listing,
     sorted alphabetically.
    Argument is file or directory path string, default . the current directory.    
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh('ls -l '+path)

def lslt(path='.'):
    """
    Call the shell directory listing command ls -lt for a long form listing,
     sorted most recent first.
    Argument is file or directory path string, default . the current directory.    
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh('ls -lt '+path)
