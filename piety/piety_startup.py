# piety_startup.py invoked from piety.py   
# Assumes Piety is the current directory. It uses relative paths to load files.
import pmacs, edsel as fr
fr.e('viewer/keys.txt')
fr.e('viewer/viewer.py')
fr.e('viewer/README.md')
fr.e('browser/urls.py')
fr.e('viewer/desktop.txt') # load this one last, so it appears in viewer
# Put some text in the Python REPL
print("""
>>> # This is the Python interpreter.
>>> # Type alt-X to enter the interpreter.
>>> # Type apm() to return to visual editing in windows.
>>> """)
pmacs.pm()

