import io
from contextlib import redirect_stdout

f = io.StringIO()
with redirect_stdout(f):
    print('foobar')
    print(12)
print('Got stdout: "{0}"'.format(f.getvalue()))

