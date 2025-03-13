from flask_bootstrap import Bootstrap5
from flask import Flask, redirect, render_template

app = Flask(__name__)

bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pathfinding")
def pathfinding():
    return render_template("pathfinding.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/responses")
def responses():
    return render_template("responses.html")

if __name__ == "__main__":
    app.run(debug=True)