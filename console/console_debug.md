
console_debug
=============

The *console_debug* module is an instrumented version of *console*.
It logs data and timestamps to an internal data structure as the user
types and the display updates.  We made it to help us investigate the
problem described in the *Bugs* section at the end of
[demo.md](../scripts/demo.md)

The *console_debug* module imports *getkey_debug* and *display_debug*,
which are also instrumented.  In all three modules, lines marked DEBUG
capture and log data or timestamps.

This sample session show how to use *console_debug*:

Run the module.  It prints a prompt *>*, then you type a line of text.
In this sample, after typing *ghi* to finish the line, type *ctrl-b*
three times to move the cursor backward one character each time, then
type *alt-b* to move the cursor backward one word, over *def*.  Then
type *alt-f* to move the cursor forward one word, back to *ghi*.  Then
type RET to echo the line, then type *ctrl-z* to exit the program and
return to the top level Python prompt, *>>>*.  

At the prompt, type *echo.debug_line*, the name of the data structure
that contains the logged data.  Python prints the data, which includes
the typed characters, timestamps, the computed output display control
strings, and other data -- see the DEBUG lines in the source modules
for details:

    ...$ python3 -im console_debug
    > abc def ghi
    abc def ghi
    Stopped
    >>> echo.debug_line
    [1674768408.479042, 'a', 1674768408.479058, 'a', <bound method
    Console.insert_char of <__main__.Console object at 0x10bc73070>>, 0,
    1674768408.8378649, 'b', 1674768408.837879, 'b', <bound method
    Console.insert_char of <__main__.Console object at 0x10bc73070>>, 1,
    ...  
    ... 10, 1674768416.198386, '\x02', 1674768416.198408, '\x02', <bound
    method Console.backward_char of <__main__.Console object at
    0x10bc73070>>, 9, 1674768419.710131, '\x1b', 1674768419.710151, '',
    1674768419.710179, 'b', 1674768419.7101922, '\x1bb', <bound method
    Console.backward_word of <__main__.Console object at 0x10bc73070>>, 8,
    3, 4, 7, 1674768419.710294, '\x1b[7G', 1674768421.9740732, '\x1b',
    1674768421.974092, '', 1674768421.9741209, 'f', 1674768421.974133,
    '\x1bf', <bound method Console.forward_word of <__main__.Console
    object at 0x10bc73070>>, 4, 7, 8, 11, 1674768421.9742012, '\x1b[11G', ...  
    ...
	
In the preceding sample, *console_debug* does not run as a Piety task.
The *console_task* module imports *console_debug* and runs it as a
Piety task.  The session is almost the same, except at the beginning
you see the Python prompt *>>>* where you have to type *main()* to
start the program.  Later, after you type *ctrl-z* to exit the
program, you have to type *ctrl-c* to interrupt Piety tasking and
return to the Python *>>>* prompt:

    ...$ python3 -im console_task
    >>> main()
    > abc def ghi
    abc def ghi
    Stoppedt
    ^CTraceback (most recent call last):
    ...
    >>> echo.debug_line
    [1674769057.810901, 'a', 1674769057.810945, 'a', <bound method
    Console.sinsert_char of <console_debug.Console object at 0x10d68adc0>>,
    0, 1674769058.153655, 'b', ...

Revised Jan 2023
