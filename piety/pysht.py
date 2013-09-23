"""
pysht.py - Python shell for Piety

Defines the command function 'mk_shell' that returns a function (a
closure) that is passed to the Console constructor, that makes the
Console instance behave as a Python shell.

We use mk_shell to make a closure so we can create different shells
that use different modules to lookup names and bind variables.
Usually we use the __main__ module so the shell returned by mk_shell
behaves just like the usual top-level interpreter.   But we could 
configure the returned shell differently.

To use it:
 from console import Console
 import pysht
 import sys
 gbls = sys.modules['__main__'].__dict__
 shell = Console(prompt='piety>>> ', command=pysht.mk_shell(gbls))

Put this code in the application module that uses the shell, not here
in pysht module, so different shell instances can use different
modules.

The command function returned by mk_shell simply passes the command
line to the Python eval function (for expressions) or the exec
statement (statements).  On eval and exec:

 http://docs.python.org/2/library/functions.html#eval 
 http://docs.python.org/2/reference/simple_stmts.html#exec
 http://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile-in-python
 http://lucumr.pocoo.org/2011/2/1/exec-in-python/

Pysht is the name of a river and a ghost town on the Olympic peninsula
in Washington state in the northwest USA.  The name is from the
Clallam language, translated as "against the wind or current"[1] or
"where the wind blows from all directions"[3].
 
 1. http://en.wikipedia.org/wiki/Pysht_River 
 2. http://en.wikipedia.org/wiki/Pysht,_Washington
 3. http://www.ghosttowns.com/states/wa/pysht.html

"""

def mk_shell(globals):
    """
    Console expects a command function with one argument, the command line
    use mk_shell to make the command function with globals dictionary baked in
    globals is sys.modules['__main__'].__dict__ to make shell behave like usual
    """

    def shell(cmdline):
        """
        Pass cmdline to Python to execute, with the globals dictionary
        This is a closure with variable globals from the environment
        """
        try:
            # exec does not automatically print values so use eval if we can
            result = eval(cmdline, globals)
            # strings print out with enclosing single quotes just like usual
            print "'"+result+"'" if isinstance(result,str) else result
            # statements (not exprs) like x = 42 crash eval with syntax error 
            #  so use exec for those
        except SyntaxError:
            exec cmdline in globals

    return shell
