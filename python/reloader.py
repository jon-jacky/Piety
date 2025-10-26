"""
reloader.py - MicroPython does not provide a module reload function.
              Here we provide two variabts
"""

import sys

def reinit(module):
    """
    Reinitialize a module: delete it from sys.modules, then import it 
    again.   This has the effect of re-initializing all its variables.
    The argument is the module object.
    Returns the newly imported module object.
    """
    module_name = module.__name__
    del sys.modules[module_name]
    # THIS DOES NOT WORK
    # APPARENTLY THE del STATEMENT DOES NOT DELETE module
    # SO __import__ APPARENTLY DOES NOTHING
    #print('module ', module)
    #print('sys.modules[module_name] ', sys.modules[module_name])
    return __import__(module_name)


def reload(module_path):
    """
    Imitate CPython reload.  Execute the current version of the module 
    source file in the context of the existing module object in sys.modules.
    Depending on how the module is written, this can load the revised 
    versions of functions but preserve the values of selected variables.
    The argument module_path is a string, the path to the module source file
    always including 'module_name.py' and possibly including directories.
    Returns the reloaded module object.
    """
    module_basename = module_path.rpartition('/')[-1] # remove directories
    module_name = module_basename.partition('.')[0] # remove '.py'  NB no rpart
    module = sys.modules[module_name]
    return exec(open(module_path).read(), module.__dict__)

