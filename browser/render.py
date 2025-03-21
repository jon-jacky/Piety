"""
render.py  -  Render HTML into an editor text buffer.
"""
 
from html.parser import HTMLParser
from pathlib import Path
import textwrap

import sked as ed
import edsel as fr # fr for frame

# div class="..." special case div tags at particular web sites
# div with these classes are formatted like paragraphs.
# Other div are ignored, do not appeear in rendered output.
divclasses = ('copy post',  # www. ask.metafilter.com: posts, asks on front page
              'copy',       # metafilter: top of post or answer page
              'comments',   # metafilter: each answer or each comment
              'comments best',  # metafilter: answers marked best
              'comments bestleft', # metafilter: asker's remark on answer page
              'commtext c00', # news.ycombinator.com (Hacker News): comment
              'toptext', # ycombinator: text at top of Ask HN
              'os', # www.tbray.org/ongoing/ front page article links/summaries 
              )
 
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
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'pre'):
            if self.tags and self.tags[-1] == 'div':  # we're inside div
                self.output += '\n\n' + textwrap.fill(self.paragraph) 
            self.paragraph = '' # start a new paragraph
        if tag == 'a':  # <a href=linkurl>...</a> 
            self.linkurl = dict(attrs).get('href','')
        if tag == 'img': #  <img src="..."  alt="..." ... optional attrs .../>
            # No endtag - handle data and output here
            alt = dict(attrs).get('alt', '')
            self.output += '\n\n  [ %s ]' % (alt if alt else 'Image')
        if tag == 'br':
            # No endtag, no data. Treat br starttag like p endtag,then starttag
            self.output += '\n' + textwrap.fill(self.paragraph) # just one \n
            self.paragraph = '' # now start new paragraph                         
        # List of only the tags we handle.  We don't handle most tags.
        # BUT not img or br  because thre is nothing to capture and no endtag
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 
                    'pre', 'strong', 'em', 'a' ):
            # Do not push unmatched <p> inside <div> onto list of tags
            if ((tag != 'p')
                or (tag == 'p' and (not self.tags or self.tags[-1] != 'div'))):
                self.tags.append(tag)  # push tag onto stack of tags
            self.capture = True

        # Special case div tags at particular web sites, see divclasses above.
        # Some code here is repeated from the genereal case (right above)
        # but this is necessary to keep the special case div code separate. 
        # and make the similarities apparent.
        if tag == 'div':
            divclass = dict(attrs).get('class', '') 
            if divclass in divclasses:
                # Treat div with these classes just like paragraph
                self.paragraph = '' # start a new paragraph
                self.tags.append(tag)  # push div tag onto stack of tags
                self.capture = True

    def handle_endtag(self, tag):
        if tag in ('p', 'h1', 'h2', 'h3', 'h4'):
            # data can be long string. fill() can insert \n to break lines
            # precede each paragraph by an empty line
            self.output += '\n\n' + textwrap.fill(self.paragraph)
        if tag == 'li':
            self.output += '\n\n-- ' + textwrap.fill(self.paragraph) # bullet
        if tag == 'pre':
            self.output += '\n\n' + self.paragraph # do NOT fill
        # Again, list of only the tags we handle - BUT not img, not br
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 
                    'pre', 'strong', 'em', 'a'):
            if self.tags:  # tags list not empty, guard against unmatched tag
                self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False
                
        # Special case for div at particular web sites
        # For now treat it just like a paragraph.
        # Repeats some code from above but needed to separate out this case.
        if tag == 'div': 
            # data can be long string. fill() can insert \n to break lines
            # precede each paragraph by an empty line
            self.output += '\n\n' + textwrap.fill(self.paragraph)
            self.paragraph = '' # re-initialize to avoid duplication
        if tag == 'div':
            if self.tags:  # tags list not empty, guard against unmatched tag
                self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False
                                                                
    def handle_data(self, data):
        if self.capture: 
            tag = self.tags[-1]
            if tag in ('p', 'li','h1','h2','h3','h4', 'pre'):
                self.paragraph += data # fill self.paragraph in handle_endtag
            if tag in ('strong', 'em'):
                self.paragraph += f' *{data}* ' # these data go in same para.
            if tag == 'a': # hypertext link, usually href=...
                self.linknum += 1 # footnotes count up from 1 not 0
                self.links.append(self.linkurl) # linkurl from handle_starttag
                self.paragraph += f'_{data.strip()}_ [{self.linknum}]'

            # Special case for div tags at particular web sites
            # Treat just like paragraph
            if tag == 'div':
                ### breakpoint() # DEBUG so we can examine div data
                self.paragraph += data # fill self.paragraph in handle_endtag
                            
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
    baseurl = ed.filename # original web site url, needed by relative urls.
    saved_bufname = ed.prev_bufname # prepare for unwanted assignment by fr.e()
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.prev_bufname = saved_bufname # back out unwanted assignment by fr.e()
    ed.filename = baseurl # replace filename created by e() with web site url
    ed.buffers[bufname]['filename'] = bufname # replace filename created by e()
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    for line in parser.output.rsplit('\n'): # make list of lines from string
        ed.buffer.append(line + '\n') # each line in buffer must end with \n    
    ed.buffer += ['\n','\n','Links\n', '\n'] # Links header we can search for
    for ilink in range(parser.linknum):
        ed.buffer.append(f'{ilink+1}. {parser.links[ilink]}\n')         
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()

