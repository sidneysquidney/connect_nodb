# Connect Four Prjoect

A very simple connect four game built using Python and Flask.

Unfortunately the online version doesn't work because of this reason: 
https://stackoverflow.com/questions/32815451/are-global-variables-thread-safe-in-flask-how-do-i-share-data-between-requests. 
I think the solution is a multiprocessing.manager (not sessions or cache's), but I can't seem to get it working. If anyone can help me be able to run online, it would be much appreciated!

Otherwise you can clone and run locally, with flask run. 

There are 3 levels. The first is simply a randomised move, while the medium and hard are implemented using the minimax algorithm. The hard sees 6 moves ahead and is surprisingly hard to beat!

Link to play terminal verion online: 
https://replit.com/@sidneysquidney/Connect-Four#.replit
