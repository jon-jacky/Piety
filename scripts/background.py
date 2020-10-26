"""
background.py - Demonstrate printing to editor buffers from
the "background".  That is, adding to editor buffers from
Python code but without using using ed/edda commands or API.

This script uses blocking while loop, not piety event loop.

To run the demo:

 $ python3 -im background
... windows appear ...
:o2
... window splits ...
:b ts1
... ts1 appears in top window ...
:o2
.. ts1 window splits ...
:o
:o
... back in main window ...
:!print(next(ts1),file=ts1buf)
... timestamp appears in both ts1 windows ...
...

Alternatively:

 $ python3 -i
...
>>> import background as bg
.   ts1                   0  Text     ts1
.   ts2                   0  Text     ts2
>>> bg.main()
...
... as above: o2  b ts1  o2  o  o
...
:!print(next(bg.ts1),file=bg.ts1buf)
... you have to use bg. prefix here too ...

"""

import timestamp
import edda

# We haven't started display editor yet, window not initialized,
#  so use ed commands.
ed = edda.ed
text = ed.text

# Create the main buffer and add some content
text.startup('main')
ed.i('This is the main buffer')
# create timestamp generators
ts1 = timestamp.timestamp('ts1')
ts2 = timestamp.timestamp('ts2')
# create buffers for timestamp messages
ed.b('ts1')
ed.b('ts2')
# aliases for timestamp buffers
ts1buf = text.buffers['ts1']
ts2buf = text.buffers['ts2']
# add content to timestamp buffers
print(next(ts1), file=ts1buf)
print(next(ts2), file=ts2buf)

def main():
    edda.main(c=12)

if __name__ == '__main__':
    main()

