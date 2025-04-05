
Piety browser
=============

Text-only web browser closely integrated with the Piety editors. 
Downloaded web pages are stored and displayed in editor buffers. 

[Quick Start](#Quick-Start)
[Appearance](#Appearance)   
[Commands](#Commands)   
[Keycodes](#Keycodes)   
[HTML Tags](#HTML-Tags)   
[div Classes](#div-Classes)   
[Base URLs](#Base-URLs)   
 
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

### Appearance ###

Each web page appears in *two* editor buffers: we download the HTML sent
by the server into a buffer whose name ends in *.html*, then our browser
renders the HTML into text into a buffer with the same base name, but
ending in *.txt*.   Both buffers can be selected and viewed by the usual
editor commands or keycodes.

The URL of the page appears in the first (top) line of both versions
of the page.
 
In the rendered text page, hypertext links are displayed as footnotes.
The text in the link is marked by underscores, and is followed by a
footnote number in brackets: *\_like this\_ [12]*. At the end of the
buffer, the numbered list of link URLs appears. 

For example, here are a few lines from the rendered text page for
*news.ycombinator.com*.  This page is unusually dense with links:

    _Hacker News_ [1]_new_ [2]_past_ [3]_comments_ [4]_ask_ [5]_show_
    [6]_jobs_ [7]_submit_ [8]_login_ [9]
    
    _Fastplotlib: Driving scientific discovery through data visualization_
    [10]_medium.com/caitlin9165_ [11]_rossant_ [12]_56 minutes ago_
    [13]_hide_ [14]_9 comments_ [15]

Here are the corresponding footnotes from the end of that buffer, with
the link URLs. The URL at footnote *10.* is an absolute URL, the others
are relative URLs.

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

There are commands and keycodes to load a linked page from its 
footnote number in the body of the rendered text, or from its footnote
line at the end.  See below.

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

These are the commands (that is, function calls) you can type at the
Python prompt to run the browser.   To get to the Python prompt from
display editing mode, type *M-x* (*meta x*, hold down the *alt* key
while typing the *x* key). Use other *pmacs* editor commands (described
elsewhere) to select and view the buffers that hold web pages.

Most of these commands can also be invoked in display editor mode
by typing [keycodes](#Keycodes).

- **g(url)** - **Get** the web page at *url* and store it in its own 
   editor buffer. The *url* is a string, either a literal URL string or
   a variable with a string value (as are found in *urls.py*). Downloads
   the page at *url* into a new buffer whose name is generated 
   from that URL, and often ends in *.html*. Makes that buffer the current
   buffer so it appears in the current window, replacing the previous
   window contents. This command does *not* render the HTML into a text
   buffer.

- **r()** - **Render** the current buffer into a new text buffer.
  It is intended that the current buffer is the HTML web page downloaded
  by *g(url)* (above). The new buffer gets the same base name as the
  current buffer, but ends with *.txt*. The new text buffer is made the
  current buffer so it appears in the current window, replacing the HTML
  that was there.

- **gr(url)** - **Get** and **render** the web page at *url*.
    Calls *g(url)* and then *r()*.   Creates both *.html* and *.txt*
    buffers.  The new *.txt* buffer becomes the current buffer and
    appears in the current window.  

- **gx()** - **Get** the web page at the URL **eXtracted** from the current line 
   in the current buffer.  Similar to *g() (get)* (above) except there is no 
   URL argument. It is expected that the user has positioned the cursor at
   a line in the current window that displays an absolute or relative URL.
   The browser attempts to load the page at that URL.   

   This command works in any text buffer.  It does not have to be a web page.
   There just needs to be an absolute URL on the line.
   
   An absolute URL can be anywhere on the selected line. It begins with
   *http://* or *https://* or *file://*, and extends until a quote
   character *' "* or a white space character. 
   
   If no absolute URL is found in the line, this command assumes the
   first string following the first space(s) on the line is a relative
   URL. This format is chosen to work with the footnotes in the list at
   the end of our rendered web pages, but any relative URL in this
   format will work. The relative URL is appended to the current
   [base URL](#Base-URLs) to form the absolute URL where the
   page is fetched.
   
- **grx()** - **Get** and **Render** the web page at the URL on the 
    current line in the current buffer.   Similar to *gr()* (above)
    but there is no URL argument.

- **gf(n)** - **Get** the web page whose URL is in **Footnote n** .

- **grf(n)** - **Get** and **Render** the web page whose URL is in
   **Footnote n** .

- **gfx()** -  **Get** web page whose URL is in the
    **Footnote** whose number is **eXtracted** from current line.
    It is expected tha that the user has positioned the cursor 
    on the same line as the footnote, before the footnote of interest
    but after any other footnotes that precede it. 

- **grfx()** -  **Get** and **Render** web page whose URL is in the next 
    **Footnote** whose number is **eXtracted** from current line.

- **N()** - list all buffer **Names** in the *\*Buffers\** buffer and
   display it in the current window.  Buffers that hold web pages 
    appear in the list among other buffers that hold text being edited.
    The middle column holds the base URL of the page, used to generate
    absolute URLs from relative URLs on that page.
    
    To select a buffer, move the cursor to the line that lists 
    that buffer and type *return* (or *enter*).
    This is the usual way to view a web page that has already been loaded.
    The buffer list is what we provide instead of browser tabs, a Back
    button, or a Show Source button.

- **b()** - Return to the previous buffer.  This can be used like a
  browser 'Back button' to return to the page from which a link was loaded. 

- **dir(urls)** - list the symbolic URL names defined in *urls.py*.
  You can use any of these as the *url* argument to the *gr(url)* command.
  You can type any of the names at the Python prompt, Python will
  print its literal URL string -- which you can also use as an 
  argument to *gr(url)*.

- **get.url** - Print the absolute URL that was most recently used to
   try to load a web page.  This can be useful for debugging base URLs
   and relative URLs.   There are no parentheses in this expression, it
   is just the name of the *url* variable in the *get* module.

 - **get.response** - The HTTP response to the most recent HTTP request,
   including the HTML text of the returned page, if there is one.
   Can be inspected at the REPL for debugging or investigation.
   
  - **render.parser** - The *HTMLParser* object in the *render* module.
    Can be inspected at the REPL to help debug rendering.

### Keycodes ###

Keycodes you can type to invoke browser [commands](#Commands) (above)
while in display editing mode. To get to display editing mode from the
Python prompt, type the function call *pm()*. Use other *pmacs* editor
keycodes (described elsewhere) to select and view the buffers that hold
web pages.
  
- **M-g** - invokes *gx()*, **get** page at URL on the current line in 
            the current buffer.

- **M-r** - invokes *r()*, **render** page in the current *.html* buffer to 
            a new *.txt* buffer.

- **M-ret** - invokes *grx()*, **get** and **render** the page at the 
            URL in the current line in the current buffer.
            This command works in any kind of buffer, it does not have
            to be a web page.
            
- **M-n** - invokes *grfx()*, **get** and **render** web page whose 
    URL is in the next **Footnote** number on the current line.

- **C-x C-b** - invokes *N()*, list **buffers**, including web pages,
            but all other buffers as well.

 - **C-x b** - Invokes *b()*, return to previous buffer.
              Can be used like a browser 'Back button'
                to return to the page from which a link was loaded.  
                
### HTML Tags ###

The Piety browser only renders these HTML tags:
*h1 h2 h3 h4 p li pre a strong em img br noscript* and some *div*.

We require matching closing tags for every tag that uses them 
(all but *img* and *br*).  We tried to code some error recovery,
but unmatched tags will usually result in scrambled rendering.

Here is how each tag is rendered:
 
- **h1 h2 h3 h4** - Header text appears on a line by itself,
    preceded and followed by empty lines.

- **p** - Paragraph text is preceded and followed by empty
    lines, and is wrapped to the page width.
    
- **li** - List items are rendered just like paragraphs, 
    except they are preceded by a bullet formed from two hyphens: --.
    Unordered and ordered list items are rendered the same way;
    ordered list items are not numbered.

- **pre** - Pre-formatted text is preceded and followed by an empty line,
    and is rendered line by line just as it appears in the source, with
    the same line breaks, and no fill or wrap. This tag is used for
    code, verse, and other texts where line breaks are significant.

-  **a** - Links appear as footnotes, see [above](#Appearance-and-Workflow).
        
- **strong**, **em** - Strong text and emphasized text is 
    preceded and followed by asterisks: **\**...\****
    
- **img** -  Each image is represented by a separate line, preceded
    and followed by empty lines, that contains just *[ Image ]* if the
    image tag doesn't provide any alt text, or *[ the alt text ]* if it
    does.

    Some pages include many small images used as icons.
    To reduce clutter in the rendered text page by suppressing all 
    output from *img* tags in that page, include that page's domain
    in the module-level variable *noimage* in the *render* module.
    
- **br** - Inserts a line break, but not an empty line.

- **noscript** - Where there is a script (usually Javascript) in the 
  page, writes a message indicating that scripts are not supported.

- **div** - Most *div* tags are not rendered.  Only a few *div* classes 
    are supported. The are rendered like paragraphs.
    
### div Classes ###

Only *div* tags whose *class* attributes have a few particular values
are rendered. The *div* that belong to these classes appear in
particular web sites that we visit. We found these classes by inspecting
the HTML in the web pages from these sites.

The supported *div* classes are stored in the module level variable 
*divclasses* in *render.py*.  Sometimes we add classes.  These are the
classes supported at this writing, in Mar 2025:

    divclasses = ('copy post',  # www. ask.metafilter.com: posts, asks on front page
                  'copy',       # metafilter: top of post or answer page
                  'comments',   # metafilter: each answer or each comment
                  'comments best',  # metafilter: answers marked best
                  'comments bestleft', # metafilter: asker's remark on answer page
                  'commtext c00', # news.ycombinator.com (Hacker News): comment
                  'toptext', # ycombinator: text at top of Ask HN
                  'os', # www.tbray.org/ongoing/ front page article links/summaries 
                  )

### Base URLs ###

Some of the URLs in the footnotes are *relative* URLs -- they are incomplete.
A relative URL must be appended to a *base* URL to form a complete
*absolute* URL that can be used to fetch a page.   

Sometimes the base URL for the relative URL links on a page is the same as
the absolute URL for that page. Sometimes the base URL is just a prefix
of that absolute URL. 

We have discovered those prefix base URLs for some of the web sites we
visit.  They are stored in the module level variable *baseurls* 
in *get.py*.  Sometimes we add base URLs.  These are the base URLs
supported at this writing, in Mar 2015:

    baseurls = ('https://news.ycombinator.com/', # Hacker News
                'https://www.tbray.org/', # Tim Bray's blog, Ongoing 
                'https://github.com/', # Github generates and serves long relative urls
                'https://dercuano.github.io/', # Kragen Sitaker's notes, Dercuano
                 )

The base URL for each web page appears in a middle column of the buffer list
shown by the *N()* command or the *C-x C-b* keycode.

Revised Apr 2025

