"""
bufimport.py -  provide functions to import or reload a module directly from 
                a text buffer, without having to write it out to a file.
"""

import importlib, sys
import text

# Copied from pysh.py.  For some reason globals() doesn't work with pysh.
main_globals = sys.modules['__main__'].__dict__

def bufstring(bufname):
    'Return buffer contents as one big string.'
    return ''.join(text.lines(bufname))

def breload_m(bufname, module):
    'Execute named buffer contents in module object (which already exists)'
    exec(bufstring(bufname), module.__dict__)

def bimport_m(bufname, modname):
    'Execute named buffer contents in new named module, save in sys.modules'
    # m = types.ModuleType(modname) # works but no longer 'preferred'
    # The following two lines are now 'preferred' to ModuleType
    spec = importlib.util.spec_from_loader(modname, loader=None, 
                                           origin='from buffer %s' % bufname)
    m = importlib.util.module_from_spec(spec)
    breload_m(bufname, m)
    main_globals[modname] = m # globals() here does not work, follow pysh.py
    sys.modules[modname] = m

def pyprefix(bufname):
    'If bufname ends with .py, return prefix, otherwise print msg, return None'
    if bufname.endswith('.py'):
        return bufname[:-3]
    else:
        print('? current buffer %s is not .py' % bufname)
        return None

def bimport():
    """
    Import the current buffer.
    Print message if buffer is not .py, or is already imported.
    """
    bufname = text.current
    modname = pyprefix(bufname)
    if modname:
        if modname not in sys.modules:
            bimport_m(bufname, modname)
            print('Module %s imported from buffer %s' % (modname, bufname))
        else:
            print('? %s already in sys.modules, use breload() instead' 
                    % modname)

def breload():
    """
    Reload the current buffer.
    Print message if buffer is not .py, or module not found in sys.modules.
    """
    bufname = text.current
    modname = pyprefix(bufname)
    if modname:
        if modname in sys.modules:
            m = sys.modules[modname]
            breload_m(bufname, m)
            print('Module %s reloaded from buffer %s' % (modname, bufname))
        else:
            print('? %s not in sys.modules, use bimport() instead' 
                    % modname)

