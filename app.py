from flask import Flask, render_template, request, redirect
from parse import process_query
from ranking import compare_query
from search import Searcher
import time

app = Flask(__name__)
searcher = Searcher("resources\\final.jsonl", "resources\\doc_id_map.csv")
searcher.open()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET"])
def results():
    q = request.args.get("query")
    if q is None:
        return redirect("/")
    query = process_query(q)
    results = searcher.conjunctive_search_set(query)
    if not results:
        return render_template("no_results.html", results=results)
    
    ranked_results = []
    count = 0
    for url, score in compare_query(results, query):
        if count == 5:
            break
        count += 1
        ranked_results.append(searcher.get_url_from_csv(url))
    return render_template("success.html", results=ranked_results)

if __name__ == "__main__":
    app.run(debug=True)