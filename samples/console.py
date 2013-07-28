"""
console.py - skeleton console application for Piety.

Defines a class Console, with a getchar method that gets a single
character typed at the console keyboard, and adds it to a line buffer
(usually).  When getchar gets a line terminator character, it calls a
line processing function and passes the linebuffer to it.

The default line processing function simply echoes the line buffer to
the console display.  A different line processing function can be
passed as an optional argument to the constructor, so this same class
can act as the front end to any console application (where the user
types command lines on the keyboard).  The line processing function
can be the Python interpreter itself, so this class can act as Piety's
Python shell.

Other characters collected by getchar may be interpreted as line
editing characters.  The line buffer may be (re)displayed on the
console display when getchar runs.
"""

class Console(object):
    """
    Skeleton console application for Piety.  Has a getchar method that
    gets a single character typed at the console keyboard, and adds it to a
    line buffer (usually).  When getchar gets a line terminator
    character, it calls a line processing function and passes the
    linebuffer to it. Other characters collected by getchar may be
    interpreted as line editing characters.  The line buffer may be
    (re)displayed on the console display when getchar runs.
    """

    def __init__(self, prompt='piety>', line_terminator='\r', 
                 line_processor=None):
        """
        Creates a Console instance
        prompt - optional argument, prompt, default is 'piety>'
        line_terminator - optional argument, default is Return '\r'
        line_processor - optional argument, function to run on line
        buffer when getchar gets line terminator, default just echoes
        line buffer contents.
        """
        self.line_buffer = str()
        self.prompt = prompt
        self.line_terminator = line_terminator
        self.line_processor = line_processor if line_processor else self.echo

    def getchar(self):
        """
        Get character from console keyboard, add to line_buffer (usually).
        If character is line_terminator, call line processor on line buffer.
        Other characters may be interpreted as line editing characters.
        Line buffer may be redisplayed.
        """
        # FIXME handle single char input, for now use raw_input
        # so for now user must type one character and type RET
        # we can't use RET for line_terminator because raw_input strips it.
        ch = raw_input(self.prompt)[0]
        if ch == self.line_terminator:
            self.line_processor(self.line_buffer)
            self.line_buffer = str()
        else:
            self.line_buffer = self.line_buffer + ch
            # FIXME echo shouldn't be necessary when we have single char input
            self.echo(self.line_buffer)

    def echo(self, s):
        """
        Print s on console display
        """
        print s




    



