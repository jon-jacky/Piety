"""
pysht.py - Callable Python shell.  Can be embedded in any Python application,
            but was designed to work with the Piety scheduler and Console.
           
Defines the function 'mk_shell' whose parameters define a
configuration, which returns a function (a closure) that interprets a
single Python expression or statement.  This function is the callable
Python shell.  We use a closure so we can create different shells that
use different configurations.

At this time the only configuration parameter is the 'globals'
dictionary used by eval and exec to look up names and bind variables.

The default globals dictionary is from the __main__ module so the
shell returned by mk_shell behaves just like the usual top-level
interpreter.  But we could configure the shell differently.

To use pysht with any Python application: 

 import pysht
 pysh = pysht.mk_shell()
 command = "print 'Now it is', datetime.datetime.now()"
 pysh(command) # prints Now it is ...

To use pysht with Piety, pass the function returned by mk_shell to the
Console constructor, that makes the Console instance behave as a
Python shell:

 import console
 import pysht
 import sys
 shell = console.Console(prompt='pysh> ', command=pysht.mk_shell())

This code belongs in the Piety application module that uses the shell, not
here in the pysht module, so different shell instances can use
different configurations.

The command function returned by mk_shell simply passes the command
line to the Python eval function (for expressions) or the exec
statement (statements).  On eval and exec:

 http://docs.python.org/2/library/functions.html#eval 
 http://docs.python.org/2/reference/simple_stmts.html#exec
 http://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile-in-python
 http://lucumr.pocoo.org/2011/2/1/exec-in-python/

Pysht (rhymes with "fished") is the name of a river and a ghost town
on the Olympic peninsula in Washington state in the northwest USA.
The name is from the Clallam language, translated as "against the wind
or current"[1] or "where the wind blows from all directions"[3].
 
 1. http://en.wikipedia.org/wiki/Pysht_River 
 2. http://en.wikipedia.org/wiki/Pysht,_Washington
 3. http://www.ghosttowns.com/states/wa/pysht.html

"""

import sys, traceback

main_globals = sys.modules['__main__'].__dict__

def mk_shell(globals=main_globals):
    """
    Console expects a command function with one argument, the command line
    use mk_shell to make the command function with globals dictionary baked in
    accept the default globals to use the same dictionary the __main__ module
    """

    def shell(cmdline):
        """
        Pass cmdline to Python eval or exec to execute
        This is a closure that includes the globals dictionary 
        """
        try: # don't crash out of piety if exception, but print traceback
            try: # try eval, if it fails call exec
                # exec does not automatically print values so use eval if we can
                result = eval(cmdline, globals)
                # print out results just as in standard Python REPL
                if result == None:
                    pass
                elif isinstance(result,str):
                    print "'"+result+"'"
                else:
                    print result
                # statements (not exprs) like x = 42 crash eval with syntax error 
                #  so use exec for those
            except SyntaxError:
                exec cmdline in globals
        except BaseException as e:
          traceback.print_exc() # looks just like unhandled exception

    return shell
