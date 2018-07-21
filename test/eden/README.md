
eden tests
==========

Tests for *eden.py*.  The test scripts can include sequences of keycodes
so full screen editing can be tested, by simulating the keystrokes that a 
user might type.

The test scripts are simply Python modules.  To run the test once,
just import the module at the *eden* command line using the *!* prefix
used with any Python statement:

    :!import dnupdn

Each module can only be imported once in a Python session, so to run
the test again in the same session, call the module's *main* function:

    :!dnupdn.main()

Revised July 2018
