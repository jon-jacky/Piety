"""
urls.py - Sample URLs for testing browser
"""

# These URLs work
file = 'file:///home/jon/home/index.html'
jon = 'https://jon-jacky.github.io/home/'  # .../home/index.html


# These URLs  raise errors

# urllib.error.URLERROR: <urlopenerror no host given>
nohost = 'https:nowhere.com'

# urllib.error.URLERROR: <urlopenerror [SSL: TLSV1_UNRECOGNIZED_NAME] ...)>
unrecognized = 'https://nowhere.com'

# urllib.error.HTTPError: HTTP Error 404: Not Found
notfound = 'https://jon-jacky.github.io/home/missing.html' 


