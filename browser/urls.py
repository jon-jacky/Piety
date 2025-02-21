"""
urls.py - urlre, a URL regexp, xurl function to extract URL from a string,
          and sample URLs for testing.
"""

import re

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
 
def xurl(s):
    """
    Return (eXtract) absolute URL found in string s.
    An absolute URL begins with http:// or https:// or file://
    Return empty string if no absolute URL found.
    We expect caller has passed a string that looks like it holds a URL.
    """
    urlrep = httprep if 'http' in s else filerep if 'file' in s else norep
    m = urlrep.search(s)
    return m.group() if m else ''

def xrurl(s): 
    """
    Extract relative URL from a string formatted as one of our footnotes,
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
    return s.split()[1]  # crashes if there is no text past first whitespace
     
# Sample URLs
 
# My home page at github and the same page -- just a file -- in my local repo.
# Very simple, no style, many short paragraphs, most contain one or more links.
home = 'https://jon-jacky.github.io/home/'  # .../home/index.html
home_file = 'file:///home/jon/home/index.html'

# Another simple web page, with more text and fewer links
# but several uses  of <ul> unordered list and <li> list item.
learned = "https://jon-jacky.github.io/tesc_cs/fofc/learned.html"

# github page - Lots of stuff in addition to our content - 2227 lines!
# Our content is in lines 1967 - 2062 out of 2227
rationale = 'https://github.com/jon-jacky/Piety/blob/browser/doc/rationale.md'

# github 'raw' page - just the markdown source for rational.md - only 136 lines
rationale_raw = 'https://raw.githubusercontent.com/jon-jacky/Piety/refs/heads/browser/doc/rationale.md'

# Mostly text web page, article content in lines 516 - 575 out of 743
salmagundi = 'https://salmagundi.skidmore.edu/articles/747-martin-amis-and-the-changing-of-the-guard'

# Mostly text web page with code fragments and itemized lists
# Shows up fine in Firefox 
# BUT Piety browser gets urllib.error.HTTPError: HTTP Error 403: Forbidden
# Maybe this site doesn't like our HTTP User Agent?  Thinks it's a crawler?
hell = 'https://chrisdone.com/posts/hell-year-in-review-2025/'

# Mostly text web page with headings and code fragments
forth = 'https://pygmy.utoh.org/3ins4th.html'

# Mostly text web sites but with lots of other stuff
askmefi = 'https://ask.metafilter.com/'
hn = 'https://news.ycombinator.com/'

# Big page 6100 words, 600 photos, for testing image tags.
gorton = 'https://aresluna.org/the-hardest-working-font-in-manhattan/'

# Simple page with text and two images with alt tags
grug = 'https://grugbrain.dev/'
 
# Guardian article with lots of text but also lots of clutter
# Gets HTML page with 481 lines but it's almost all clutter.
# Article text starts on line 472 near the end of the page, 
# has only a few lines from the start of the article then ends.   
# The page itself must load more pages.
grauniad = 'https://www.theguardian.com/technology/2023/jul/25/joseph-weizenbaum-inventor-eliza-chatbot-turned-against-artificial-intelligence-ai' 
 
# These URLs  raise errors

# urllib.error.URLERROR: <urlopenerror no host given>
nohost = 'https:nowhere.com'

# urllib.error.URLERROR: <urlopenerror [SSL: TLSV1_UNRECOGNIZED_NAME] ...)>
unrecognized = 'https://nowhere.com'

# urllib.error.HTTPError: HTTP Error 404: Not Found
notfound = 'https://jon-jacky.github.io/home/missing.html' 
 
