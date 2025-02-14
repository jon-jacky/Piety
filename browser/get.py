f"""
get.py - Get a web page and store it in a Piety editor buffer.
"""

from urllib import request, parse
from pathlib import Path
 
import sked as ed, edsel as fr # fr for frame
import urls, render
import key, dmacs # so we can add browser keycode entries to keymap

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
    bufname = ppath.name # extract name from Path object
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.filename = url # replace filename created by e() with url
    ed.buffers[bufname]['filename'] = url # replace filename created by e()
    buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    # Fill in buffer text
    for line in r.readlines():
        ed.buffer.append(line.decode('utf-8')) # FIXME? get encoding fro9m HTTP
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines') # after '0 lines' from e()
    
def gx():
    'Get web page at URL eXtracted from current line in current buffer.'
    g(urls.xurl(ed.buffer[ed.dot]))

def gr(url):
    'Get and Render web page at url'
    g(url)
    render.r()
    
def grx():
    'Get and Render web page at url eXtracted from current line in buffer'
    gx()
    render.r()

# Add keycodes for browser operations to keymap 
dmacs.keymap[key.M_g] = gx # get page at URL on current line in buffer
                           # FIXME?  Overrides M_g: edsel.graffiti in dmacs
dmacs.keymap[key.M_r] = render.r # render html from current buf. to .txt .buf
dmacs.keymap[key.M_ret] = grx # get and render page at URL on current line

