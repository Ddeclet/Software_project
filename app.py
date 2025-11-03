from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")

if __name__ == "__main__":
    app.run(debug=True)
