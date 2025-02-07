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
        # self.tags is a list -- a stack -- of tags for nested elements.
        # self.tags[-1] is top, tag for the current, possibly deeply nested elt.
        self.tags = [] # empty tags list means we are not in any supported tag.
        # handle_data accumulates data in self.paragraph,
        # handle_endtag formats self.paragraph
        self.paragraph = ''
        # Each link is numbered in place in the buffer like a footnote.
        # Then all the numbered link URLs are printed at the bottom of the buf.
        self.linknum = 0 # footnote number, first link gets linknum 1
        self.links = [] # indexed 0 .. final linknum - 1
        self.linkurl = '' # assigned by handle_starttag
        self.placeholder = 'https://nowhere.com/unknown.html'
                 
    def handle_starttag(self, tag, attrs):
        # List of only the tags we handle.  We don't handle most tags.
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            self.paragraph = '' # start a new paragraph
        if tag == 'a':  # <a href=linkurl>...</a> 
            self.linkurl = attrs[0][1] # assumes attrs[0] is ('href', url)
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'strong', 'em', 'a' ):
            self.tags.append(tag)  # push tag onto stack of tags
            self.capture = True
                                                    
    def handle_endtag(self, tag):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            # data can be long string. fill() can insert \n to break lines
            # precede each paragraph by an empty line
            self.output += '\n\n' + textwrap.fill(self.paragraph)
        # Again, list of only the tags we handle
        if tag in ('p', 'h1', 'h2', 'h3', 'h4', 'strong', 'em', 'a'):
            self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False
                                        
    def handle_data(self, data):
        if self.capture: 
            tag = self.tags[-1]
            if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
                self.paragraph += data # fill self.paragraph in handle_endtag
            elif tag in ('strong', 'em'):
                self.paragraph += f' *{data}* ' # these data go in same para.
            elif tag == 'a': # hypertext link, usually href=...
                self.linknum += 1 # footnotes count up from 1 not 0
                self.links.append(self.linkurl) # linkurl from handle_starttag
                self.paragraph += f'_{data.strip()}_ [{self.linknum}]'
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
        ed.buffer.append(line + '\n') # each line in buffer must end with \n    
    ed.buffer.append('\n\n')
    for ilink in range(parser.linknum):
        ed.buffer.append(f'{ilink+1}: {parser.links[ilink]}\n')         
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
  

    
