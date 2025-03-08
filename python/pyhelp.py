"""
pyhelp.py - The help function here calls the Python interpreter help. But
unlike builtin Python help, it does not rewrite the screen, it just writes
the help text to the standard output, which can be redirected anywhere.
"""

import pydoc
                                
# Alias for builtin Python help so we can still use it after we define our help.
# phelp = help # FIXME wait on this

def help(topic):
    """
    Print help on topic, a Python object: module, function etc. Prints to stdout.
    Uses the pydoc module render_doc function, does not invoke a shell process.
    Unlike builtin Python help, this function does not rewrite the screen,
     it just writes the help text to the standard output.
    To use builtin Python help, use the alias phelp defined above.
    FIXME: Unlike builtin Python help, this fcn does not accept string arguments.
    """
    helptext = pydoc.render_doc(topic, "Help on %s") # one big string
    for line in helptext.splitlines():
        print(line)
     
