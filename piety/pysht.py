"""
pysht.py - Python shell for Piety

Defines the command function passed to the Console constructor,
then makes that Console instance into a Python shell.

Simply passes the command function to the Python eval function (for
expressions) or the exec statement (statements).  On eval and exec:

 http://docs.python.org/2/library/functions.html#eval 
 http://docs.python.org/2/reference/simple_stmts.html#exec
 http://lucumr.pocoo.org/2011/2/1/exec-in-python/

Pysht is the name of a river and a ghost town on the Olympic peninsula
in Washington state in the northwest USA.  The name is from the
Clallam language, translated as "against the wind or current"[1] or
"where the wind blows from all directions"[3].
 
 1. http://en.wikipedia.org/wiki/Pysht_River 
 2. http://en.wikipedia.org/wiki/Pysht,_Washington
 3. http://www.ghosttowns.com/states/wa/pysht.html

"""

def python(line):
    """
    Pass line to Python interpreter, with the global environment
    """
    gbls = globals() # just call it once
    try:
        # if line is an expression, evaluate and print value
        print eval(line, gbls)
    except SyntaxError:
        # statements (not exprs) like x = 42 crash eval with syntax error 
        # but exec does *not* print value
        exec line in gbls

# To use it:
#  from console import Console
#  import pysht
#  shell = Console(prompt='piety>>> ', command=pysht.python)
# But create shell in application not here in pysht module
#  so we can have multiple shell instances
