"""
render.py  -  Render HTML into an editor text buffer
"""
 
from html.parser import HTMLParser
from pathlib import Path

import sked as ed
import edsel as fr # fr for frame

class HTML2Text(HTMLParser):
    """
    Render HTML to text, using Python standard library HTMLParser
    
    Based on Andrej Kesely's answer in Stack Overflow:
    Extracting Text / Parse Text with html.parser (Python)
    https://stackoverflow.com/questions/64695883/extracting-text-parse-text-with-html-parser-python
    
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
        if tag in ('p', 'h1'):
            self.capture = True
                                                    
    def handle_endtag(self, tag):
        if tag in ('p', 'h1'):
            self.capture = False
            
    def handle_data(self, data):
        if self.capture: 
            self.data.append(data)
             
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
    
    # From here on, the code is almost exactly like in get.py fcn g()
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.filename = bufname # replace filename created by e() with url
    ed.buffers[bufname]['filename'] = bufname # replace filename created by e()
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    # Fill in buffer text
    for line in html2text.data:
        ed.buffer.append(line.rstrip() + '\n') # just one terminal \n  
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
