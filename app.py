from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key_very_insecure")


PROFESSOR_NAMES = {
    "luis.colon19@upr.edu": "Luis Colón Colón",
    "eliana.valenzuela@upr.edu": "Eliana Valenzuela Andrade",
    "juano.lopez@upr.edu": "Juan Lopez Gerena",
    "aixa.ramirez@upr.edu": "Aixa Ramirez Toledo",
    "emilio.perez@upr.edu": "Emilio Pérez Arnau",
}

# Term activo
TERMS = ["C51"]


# Horas de oficina
OFFICE_HOURS = {
    "luis.colon19@upr.edu": [
        {"day": "Lunes", "start": "11:30 AM", "end": "12:30 PM", "term": "C51"},
        {"day": "Lunes", "start": "2:30 PM",  "end": "3:00 PM",  "term": "C51"},
        {"day": "Miércoles", "start": "11:30 AM", "end": "12:30 PM", "term": "C51"},
        {"day": "Miércoles", "start": "2:30 PM",  "end": "3:00 PM",  "term": "C51"},
    ],
    "eliana.valenzuela@upr.edu": [
        {"day": "Lunes", "start": "8:00 AM", "end": "10:00 AM", "term": "C51"},
        {"day": "Miércoles", "start": "8:00 AM", "end": "10:00 AM", "term": "C51"},
        {"day": "Viernes", "start": "8:00 AM", "end": "10:00 AM", "term": "C51"},
    ],
    "juano.lopez@upr.edu": [
        {"day": "Lunes", "start": "8:00 AM", "end": "10:30 AM", "term": "C51"},
        {"day": "Miércoles", "start": "8:00 AM", "end": "10:30 AM", "term": "C51"},
        {"day": "Martes", "start": "8:00 AM", "end": "8:30 AM", "term": "C51"},
        {"day": "Jueves", "start": "8:00 AM", "end": "8:30 AM", "term": "C51"},
    ],
    "aixa.ramirez@upr.edu": [
        {"day": "Martes", "start": "1:45 PM", "end": "4:30 PM", "term": "C51"},
        {"day": "Jueves", "start": "1:45 PM", "end": "4:30 PM", "term": "C51"},
    ],
    "emilio.perez@upr.edu": [
        {"day": "Martes", "start": "7:00 AM", "end": "8:00 AM", "term": "C51"},
        {"day": "Martes", "start": "10:00 AM", "end": "10:30 AM", "term": "C51"},
        {"day": "Martes", "start": "4:00 PM", "end": "5:30 PM", "term": "C51"},
        {"day": "Jueves", "start": "7:00 AM", "end": "8:00 AM", "term": "C51"},
        {"day": "Jueves", "start": "10:00 AM", "end": "10:30 AM", "term": "C51"},
        {"day": "Jueves", "start": "4:00 PM", "end": "5:30 PM", "term": "C51"},
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

    return render_template("profesores_home.html", prof_id="luis.colon19@upr.edu")

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

@app.route("/departamentos/ccom")
def departamento_ccom():
    
    if not session.get("email"):
        return redirect(url_for("login"))

    
    ccom_prof_ids = [
        "luis.colon19@upr.edu",
        "juano.lopez@upr.edu",
        "eliana.valenzuela@upr.edu",
        "aixa.ramirez@upr.edu",
        "emilio.perez@upr.edu",
    ]

    profesores = []
    for pid in ccom_prof_ids:
        nombre = PROFESSOR_NAMES.get(pid, pid)
        horas_brutas = OFFICE_HOURS.get(pid, [])

       
        horarios = []
        for h in horas_brutas:
            horarios.append(f"{h['day']} {h['start']} - {h['end']}")

        profesores.append({
            "nombre": f"Prof. {nombre}",
            "email": pid,
            "horarios": horarios
        })

    return render_template("departamento_ccom.html", profesores=profesores)

@app.route("/editar_cuentas")
def editar_cuentas():
    return render_template("editar_cuentas.html")

@app.route("/editar_horas/<prof_id>")
def editar_horas(prof_id):
    if prof_id not in OFFICE_HOURS:
        abort(404)

    prof = {
        "email": prof_id,
        "nombre": PROFESSOR_NAMES.get(prof_id, prof_id)
    }

    horas = [
        {"dia": h["day"], "inicio": h["start"], "fin": h["end"], "term": h["term"]}
        for h in OFFICE_HOURS[prof_id]
    ]

    return render_template(
        "editar_horas.html",
        prof=prof,
        horas=horas,
        terms=TERMS
    )


@app.route("/api/office-hour/update", methods=["POST"])
def api_update_office_hour():
    data = request.get_json(force=True)
    email = data.get("email")
    index = data.get("index")
    day   = data.get("day")
    start = data.get("start")
    end_  = data.get("end")
    term  = data.get("term")

    if not (email in OFFICE_HOURS and isinstance(index, int)):
        return jsonify({"ok": False, "error": "Parámetros inválidos"}), 400

    # Validaciones simples de formato
    def _valid_time(s):
        try:
            hhmm, ap = s.split()
            hh, mm = hhmm.split(":")
            hh = int(hh); mm = int(mm)
        except Exception:
            return False
        return (1 <= hh <= 12) and (0 <= mm <= 59) and ap in ("AM", "PM")

    if day not in ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]:
        return jsonify({"ok": False, "error": "Día inválido"}), 400
    if not _valid_time(start) or not _valid_time(end_):
        return jsonify({"ok": False, "error": "Hora inválida"}), 400
    if term not in TERMS:
        return jsonify({"ok": False, "error": "Term inválido"}), 400

    hours = OFFICE_HOURS[email]
    if 0 <= index < len(hours):
        hours[index] = {"day": day, "start": start, "end": end_, "term": term}
    else:
        return jsonify({"ok": False, "error": "Índice fuera de rango"}), 400

    return jsonify({"ok": True})

@app.route("/agregar-hora/<prof_id>", methods=["GET", "POST"])
def agregar_hora_oficina(prof_id):
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))
    
    prof = PROFESSOR_NAMES.get(prof_id)
    
    if not prof:
        return abort(404)

    if request.method == "POST":
        dia = request.form["dia"]
        inicio = request.form["inicio"]
        fin = request.form["fin"]
        
        nueva_hora = {
            "dia": dia,
            "inicio": inicio,
            "fin": fin,
            "term": TERMS[0]
        }
        
        # Inicializar la lista si no existe
        if prof_id not in OFFICE_HOURS:
            OFFICE_HOURS[prof_id] = []
            
        OFFICE_HOURS[prof_id].append(nueva_hora)
        
        flash(f"Nueva hora agregada para {prof.get('nombre')}.", "success")
        return redirect(url_for("editar_horas_oficina", prof_id=prof_id))
    
    # Renderizar el formulario (GET)
    return render_template("agregar_hora_oficina.html", prof=prof, prof_id=prof_id)

@app.route("/api/office-hour/delete", methods=["POST"])
def api_delete_office_hour():
    data = request.get_json(force=True)
    email = data.get("email")
    index = data.get("index")

    if email not in OFFICE_HOURS or not isinstance(index, int):
        return jsonify({"ok": False, "error": "Parámetros inválidos"}), 400

    hours = OFFICE_HOURS[email]
    if 0 <= index < len(hours):
        hours.pop(index)
        return jsonify({"ok": True})

    return jsonify({"ok": False, "error": "Índice fuera de rango"}), 400

@app.route('/confirmar_citas')
def confirmar_citas():
    # Simulación de datos reales desde base de datos
    profesor = "Luis Colón"
    citas = [
        {
            "id": 1,
            "estudiante": "Sebastian Soto Delgado",
            "dia": "Martes",
            "hora_inicio": "10:30",
            "hora_fin": "11:00"
        },
        {
            "id": 2,
            "estudiante": "Dereck Declet",
            "dia": "Jueves",
            "hora_inicio": "11:30",
            "hora_fin": "12:00"
        }
    ]

    return render_template("confirmar_citas.html", profesor=profesor, citas=citas)



if __name__ == "__main__":
    app.run(debug=True)


