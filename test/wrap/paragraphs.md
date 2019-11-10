
paragraphs.md

Investigate formatting of wrapped paragraphs at github.

Here is a paragraph typed into edsel, typing RETURN at about
60 characters.  Here is more more more more more still more
more more more more more more more more more more even more
more more more more more more more moer more more yet more.

In the source text, the preceding paragraph has lines that end with the words:
... about  
... still more  
... even more  
... yet more  

In the source text, every line in the preceding paragraph ends with two spaces.
in order to force line breaks.
This is a little-known (to me) feature provided by github markdown.

This paragraph was typed with lines exceeding 80 characters, 1 
then used the edsel [J command with a parameter to wrap the text 2
to 65 characters, then marked the end of each line with digits 3
1..7 More more more more more more more more more more more more 4  
more more more more more more more more more more more more more 5
more more more still more more more more more more more more 6
more more more more more more more more more more more even more 7

Ah, we notice that the line above ending in 4 ends with two spaces.

This paragraph was typed with lines exceeding 80 characters, and was left with the extra long lines.
More more more more more more more more more more more more more more more more more more more still more
More more more more more more more more more more more more more more more more more more more even more
mire more more more more more more more more more more more more more more more more more more still more

The following paragraph is a cut-pasted copy of the preceding one, but wrapped using [J with 
fill_column = 65.

This paragraph was typed with lines exceeding 80 characters, and  
was left with the extra long lines. More more more more more  
more more more more more more more more more more more more more  
more still more More more more more more more more more more  
more more more more more more more more more more even more mire  
more more more more more more more more more more more more more  
more more more more more still more 

Oh, our homemade [J wrap left two blank lines at the end of each line above!

The following paragraph is a cut-pasted copy of the preceding one, 
but with initial indent 6 lines, then wrapped using [J with fill_column = 75,
and using Python textwrap.fill() 

      This paragraph was typed with lines exceeding 80 characters, and
      was left with the extra long lines. More more more more more   more
      more more more more more more more more more more more more   more
      still more More more more more more more more more more   more more
      more more more more more more more more even more mire   more more
      more more more more more more more more more more more   more more
      more more more still more

This paragraph is similar but with no initial indent and fill_column 69,
to get the line breaks in the same places.

This paragraph was typed with lines exceeding 80 characters, and
was left with the extra long lines. More more more more more   more
more more more more more more more more more more more more   more
still more More more more more more more more more more   more more
more more more more more more more more even more mire   more more
more more more more more more more more more more more   more more
more more more still more

This paragraph is inside an item so it should be indented, 
but wrapped:

- This is the header, the rest has 2 char indent and fill_column 71
  This paragraph was typed with lines exceeding 80 characters, and
  was left with the extra long lines. More more more more more   more
  more more more more more more more more more more more more   more
  still more More more more more more more more more more   more more
  more more more more more more more more even more mire   more more
  more more more more more more more more more more more   more more
  more more more still more

Notice how the two blank lines at the end of each line were preserved
in the wrapped text.




