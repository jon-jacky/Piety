"""
pmacs.py - Initialize global variables used by pmacs just once at startup.
"""

import edsel

inline = True # kill (cut) and yank (paste) within a single line

# We need this here in pmacsinit not pmacs so reloading pmacs
# while pm is running does not reassign saved_put_marker to put_no_marker

saved_put_marker = edsel.put_marker # so we can restore after put_no_marker
