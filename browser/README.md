
Piety browser
=============

Text-only web browser closely integrated with the Piety editors. 
Downloaded web pages are stored and displayed in editor buffers. 

### Quick Start ###

Run the Piety browser in an ordinary session of the Piety display
editor, [pmacs](../editors/README.md).  To start *pmacs*:

There isn't any installation procedure.  Just clone the 
Piety repository under your home directory.

Run this command to put the editor and browser modules on your
*PYTHONPATH*, so you can run them from any directory. Note the dot at
the beginning of the command:

    . ~/Piety/bin/paths      

Run this command to start the display editor, including the browser:

    python3 -im pm

Now you can run the browser by typing [commands](#Commands) at the Python
prompt, or by pressing [keycodes](#Keycodes).

[Appearance and Workflow](#Appearance-and-workflow)   
[Commands](#Commands)   
[Keycodes](#Keycodes)   
[Internals](#Internals)   
[Supported HTML Tags](#Supported-HTML-Tags)   
[Supported div Classes](#Supported-div-Classes)   
[Absolute and Relative URLs](#Absolute-and-Relative-URLs)   

### Appearance and Workflow ###

Each web page appears in *two* editor buffers: we download the HTML sent
by the server into a buffer whose name ends in *.html*, then our browser
renders the HTML into text into a buffer with the same base name, but
ending in *.txt*.   Both buffers can be selected and viewed by the usual
editor commands or keycodes.

In the rendered text page, hypertext links are displayed as footnotes.
The text in the link is marked by underscores, and is followed by a
footnote number in brackets: *\_like this\_ [12]*. At the end of the
buffer, the numbered list of link URLs appears. You can scroll down to
the numbered URL you want, and then select it to load the linked page.
It is convenient to display the rendered body text in one display
window and the list of URLs in another.

For example, here are a few lines from the rendered text page for
*news.ycombinator.com*.  This page is unusually dense with links:

    _Hacker News_ [1]_new_ [2]_past_ [3]_comments_ [4]_ask_ [5]_show_
    [6]_jobs_ [7]_submit_ [8]_login_ [9]
    
    _Fastplotlib: Driving scientific discovery through data visualization_
    [10]_medium.com/caitlin9165_ [11]_rossant_ [12]_56 minutes ago_
    [13]_hide_ [14]_9 comments_ [15]

Here are some lines from the end of that buffer, with the link URLs:

    10. https://medium.com/@caitlin9165/fastplotlib-driving-scientific-discovery-through-data-visualization-418f8bff094c
    11. from?site=medium.com/caitlin9165
    12. user?id=rossant
    13. item?id=43334190
    14. hide?id=43334190&goto=news
    15. item?id=43334190

Handling links as footnotes in this way enables us to store the link
URLs along with the body text in an ordinary text buffer, without
cluttering the body text too much. We don't have to add any new data
structures to hide the link URLs off the display as most browsers do.

We use the already existing editor features instead of adding
new ones just to support the browser.  Instead of browser tabs,
we list the browser buffers along with all the others in the buffer list.
Instead of a "back button", all the downloaded and rendered pages remain
in buffers so they can be selected and viewed at any time.
Instead of a "show HTML source" function, we always retain the HTML for each
page in a buffer. Instead of bookmarks, we have a frequently updated
module *urls.py* that defines URLs and assigns them to short variable
names so they can be used easily.

### Commands ###

- **g(url)** - **Get** web page at *url* and stor it in its own editor buffer.
   The *url* is a string, either a literal URL string or a variable with
   a string value (as are found in *urls.py*). Downloads the page at
   *url* into a new buffer whose name ends in *.html*. Makes that buffer
   the current buffer so it appears in the current window, replacing the
   previous window contents. This command does *not* render the HTML
   into a text buffer.

- **r()** - **Render** the current buffer into a new text buffer.
  It is intended that the current buffer is a downloaded HTML web page.
  The new buffer gets the same base name as the current buffer, but 
  ends with *.txt*.   The new text buffer is made the current buffer so 
  it appears in the current window, replacing the HTML that was there.

- **gr(url)** - **Get** and **render** the web page at *url*.  
    Calls *g(url)* and then *r()*.   Creates both *.html* and *.txt*
    buffers.  The new *.txt* buffer becomes the current buffer and
    appears in the current window.  
    
### Keycodes ###

To come.

### Internals ###

To come.

### Supported HTML Tags ###

To come.

### Supported div Classes ###

To come.

### Absolute and Relative URLs ###

To come.

Revised Mar 2025

