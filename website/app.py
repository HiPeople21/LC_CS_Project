from flask import Flask, redirect, render_template

from ..visualisations import generate_barchart, generate_heatmap

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/pathfinding")
    # return render_template("index.html")

@app.route("/pathfinding")
def pathfinding():
    return render_template("pathfinding.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

if __name__ == "__main__":
    app.run(debug=True)