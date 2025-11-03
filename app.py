from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Login como pantalla inicial (si quieres dejarlo así)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # aquí podrías validar
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/inicio")
def index():
    return render_template("index.html") 

@app.route("/calendario")
def calendario():
    return render_template("calendario.html")

@app.route("/horas")
def horas():
    return render_template("horasDeOficina.html")

if __name__ == "__main__":
    app.run(debug=True) 