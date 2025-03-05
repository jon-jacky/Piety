"""
host.py - Python functions that wrap commands to the host operating system.

          One function here invokes the host shell and several invoke particular 
          host shell commands, so you can use the host shell without exiting the
          Python session.  These functions run the host shell in a subprocess.
          
          Several functions here call the Python standard library directly.
          These functions do not use the host shell or a subprocess.
          
          These functions all write command output on the standard output, 
          so the output can be redirected.
"""        

import subprocess, os, pydoc

def sh(command):
    """
    Invoke shell command, a string, in a shell subprocess.
    See https://docs.python.org/3/library/subprocess.html
    Capture command output and print it on the calling process standard output,
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

def ls(path='.'):
    """
    Call the shell directory listing command ls -C for a compact listing.
    Argument is file or directory path string, default . the current directory. 
    Invokes the ls command in a shell subprocess, writes output on stdout.
    """
    sh('ls -C '+path)

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
   
def man(topic):
    """
    Print man page on topic, a string.
    Invokes the man command in a shell subprocess, writes output on stdout.    
    """
    sh('man ' + topic)

def help(topic):
    """
    Print help on topic, a Python object: module, function etc. Prints to stdout.
    Uses the pydoc module render_doc function, does not invoke a shell process.
    """
    helptext = pydoc.render_doc(topic, "Help on %s") # one big string
    for line in helptext.splitlines():
        print(line)
        
    
