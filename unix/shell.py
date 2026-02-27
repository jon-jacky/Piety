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
import contextlib # redirect_stdout stores intermediate results in StringIO
import io # StringIO

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
    Call the shell directory listing command ls -C for a compact listing,
    and -F to indicate directories with / suffix.
    Argument is file or directory path string, default . the current directory. 
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh(f'ls -C -F -w {width} ' + path)

def lsl(path='.'):
    """
    SUPERCEDED BY lsl DERIVED FROM lstfx BELOW - NOT! Restore this simpler form
    Call the shell directory listing command ls -l for a long form listing,
     sorted alphabetically.  Also -a to show parent, -F to indicate directories
    Argument is file or directory path string, default . the current directory.    
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh('ls -alF '+path)

def lslt(path='.'):
    """
    SUPERCEDED BY lslt DERIVED FROM lstfx BELOW - NOT! Restore simpler form
    Call the shell directory listing command ls -lt for a long form listing,
     sorted most recent first. Also -a to show parent, -F to indicate directories
    Argument is file or directory path string, default . the current directory.    
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh('ls -altF '+path)
         
def lslxfXXX(path='.', cmd='ls -l'):
    """
    NOW HIDE THIS WITH XXX - we *don't* want the extra formatting with path
    lsl with eXtra Formatting.
    In each line, prefix filename at the end with its path (from path= arg).
    
    Call cmd, a shell directory listing command such as 'ls -l' or 'ls -lt'
     for a long form listing, default cmd is 'ls -l' to sort alphabetically.
    path is file or directory path string, default '.' the current directory.    
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    lslines = io.StringIO('')
    with contextlib.redirect_stdout(lslines):
        sh(cmd+' '+path)
    for line in lslines.getvalue().splitlines():
        stats, spc, fname = line.rpartition(' ')
        pathstr = '' if path == '.' else path + '/'
        print(stats + spc + pathstr + fname)
        
def lslXXX(path='.'): lslxf(path, 'ls -l')

def lsltXXX(path='.'): lslxf(path, 'ls -lt')

