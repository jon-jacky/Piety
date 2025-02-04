"""
render.py  -  Render HTML into an editor text buffer.
"""
 
from html.parser import HTMLParser
from pathlib import Path
import textwrap

import sked as ed
import edsel as fr # fr for frame

class HTML2Text(HTMLParser):
    """
    Render HTML to text, using Python standard library HTMLParser.
    
    Based on Andrej Kesely's answer in Stack Overflow:
    Extracting Text / Parse Text with html.parser (Python)
    https://stackoverflow.com/questions/64695883/extracting-text-parse-text-with-html-parser-python
    Also informed by Andreas' and Jorge Perez' answers in 
    Converting html to text with Python
    https://stackoverflow.com/questions/14694482/converting-html-to-text-with-python
        
    Example:                         
    from render import HTML2Text
    html2text = HTML2Text()
    html2text.feed(''.join(ed.buffer)) # requires string, not list of string
    for line in html2text.data: print(line.rstrip()) #  remove extra \n
    """
    def __init__(self):
        super().__init__()
        self.data = []
        self.capture = False
                            
    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            self.capture = True
                                                    
    def handle_endtag(self, tag):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            self.capture = False
            
    def handle_data(self, data):
        if self.capture: 
            self.data.append('\n' + data) # blank lines between paragraphs
             
def r():
    """
    Render current buffer, a downloaded HTML web page, to a new text buffer.
    Current buffer is named basename or basename.html
    New text buffer is named basename.txt
    
    Name 'r' for 'render'.  We also have sked.r, reverse search
    """ 
    html2text = HTML2Text()
    html2text.feed(''.join(ed.buffer)) # requires string, not list of string

    path = Path(ed.bufname) # extract ppath, a Path object, from Parse object
    bufname = path.stem + '.txt'  # path.stem is basename index.html -> index
    
    # From here on, the code is similar to get.py fcn g()
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.filename = bufname # replace filename created by e() with url
    ed.buffers[bufname]['filename'] = bufname # replace filename created by e()
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    # Fill in buffer text
    for element in html2text.data:  # each element is a <p> or <h1> or ...
        ed.buffer.append('\n') # separate elments with empty lines
        # element is a long string. fill() inserts \n's to define lines ...
        filled = textwrap.fill(element).rsplit('\n') # ... rsplit() makes list.
        for line in filled:
            ed.buffer.append(line + '\n') # each line in buffer ends with \n
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
