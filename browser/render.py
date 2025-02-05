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
    parser = HTML2Text()
    parser.feed(''.join(ed.buffer)) # requires string, not list of string
    for line in parser.data: print(line.rstrip()) #  remove extra \n
    """
    def __init__(self):
        super().__init__()
        # self.output is onw big string with embedded \n indicating lines
        self.output = ''  # Accumulate parsed and formatted data here.
        self.capture = False # Not in any supported tag, discard html 
        # self.tags is needed so handle_data can handle each tag differently.
        # self.tags is a list so we can append and pop tags for nested elements
        # self.tags[-1] is the tag for the current, possibly deeply nested elt.
        self.tags = [] # empty tags list means we are not in any supported tag.
        
    def handle_starttag(self, tag, attrs):
        # List of only the tags we handle.  We don't handle most tags.
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'strong', 'em'):
            self.tags.append(tag)
            self.capture = True
                                                    
    def handle_endtag(self, tag):
        # Again, list of only the tags we handle
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'strong', 'em'):
            self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False
                                        
    def handle_data(self, data):
        if self.capture: 
            tag = self.tags[-1]
            if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
                self.output += '\n' # Separate this element with empty line.
                # data can be long string. fill() can insert \n to break lines
                self.output += textwrap.fill(data) + '\n' # add final linebreak
            elif tag in ('strong', 'em'):
                self.output += f' *{data}* ' # these data go in same line
            else:
                pass  # more tags to come
                
def r():
    """
    Render current buffer, a downloaded HTML web page, to a new text buffer.
    When current buffer is named basename or basename.html,
    then new text buffer is named basename.txt     
    Name 'r' for 'render'.  We also have sked.r, reverse search
    """ 
    global parser # make this global so we can inspect parser.output in REPL
    parser = HTML2Text()
    parser.feed(''.join(ed.buffer)) # requires string, not list of string

    path = Path(ed.bufname) # create Path object from ed.bufname string
    bufname = path.stem + '.txt'  # path.stem is basename index.html -> index
    
    # From here on, the code is similar to get.py fcn g()
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.filename = bufname # replace filename created by e() with url
    ed.buffers[bufname]['filename'] = bufname # replace filename created by e()
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    for line in parser.output.rsplit('\n'): # make list of lines from string
        ed.buffer.append(line + '\n') # each line in buffer ends with \n    
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
  

    
