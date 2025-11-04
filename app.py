from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key_very_insecure")

# Credenciales de prueba
USERS = {
    "javier@gmail.com": {
        "password": "usuario1234",
        "role": "user"
    },

    "javierAdmin@gmail.com": {
        "password": "admin1234",
        "role": "superadmin"
    }
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = USERS.get(email)
        if user and password == user["password"]:
            
            # Guardar sesión mínima
            session["email"] = email
            session["role"] = user["role"]

            # Redirigir según rol
            if user["role"] == "superadmin":
                return redirect(url_for("superadmin_home"))
            else:
                return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("login.html", email=email)

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/superadmin")
def superadmin_home():
    # proteger ruta: solo superadmin
    if session.get("role") != "superadmin":
        flash("Acceso denegado. Inicia sesión como administrador.", "error")
        return redirect(url_for("login"))
    return render_template("superadmin_home.html")

@app.route("/inicio")
def index():
    # opción: permitir acceso solo si hay sesión (user o superadmin)
    if not session.get("email"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/calendario")
def calendario():
    if not session.get("email"):
        return redirect(url_for("login"))
    return render_template("calendario.html")

@app.route("/horas")
def horas():
    if not session.get("email"):
        return redirect(url_for("login"))
    return render_template("horasDeOficina.html")

@app.route("/editar_cuentas")
def editar_cuentas():
    return render_template("editar_cuentas.html")

if __name__ == "__main__":
    app.run(debug=True)