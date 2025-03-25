"""
search.py - Search web sites by sending query URLs
 
To search Hacker News: Sample query, list stories that match the query
'STEPS reinventing programming', ordered by date:

 https://hn.algolia.com/?dateRange=all&page=0&prefix=false&query=STEPS%20reinventing&sort=byDate&type=story 

The query part there is:

 &query=STEPS%20reinventing%20programming&sort=byDate&type=comment

Never mind, it doesn't work.  Sending the query just results in
hn.algolia.com sending back a page of Javascript, which your
browser has to run to actually execute the query.   That page contains:

<noscript>This page will only work with JavaScript enabled</noscript>

Bah!  The Piety browser will never support Javascript.
"""

import get

hnprefix = 'https://hn.algolia.com/?dateRange=all&page=0&prefix=false&query='

def hnsearch(type, query):
    """
    Search Hacker News by sending query to hn.algolia.com.
    type is 'story', 'comment', or 'user'
    query is a string of space-separtaed keywords: 'STEPS reninvention'
    BUT the server just returns a page of Javascript the browser must execute!
    """
    hnquery = '%20'.join(query.split())
    hntype = f'&sort=byDate&type={type}'
    get.gr(hnprefix + hnquery + hntype)

def hnuser(user):
    """ 
    Retrieve all comments posted by user, most recent first.
    Does *not* send query to Algolia or require Javascript - so it works!
    """
    get.gr(f'https://news.ycombinator.com/threads?id={user}')
    
def hnitem(id):
    'Get the HN item page with integer (not string) id number'
    get.gr(f'https://news.ycombinator.com/item?id={id}')
    
