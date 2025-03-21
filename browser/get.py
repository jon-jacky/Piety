"""
get.py - Get a web page and store it in a Piety editor buffer.
"""

from urllib import request, parse
from pathlib import Path
import re
 
import sked as ed, edsel as fr # fr for frame
import render
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
    after the first one or more whitespace characters.
    We assume caller has passed a string that looks like it holds a relative URL.
    """
    rurl =  s.split()[1]  # crashes if there is no text past first whitespace
    return rurl[2:] if rurl.startswith('..') else rurl # FIXME? Special case!

def xurl(s):
    """
    eXtract absolute or relative URL from string s
    """
    url = xaurl(s) # extract absolute URL, '' if not found
    if not url: # absolute URL not found on line - must be relative URL
        rurl = xrurl(s) # find relative URL
        url = ed.filename + rurl # ed.filename stores base URL
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
            'file:///home/jon/z/z/', # Our own Z notes, for testing
            )

def g(url):
    """
    (g)et web page from url and store it in its own Piety editor buffer.     
    """
    print('Loading page...') # sometimes there is quite a delay in urlopen
    # If urlopen fails just let it crash, return to >>> and don't create buffer
    # Any error message from urlopen will be printed in REPL.
    r = request.urlopen(url)

    # If we get this far, urlopen must have succeeded.  Create and fill buffer. 
    purl = parse.urlparse(url) # return Parse object
    ppath = Path(purl.path) # extract ppath, a Path object, from Parse object
    bufname = ppath.name if ppath.name else purl.netloc # .name might be empty
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    # Special case handling of base URLs from particular web sites - see above
    baseurl = url # default, often the base url is the same as the page url
    for burl in baseurls:
        if url.startswith(burl):
            baseurl = burl
    ed.filename = baseurl # replace filename created by e() with baseurl
    ed.buffers[bufname]['filename'] = baseurl # replace filename created by e()
    buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    # Fill in buffer text
    for line in r.readlines():
        ed.buffer.append(line.decode('utf-8')) # FIXME? get encoding fro9m HTTP
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
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
    """
    global url # So we can examine it in REPL
    url = xurl(ed.buffer[ed.dot]) # relative or absolute URL, '' if not found
    g(url)
    
def gr(url):
    'Get and Render web page at url'
    g(url)
    render.r()
    
def grx():
    'Get and Render web page at url eXtracted from current line in buffer'
    gx()
    render.r()

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
    url = fnurl(n)
    g(url)

def grf(n):
    'Get and render web page whose URL is in footnote n'
    gf(n)
    render.r()

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
    
def grfx():
    'Get and Render web page at next Footnote on eXtracted from current line.'
    gfx()
    render.r()
    
# Add keycodes for browser operations to keymap 
dmacs.keymap[key.M_g] = gx # get page at URL on current line in buffer
                           # FIXME?  Overrides M_g: edsel.graffiti in dmacs
dmacs.keymap[key.M_r] = render.r # render html from current buf. to .txt .buf
dmacs.keymap[key.M_ret] = grx # get and render page at URL on current line
dmacs.keymap[key.M_n] = grfx # get and render page at next footnote ref on line.
