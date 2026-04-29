"""
get.py - Get a web page and store it in a Piety editor buffer.
"""

from html.parser import HTMLParser
from urllib import request, parse
from pathlib import Path
import re
 
import sked as ed, edsel as fr # fr for frame
import key, dmacs # so we can add browser keycode entries to keymap
  
# Simple regular expressions for matching URLs
# Match https:// or file:// prefix and all that follows 
#  up to whitespace or , ' "
# Much simpler than URL regexps found on the Internet,
# Matches many invalid URLs, but in our application that's not a problem,
httpre = 'https?://[^,\'"\s]+'
filere = 'file://[^,\'"\s]+'
httprep = re.compile(httpre) # p for pattern
filerep = re.compile(filere)
norep = re.compile('No URL here')

fnref = '\[\d+\]' # footnote reference - decimal digits inside [...]
fnrefp = re.compile(fnref)
fnline = '^\s*\d+\.\s+' # footnote line - whitespace, digits, period, whitepace
fnlinep = re.compile(fnline)

def xaurl(s):
    """
    Return (eXtract) Absolute URL found in string s.
    An absolute URL begins with http:// or https:// or file://
    Return empty string if no absolute URL found.
    We expect caller has passed a string that looks like it holds a URL.
    """
    urlrep = httprep if 'http' in s else filerep if 'file' in s else norep
    m = urlrep.search(s)
    return m.group() if m else ''

def xrurl(s): 
    """
    EXtract Relative URL from a string formatted as one of our footnotes,
    like these:

        10. toolkit.html
        11. ../z-lectures/z-lectures.html
    
    or like these:
    
        47. /food-drink
        48. /384528/My-very-first-Can-I-eat-this-question
    
    For now, we just return the first string of non-whitespace characters
    after the first one or more whitespace characters, if there is one
    If no such string, return '' to indicate no URL found.
    """
    words = s.split()
    if len(words) != 2: # FIXME? Crudest check that s has relative URL, unsound
        return '' # indicates no URL found
    rurl =  words[1]
    return rurl[2:] if rurl.startswith('..') else rurl # FIXME? Special case!

def xurl(s):
    """
    eXtract absolute or relative URL from string s
    Or return '' if no URL found.
    """
    url = xaurl(s) # extract absolute URL, '' if not found
    if not url: # absolute URL not found on line - must be relative URL
        rurl = xrurl(s) # find relative URL, returns '' if none found
        url = ed.filename + rurl if rurl else '' # ed.filename stores base URL
    return url    

# URLs in baseurls are prefixes of web page absolute urls
#  used as base urls for fetching other pages from that site using relative urls.
# The absolute url may include a suffix like 'newest' or 'news?p=2'
#  that must be omitted when forming a url from the base url + relative url.
# The base URL is supposed to be identified by a tag in the page itself
#  but here we just handle particular base urls as special cases.
baseurls = ('https://news.ycombinator.com/', # Hacker News
            'https://www.tbray.org/', # Tim Bray's blog, Ongoing 
            'https://github.com/', # Github generates and serves long relative urls
            'https://dercuano.github.io/', # Kragen Sitaker's notes, Dercuano
            'https://derctuo.github.io/', # Kragen Sitaker's notes, Derctuo
            'https://dernocua.github.io/', # Kragen Sitaker's notes, Dernocua                        
            'https://courses.cs.northwestern.edu/325/readings/graham/',
            'file:///home/jon/z/z/', # Our own Z notes, for testing
            )

url = ''  # URL is global so we can use it in render r(url) also for debugging
response = None # response is global so we can inspect it at the REPL

title = 'No title yet' # Contents of page <title> 

class HTML2Title(HTMLParser):
    """
    Minimal parser, find <title>, assign its data to global title (above)
     so it can be used to make bufname
    """
    def __init__(self):
        super().__init__()
        # Needed by handle_data, which for some reason doesn't have tag arg.
        self.tag = 'Unassigned'

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.tag = tag

    def handle_endtag(self, tag):
        if tag == 'title':
            self.tag = 'Unassigned' # Unnecessary?  Should be only 1 title
                                        
    def handle_data(self, data):
        global title
        if self.tag == 'title':
            title = data # global title, so we can use it to make bufname
    
def g(aurl):
    """
    (g)et web page from aurl and store it in its own Piety editor buffer.     
    """
    global url, response, req
    global title # make this global so we can assign default
    url = aurl  
    title = 'No title' # default, parser.feed assigns title if there is one
    
    # See https://docs.python.org/3/howto/urllib2.html
    # Default User-Agent is Python-urllib/n.m which often gets 403: Forbidden 
    # MetaFilter requires 'Lynx' somewhere in User-Agent if using HTTP/1.x
    req = request.Request(url, None, {'User-Agent': 'Piety browser, not Lynx'})
    print('Loading page...') # sometimes there is quite a delay in urlopen
    # If urlopen fails just let it crash, return to >>> and don't create buffer
    # Any error message from urlopen will be printed in REPL.

    response = request.urlopen(req)

    # Can't use this - because we don't have bufname yet.
    #fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname

    # Following code is based on body of sked.e()
    # Instead of calling fr.e(...), assign ed. variables then save_buffer()

    # First save current buffer (soon to be previous) before making new one    
    if ed.S() > 0: ed.save_buffer()  
    ed.prev_bufname = ed.bufname
    
    # Special case handling of base URLs from particular web sites - see above
    baseurl = url # default, often the base url is the same as the page url
    for burl in baseurls:
        if url.startswith(burl):
            baseurl = burl
    # For web pages, filename stores page URL, not file name in file system
    ed.filename = baseurl # Just show the baseurl in the buffer listing

    # Now assign ed.buffer contents - must do this before assigning ed.bufname
    ed.buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    ed.buffer.append(f'<!-- {url} -->\n') # put page URL on first line
    ed.buffer.append('\n')
    # Fill in buffer text from HTTP response
    for line in response.readlines():
        ed.buffer.append(line.decode('utf-8')) # FIXME? get encoding from HTTP
    # Run parser to find <title> in ed.buffer and assign to global title above 
    parser = HTML2Title()
    parser.feed(''.join(ed.buffer)) # requires string, not list of string
    bufname = title[:12].replace(' ','-')+'.html' # use global title above
    ed.bufname = ed.bname(bufname) # add <2> etc. suffix if needed.
    
    # Assign remaining buffer variables in ed.
    ed.saved = True # put this *before* move_dot for display code

    # Save buffer, and for display we have to follow fr.e() code not ed.e() 
    # fr.display_e replaces ed.move_dot in fr.e().  It includes move_dot
    # Must move dot before saving buffer
    fr.display_e(min(ed.S(),1)) # start of buffer, empty buffer S() is 0
    ed.save_buffer() # put the new current buffer in the saved buffers
    # fr.refresh() # I think this is handled by fr.display_e() above
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
        
def gx():
    """
    Get web page at URL eXtracted from current line in current buffer.
    We expect user has selected a line
     that looks like it holds an absolute or relative URL.
    We expect that line is one of our footnotes on a rendered web page.
    We have arranged that the filename associated with the buffer that
    holds that rendered web page is actually the absolute URL of that page,
    so it is the base URL of any relative URLs that appear in footnotes.
    If there is no URL on the line, do nothing
    """
    global url # So we can examine it in REPL
    url = xurl(ed.buffer[ed.dot]) # relative or absolute URL, '' if not found
    if url: # url is '' if no URL found on line
        g(url)

def fnnum(line):
    """
    Return integer footnote number of line, a string, or '' if not a footnote.
    Footnote number, if there is one, matches fnlinep regular expression
    """
    m = fnlinep.search(line)
    fnstr = m.group() if m else ''
    return int(fnstr.strip()[:-1]) if fnstr else ''
        
def fnurl(n):
    """
    Return URL in buffer at footnote n or '' if footnote n not found.
    Example footnote line, a relative URL: '187. ?p=2\n'
    """
    for line in ed.buffer:
        if n == fnnum(line):
            return xurl(line) # return breaks from loop
    return '' # not found
    
def gf(n):
    'Get web page whose URL is in footnote n'
    global url
    url = fnurl(n)
    g(url)

def fnrefnum():
    """
    Return integer footnote reference number next on current line.
    Return 0 if no footnote found.
    """
    m = fnrefp.search(ed.buffer[ed.dot][ed.point:])
    fnrefn = m.group() if m else ''
    return int(fnrefn[1:-1]) if fnrefn else 0
    
def gfx():
    'Get web page at next Footnote eXtracted from current line.'
    n = fnrefnum() # Footnote number, or 0 if no footnote on line
    g(fnurl(n))  # crashes if no footnote on line

def clear_webpages():
    'Delete all webpages, buffers whose bufname includes .html or .htxt'
    ed.clear_buffers('all web pages', 
        # use 'in' not 'endswith' to include ...html<2>  ...htxt<3> etc.
        discard=(lambda buf: '.html' in buf['filename']
                    or '.htxt' in buf['bufname']))
        
# Add keycodes for browser operations to keymap 
dmacs.keymap[key.M_g] = gx # get page at URL on current line in buffer
                           # FIXME?  Overrides M_g: edsel.graffiti in dmacs
# key.C_o entry is now assigned in viewer.py
# dmacs.keymap[key.C_o] = grx # get and render page at URL on current line
  
