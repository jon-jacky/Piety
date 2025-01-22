"""
get.py - Get a web page and store it in a Piety editor buffer.
"""

from urllib import request

import sked as ed, edsel as fr # fr for frame

def g(url):
    """
    (g)et web page from url and store it in its own Piety editor buffer.     
    """
    # FIXME - Very incomplete for now!
    # Appends lines from downloaded page to current buffer.
    # You must have already created and named the buffer.
    r = request.urlopen(url)
    # PRELUDE - handle error codes 404 at least
    # FIRST - extract bufname basename from URL
    # NEXT - extract mime-type from r to get bufname extension; .html .txt .md
    # ALSO - use url for buffer filename
    # Finally, fill in buffer text:
    for line in r.readlines():
        ed.buffer.append(line.decode('utf-8')) # get encoding from response?
    fr.refresh()    

