from flask import Flask, render_template, request, redirect
from parse import process_query
from ranking import merge_scores, tf_idf
from search import Searcher
from flask_caching import Cache
import time

config = {
    "DEBUG": True,         
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
searcher = Searcher("resources\\final.jsonl", "resources\\doc_id_map.csv")
searcher.open()

@app.route("/")
@cache.cached(timeout=50)
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET"])
# @cache.cached(timeout=300, query_string=True)
def results():
    q = request.args.get("query")
    if q is None:
        return redirect("/")
    query = process_query(q)
    start_time = time.time()
    results = searcher.conjunctive_search_set(query)
    if not results:
        return render_template("no_results.html", results=results)
    
    ranked_results = []
    count = 0
    for url, score in merge_scores(results, query):
        if count == 5:
            break
        count += 1
        ranked_results.append(searcher.get_url_from_csv(url))
    elapsed_time = time.time() - start_time
    return render_template("success.html", results=ranked_results, etime=f"{elapsed_time:.5f}")

if __name__ == "__main__":
    app.run(debug=True)