"""
urls.py - Sample URLs for testing.
"""

# Sample URLs
 
# My home page at github and the same page -- just a file -- in my local repo.
# Very simple, no style, many short paragraphs, most contain one or more links.
home = 'https://jon-jacky.github.io/home/'  # .../home/index.html
home_file = 'file:///home/jon/home/index.html'

# This page has some links which are relative URLs.
# For testing browser code from a file URL when no Internet.
zfile = 'file:///home/jon/z/z/index.html'

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
mefi = 'https://www.metafilter.com/'
hn = 'https://news.ycombinator.com/'
hnnew = 'https://news.ycombinator.com/newest' # Must *not* have final /

# Link blogs etc.
trivium = 'http://leahneukirchen.org/trivium/'
tbray='https://www.tbray.org/ongoing/'
nelson='https://pinboard.in/u:nelson'

# Reviving the Dillo browser
dillo = 'https://dillo-browser.github.io/'
dilloslides = 'https://dillo-browser.github.io/fosdem-2025/'
 
# Simple page with text and two images with alt tags
grug = 'https://grugbrain.dev/'

# Big page 6100 words, 600 photos, for testing image tags.
gorton = 'https://aresluna.org/the-hardest-working-font-in-manhattan/'

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
 
