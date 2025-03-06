from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=["GET"])
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)