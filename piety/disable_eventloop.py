"""
disable_eventloop.py

Import this stub module before importing the edsel module to prevent
loading the eventloop module into edsel and prevent edsel from running
in the asyncio event loop.    The edsel module contains the code:

    eventloop_enabled = True # default

    if 'disable_eventloop' in sys.modules:
        eventloop_enabled = False
        # don't import eventloop
    else:
        import eventloop     
"""
                       
