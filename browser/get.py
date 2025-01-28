"""
get.py - Get a web page and store it in a Piety editor buffer.
"""

from urllib import request, parse
from pathlib import Path
 
import sked as ed, edsel as fr # fr for frame

def g(url):
    """
    (g)et web page from url and store it in its own Piety editor buffer.     
    """
    # If urlopen fails just let it crash, return to >>> and don't create buffer
    r = request.urlopen(url)

    # If we get this far, urlopen must have succeeded - create buffer
    purl = parse.urlparse(url) # return Parse object
    ppath = Path(purl.path) # extract ppath, a Path object, from Parse object
    bufname = ppath.name # extract name from Path object
    fr.e(bufname) # create empty buffer, assign local bufname to ed.bufname
    ed.filename = url # supercede e() so full url shows up in buffer list
    ed.buffers[bufname]['filename'] = url # supercede e()
    buffer = ['\n'] # So content starts at index 1 not 0, like other buffers.
    # Fill in buffer text
    for line in r.readlines():
        ed.buffer.append(line.decode('utf-8')) # get encoding from response?
    fr.refresh()
    ed.dot = 1 # first line of content, top line of window, is index 1 not 0
    print(f'{ed.bufname}, {len(ed.buffer)} lines')
