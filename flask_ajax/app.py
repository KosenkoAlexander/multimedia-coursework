from flask import Flask, render_template, request

app = Flask(__name__)

DATA = [
    {"name": "Alice", "city": "Paris"},
    {"name": "Bob",   "city": "London"},
    {"name": "Eve",   "city": "Paris"},
    {"name": "Sam",   "city": "Berlin"},
]

@app.route("/")
def index():
    return render_template("index.html", rows=DATA)

@app.route("/filter")
def filter_data():
    city = request.args.get("city", "").lower()
    filtered = [r for r in DATA if city in r["city"].lower()]
    return render_template("table_rows.html", rows=filtered)

if __name__ == "__main__":
    app.run(debug=True)