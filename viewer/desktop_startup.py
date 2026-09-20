# desktop_startup.py invoked from desktop.py   
# Assumes Piety is the current directory. It uses relative paths to load files.
import edsel, frame as fr
fr.e('viewer/keys.txt')
fr.e('viewer/viewer.py')
fr.e('viewer/README.md')
fr.e('browser/urls.py')
fr.e('viewer/desktop.txt') # load this one last, so it appears in viewer
# Put some text in the Python REPL
print("""
>>> # This is the Python interpreter.
>>> # Type alt-X to enter the interpreter REPL.
>>> # Type ed() to return to return from the REPL to editing in windows.
>>> """)
from edsel import ed # overwrite ed imported from frame dmacs get render ...
ed() # start display editing in viewer window

