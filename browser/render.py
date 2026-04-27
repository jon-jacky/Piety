"""
render.py  -  Render HTML into an editor text buffer.
"""
 
from html.parser import HTMLParser
from pathlib import Path
import textwrap

import sked as ed
import edsel as fr # fr for frame
import get # get.url get.title and get.g() are used here
import key, dmacs # for adding keycodes to keymap

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

# span class="..." special case span tags at particular web sites
# span with these classes are formatted like paragraphs.
# Other span are ignored, do not appeear in rendered output.
spanclasses = ('titleline',  # HN item title with link to non-HN article
              )
              
# Do not show [ Image ] in rendered output for these text-only sites
noimage = ('https://news.ycombinator.com/', # Hacker News
            )

width = 70 # window width for textwrap.fill(text, width) # FIXME? panel width

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
        self.showimage = True # default, show [ Image ] or [ alt text ]
        for nurl in noimage:
            if url.startswith(nurl):  # global url assigned in render()
                self.showimage = False # do not show [ Image ] in this page
                
    def handle_starttag(self, tag, attrs):
        if tag in ('title', 'p', 'li', 'h1', 'h2', 'h3', 'h4', 
                    'pre', 'noscript'):
            if self.tags and self.tags[-1] == 'div':  # we're inside div
                self.output += '\n\n' + textwrap.fill(self.paragraph, width) 
            self.paragraph = '' # start a new paragraph
        if tag == 'a':  # <a href=linkurl>...</a> 
            self.linkurl = dict(attrs).get('href','')
        if tag == 'img': #  <img src="..."  alt="..." ... optional attrs .../>
            # No endtag - handle data and output here
            alt = dict(attrs).get('alt', '')
            if self.showimage:
                self.output += '\n\n  [ %s ]' % (alt if alt else 'Image')
        if tag == 'br':
            # No endtag, no data. Treat br starttag like p endtag,then starttag
            self.output += '\n' + textwrap.fill(self.paragraph, width) # one \n
            self.paragraph = '' # now start new paragraph                         
        # List of only the tags we handle.  We don't handle most tags.
        # BUT not img or br  because thre is nothing to capture and no endtag
        if tag in ('title', 'p', 'li', 'h1', 'h2', 'h3', 'h4', 
                    'pre', 'strong', 'em', 'a', 'noscript'):
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

        # Special case span tags at particular web sites, see spanclasses above.
        # Just copied code div classes right above
        if tag == 'span':
            spanclass = dict(attrs).get('class', '') 
            if spanclass in spanclasses:
                # Treat span with these classes just like paragraph
                self.paragraph = '' # start a new paragraph
                self.tags.append(tag)  # push span tag onto stack of tags
                self.capture = True

    def handle_endtag(self, tag):
        if tag in ('title', 'p', 'h1', 'h2', 'h3', 'h4', 'noscript'):
            # data can be long string. fill() can insert \n to break lines
            # precede each paragraph by an empty line
            self.output += '\n\n' + textwrap.fill(self.paragraph, width)
        if tag == 'li':
            self.output += '\n\n-- ' + textwrap.fill(self.paragraph, width) # bullet
        if tag == 'pre':
            self.output += '\n\n' + self.paragraph # do NOT fill
        # Again, list of only the tags we handle - BUT not img, not br
        if tag in ('title', 'p', 'li', 'h1', 'h2', 'h3', 'h4', 
                    'pre', 'strong', 'em', 'a', 'noscript'):
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
            self.output += '\n\n' + textwrap.fill(self.paragraph, width)
            self.paragraph = '' # re-initialize to avoid duplication
        if tag == 'div':
            if self.tags:  # tags list not empty, guard against unmatched tag
                self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False

        # Special case for span at particular web sites
        # Just copy div code above
        if tag == 'span': 
            # data can be long string. fill() can insert \n to break lines
            # precede each paragraph by an empty line
            self.output += '\n\n' + textwrap.fill(self.paragraph, width)
            self.paragraph = '' # re-initialize to avoid duplication
        if tag == 'span':
            if self.tags:  # tags list not empty, guard against unmatched tag
                self.tags.pop()
            if not self.tags: # tags list empty, not in any supported tag
                self.capture = False
                                                                
    def handle_data(self, data):
        # global title # No longer needed - use get.title instead
        if self.capture: 
            tag = self.tags[-1]
            if tag in ('title', 'p', 'li','h1','h2','h3','h4', 'pre', 'noscript'):
                self.paragraph += data # fill self.paragraph in handle_endtag
            #if tag == 'title': # No longer needed - use get.title instead
            #    title = data # global title, so we can use it to make bufname
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

            # Special case for span tags at particular web sites
            # Copy div code right above
            if tag == 'span':
                ### breakpoint() # DEBUG so we can examine div data
                self.paragraph += data # fill self.paragraph in handle_endtag
 
url = ''  # Make URL global so HTML2Text methods can use it
                            
def r(aurl):
    """
    Render current buffer, a downloaded HTML web page, to a new text buffer.
    Name 'r' for 'render'.  We also have sked.r, reverse search
    aurl arg is only so we can put url in first line at top of rendered page.
    When current buffer is named basename or basename.html,
    new text buffer is named basename.htxt, distinguish from other .txt buffers
    """ 
    global parser # make this global so we can inspect parser.output in REPL
    global url # make this global so methods in HTML2Text can see it.
    # global title # make this global so we can assign default # use get,title
    url = aurl
    # title = 'No title' # default # Not needed - now use get.title
    parser = HTML2Text()
    parser.feed(''.join(ed.buffer)) # requires string, not list of string
    bufname = get.title[:12].replace(' ','-') + '.htxt' #M-o can't handle space
                        
    # From here on, the code is similar to get.py fcn g()
    baseurl = ed.filename # original web site url, needed by relative urls.
    saved_bufname = ed.prev_bufname # prepare for unwanted assignment by fr.e()
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.prev_bufname = saved_bufname # back out unwanted assignment by fr.e()
    ed.filename = baseurl # replace filename created by e() with web site url
    ed.buffers[bufname]['filename'] = bufname # replace filename created by e()
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    ed.buffer += [ url, '\n'] # Put page URL on first line
    for line in parser.output.rsplit('\n'): # make list of lines from string
        # Hack: Filter out duplicate empty lines, not sure where they come from.
        if not (line == '' and ed.buffer[-1] == '\n'):
            ed.buffer.append(line + '\n') # each line in buffer ends with \n    
    ed.buffer += ['\n','Links\n', '\n'] # Links header we can search for
    for ilink in range(parser.linknum):
        ed.buffer.append(f'{ilink+1}. {parser.links[ilink]}\n')         
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()

# Rendering functions that use functions from get module

def gr(url):
    'Get and Render web page at url'
    get.g(url)
    r(url)
    
def grx():
    'Get and Render web page at url eXtracted from current line in buffer'
    get.gx()
    render.r(get.url) # gx assigns get.url

def grf(n):
    'Get and render web page whose URL is in footnote n'
    get.gf(n)
    r(get.url) # gf assigns get.url
     
def grfx():
    'Get and Render web page at next Footnote eXtracted from current line.'
    gfx()
    render.r(url) # gfx assigns global url

def hnitem(item_number):
    'Get the HN item (page) with the given integer (not string) item number'
    gr('https://news.ycombinator.com/item?id=' + str(item_number))
    
# Add keycodes for browser operations to keymap 
dmacs.keymap[key.M_r] = r # render html from current buf. to .txt .buf
# key.C_o entry is now assigned in viewer.py
# dmacs.keymap[key.C_o] = grx # get and render page at URL on current line
dmacs.keymap[key.M_s] = grfx # get and render page at next footnote ref on line.

