# excerpt from Eli Bendersky
# https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
# but add blank line after with-block so we can run it with edsel R P ^T

import io
from contextlib import redirect_stdout

f = io.StringIO()
with redirect_stdout(f):
    print('foobar')
    print(12)

print('Got stdout: "{0}"'.format(f.getvalue()))

