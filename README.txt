How to run the index: 
In order to run the index you must simply declare an indexer object such as x = Indexer(). Afterwards you perform run()
utilizing the indexer and the directory of files that you want to index through such as “Dev”, the command will look
something like this EX: x.run(“DEV”). This will now create a resources directory in the current file location and inside
the directory will be a partial indexes directory with partial indexes of the files and final.json which will be the final index.
The indexer will automatically go through every file in the directory and give it a doc id that will appear on the doc_id_map.csv. While it is operating partial indexes will be made every 500 documents and then merged together at the very end.

How to start the search interface and perform a query: 
Functions called in main():
process_query(query) - continuously takes user input from the user, connects to the search bar in the web GUI.

conjunctive_search_set(query) - Performs conjunctive query processing using set intersection. Returns a dictionary
where keys are document IDs and values are lists of (token, frequency) pairs. Data is used to calculate scores for final ranking

merge_scores(results, query) -  takes the two rankings used in this search engine - page rank and tf-idf - 
and merges the results into one final “score”. The highest five results will be shown onto the webpage with
its corresponding AI generated summary.

In order to start the search interface you must run the app.py file in order to start the web server.
This will result in the web server to be opened and a link to be printed in the terminal. After clicking on the
terminal link you will be redirected to the search engine web GUI and you will see a search bar in which you can
enter a query. After entering a query you will be shown one of two pages- a successful search with 5 of the most
relevant results or a “not found page”. In the event of a successful search, there will be a button on the far
right side of the resulting URLs that will show an AI generated summary of the page when clicked. There will also
be a search time right under the search bar that will display the time it took - < 300 ms - to fetch the results of the query.
