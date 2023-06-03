
keyseq.py
=========

**keyseq.py**: construct emacs-style key sequence from one or more characters.

Define function keyseq(c).  On each call, pass in a single character.
Do not block waiting for sequence to complete, return after each call.
When sequence is complete, return the entire sequence (maybe single char).
When sequence is incomplete, return the empty string ''.
Pass in C_g (^G) to cancel incomplete sequence in progress and just return C_g.

Following emacs nomenclature, we call a sequence of one or more characters
that can be used as an editor command a 'key'.

This function does *not* block after receiving a prefix character  such
as C_x.  Instead, this function  always returns immediately after
receiving each single character.  If the character is a prefix, and
more characters are expected, this function just returns the empty
string, ''.   If the character is not a prefix (it is a printing
character or a self-contained  control character) this function
returns that character.  If the character is the last character in a
multicharacter sequence, this function returns the whole sequence
including the prefix  character(s) and the last character.

Also, the function might read multiple characters in one call,
if more than one character arrived since the last call.  This
might happen for special function keys, arrow keys etc. that include
a prefix plus contents, all sent rapidly.   If the function reads
more than a single character in one call, it immediately returns
the entire sequence of characters it read.

Each key sequence begins with prefix character or characters indicating more
follows. ESC is the prefix for the meta commands and terminal control
codes. C_x is the prefix for some key sequences such as C_x b, the
editor  command  to switch to another buffer.  ESC-[ (called CSI) is
the prefix for terminal control codes.

To avoid waiting indefinitely for a sequence that never finishes,
reading C_g (that is, CTRL g or ^g) at any time ends waiting,
discards any incomplete sequence, and immediately returns just C_g.
So the user can type C_g if a program appears hung when reading a command.
C_g is used as the Cancel command by some programs.

This module is in the vt_terminal directory (not the editors directory or
elsewhere) because here meta keys M-... are key sequences starting
with the ASCII escape character.  Also, here cursor arrow keys
are key sequences staring with the ANSI control sequence introducer (csi)
esc-[   These are true of VT-style video terminals and emulators but might
not be true of other platforms, where they might be represented by 
keyboard scan codes or something else.

In the modules in the editors directory, keys (including key sequences) 
are referred to only by name.  Their internal structure as sequences of
ASCII characters (or something else) is not visible.

Revised Jun 2023
