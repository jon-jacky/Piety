
paragraphs.md

Investigate formatting of wrapped paragraphs at github.

Here is a paragraph typed into edsel, typing RETURN at about
60 characters.  Here is more more more more more still more
more more more more more more more more more more even more
more more more more more more more moer more more yet more.

In the source text, the preceding paragraph has lines that end with
... about
... still more
... even more
... yet more

In the source text, every line in the preceding paragraph ends with two spaces
in order to force line breaks.

But the edsel cursor, when sent to the end of the line, does not show the two spaces.
and !ed.buf.lines[10:15] shows each has no trailing blanks - edsel code
must trim them off!

This paragraph was typed with lines exceeding 80 characters, then used the
edsel [J command to wrap the text to the old default width, 80 characters. More
more more more more more more more more more more more more more more more more
more more more more more more more more more more more still more more more
more more more more more more more more more more more more more more more more
even more

This paragraph was typed with lines exceeding 80 characters, and was left with the extra long lines.
More more more more more more more more more more more more more more more more more more more still more
More more more more more more more more more more more more more more more more more more more even more
mire more more more more more more more more more more more more more more more more more more still more


