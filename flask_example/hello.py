from flask import Flask, render_template

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# use `flask --app hello run`
@app.route('/')
def hello(name=None):
    return render_template('index.html')