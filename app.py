from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key_very_insecure")

# Profesores
PROFESORES = {
    "luis-colon":        {"nombre": "Prof. Luis Colón Cólon", "email": "luis.colon19@upr.edu"},
    "eliana-valenzuela": {"nombre": "Prof. Eliana Valenzuela Andrade", "email": "eliana.valenzuela@upr.edu"},
    "juan-lopez":        {"nombre": "Prof. Juan Lopez Gerena", "email": "juano.lopez@upr.edu"},
    "aixa-ramirez":      {"nombre": "Prof. Aixa Ramirez Toledo", "email": "aixa.ramirez@upr.edu"},
    "emilio-perez":      {"nombre": "Prof. Emilio Pérez Arnau", "email": "emilio.perez@upr.edu"},
}

# Term activo
TERM_ACTUAL = "C51"

# Horas de oficina
OFFICE_HOURS = {
    "luis-colon": [
        {"dia": "Lunes",      "inicio": "11:30am", "fin": "12:30pm", "term": TERM_ACTUAL},
        {"dia": "Lunes",      "inicio": "2:30pm",  "fin": "3:00pm",  "term": TERM_ACTUAL},
        {"dia": "Miércoles",  "inicio": "11:30am", "fin": "12:30pm", "term": TERM_ACTUAL},
        {"dia": "Miércoles",  "inicio": "2:30pm",  "fin": "3:00pm",  "term": TERM_ACTUAL},
    ],
    "eliana-valenzuela": [
        {"dia": "Lunes",      "inicio": "8:00am", "fin": "10:00am", "term": TERM_ACTUAL},
        {"dia": "Miércoles",  "inicio": "8:00am", "fin": "10:00am", "term": TERM_ACTUAL},
        {"dia": "Viernes",    "inicio": "8:00am", "fin": "10:00am", "term": TERM_ACTUAL},
    ],
    "juan-lopez": [
        {"dia": "Lunes",      "inicio": "8:00am",  "fin": "10:30am", "term": TERM_ACTUAL},
        {"dia": "Miércoles",  "inicio": "8:00am",  "fin": "10:30am", "term": TERM_ACTUAL},
        {"dia": "Martes",     "inicio": "8:00am",  "fin": "8:30am",  "term": TERM_ACTUAL},
        {"dia": "Jueves",     "inicio": "8:00am",  "fin": "8:30am",  "term": TERM_ACTUAL},
    ],
    "aixa-ramirez": [
        {"dia": "Martes",     "inicio": "1:45pm",  "fin": "4:30pm",  "term": TERM_ACTUAL},
        {"dia": "Jueves",     "inicio": "1:45pm",  "fin": "4:30pm",  "term": TERM_ACTUAL},
    ],
    "emilio-perez": [
        {"dia": "Martes",     "inicio": "7:00am",  "fin": "8:00am",  "term": TERM_ACTUAL},
        {"dia": "Martes",     "inicio": "10:00am", "fin": "10:30am", "term": TERM_ACTUAL},
        {"dia": "Martes",     "inicio": "4:00pm",  "fin": "5:30pm",  "term": TERM_ACTUAL},
        {"dia": "Jueves",     "inicio": "7:00am",  "fin": "8:00am",  "term": TERM_ACTUAL},
        {"dia": "Jueves",     "inicio": "10:00am", "fin": "10:30am", "term": TERM_ACTUAL},
        {"dia": "Jueves",     "inicio": "4:00pm",  "fin": "5:30pm",  "term": TERM_ACTUAL},
    ],
}

# Credenciales de prueba
USERS = {
    "javier@gmail.com": {
        "password": "usuario1234",
        "role": "user"
    },

    "javierAdmin@gmail.com": {
        "password": "admin1234",
        "role": "superadmin"
    },

    "javierSub@gmail.com": {
        "password": "subadmin1234",
        "role": "subadmin"
    },
    "javierProf@gmail.com": {
        "password": "profesor1234",
        "role": "profesores"
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
            elif user["role"] == "subadmin":
                return redirect(url_for("subadmin_home"))
            elif user["role"] == "profesores":
                return redirect(url_for("profesores_home"))
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

@app.route("/subadmin")
def subadmin_home():
    # proteger ruta: solo subadmin
    if session.get("role") != "subadmin":
        flash("Acceso denegado. Inicia sesión como subadministrador.", "error")
        return redirect(url_for("login"))
    return render_template("subadmin_home.html")

@app.route("/profesores")
def profesores_home():
    # proteger ruta: solo profesores
    if session.get("role") != "profesores":
        flash("Acceso denegado. Inicia sesión como profesores.", "error")
        return redirect(url_for("login"))
    return render_template("profesores_home.html")

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

@app.route("/editar_horas/<prof_id>")
def editar_horas(prof_id):
    prof = PROFESORES.get(prof_id)
    if not prof:
        return abort(404)
    horas = OFFICE_HOURS.get(prof_id, [])
    return render_template("editar_horas.html", prof=prof, horas=horas)

if __name__ == "__main__":
    app.run(debug=True)