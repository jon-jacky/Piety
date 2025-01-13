"""
host.py - Python wrappers for host shell and some particular shell commands,
          so you can use the shell without exiting the Python session.
"""        

import subprocess, os, pydoc

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

def cd(path):
    'Change current directory to path, a string'
    os.chdir(path)

def pwd():
    'Print current working directory'
    print(os.getcwd())  # returns a string

def ls(path='.'):
    """
    Call the shell directory listing command ls -C for a compact listing.
    Argument is file or directory path string, default . the current directory.    
    """
    sh('ls -C '+path)

def lsl(path='.'):
    """
    Call the shell directory listing command ls -l for a long form listing,
     sorted alphabetically.
    Argument is file or directory path string, default . the current directory.    
    """
    sh('ls -l '+path)

def lslt(path='.'):
    """
    Call the shell directory listing command ls -lt for a long form listing,
     sorted most recent first.
    Argument is file or directory path string, default . the current directory.    
    """
    sh('ls -lt '+path)
   
def man(topic):
    'Print man page on topic, a string'
    sh('man ' + topic)

def help(topic):
    'Print help on topic, a Python object - module, function etc.'
    helptext = pydoc.render_doc(topic, "Help on %s") # one big string
    for line in helptext.splitlines():
        print(line)
        
    
