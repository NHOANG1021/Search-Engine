from flask import Flask, render_template, request, redirect, jsonify
from parse import process_query
from ranking import merge_scores
from search import Searcher
from flask_caching import Cache
from tokenizer import extract_contents
import time
import gemini as g

config = {
    "DEBUG": True,         
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

searcher = Searcher("resources/final.jsonl", "resources/doc_id_map.csv")
searcher.open()

@app.route("/")
def index():
    """
    Loads home page for the search engine
    """
    return render_template("index.html")

@app.route("/results", methods=["GET"])
def results():
    """
    Generates a results page
    """
    q = request.args.get("query")
    if not q:
        return redirect("/")

    query = process_query(q)
    start_time = time.time()
    results = searcher.conjunctive_search_set(query)

    if not results:
        return render_template("no_results.html", results=results)

    ranked_results = []

    for docid, score in merge_scores(results, query):
        info = searcher.get_url_from_csv(docid)
        ranked_results.append({"url": info[0], "docid": info[1]})


    elapsed_time = time.time() - start_time
    return render_template("success.html", results=ranked_results, etime=f"{elapsed_time:.5f}")

@app.route("/summarize", methods=["POST"])
def summarize():
    """
    Backend integration to create a ai summary for the page
    """
    data = request.get_json()
    docid = data.get("docid")  # Correct key name
    if not docid:
        return jsonify({"error": "File is required"}), 400

    try:
        api_key = "AIzaSyDHRURf3ECW1mOCPXB5zfGn7ionHted2WE" 
        contents = extract_contents(docid.strip())
        summary = g.summarize_webpage(api_key, contents["content"])
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"Failed to summarize: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
