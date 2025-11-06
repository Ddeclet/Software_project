from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key_very_insecure")

# --- COLECCIONES GLOBALES (Simulación de DB) ---

# Profesores
PROFESORES = {
    "luis-colon":        {"nombre": "Prof. Luis Colón Cólon", "email": "luis.colon19@upr.edu"},
    "eliana-valenzuela": {"nombre": "Prof. Eliana Valenzuela Andrade", "email": "eliana.valenzuela@upr.edu"},
    "juan-lopez":        {"nombre": "Prof. Juan Lopez Gerena", "email": "juano.lopez@upr.edu"},
    "aixa-ramirez":      {"nombre": "Prof. Aixa Ramirez Toledo", "email": "aixa.ramirez@upr.edu"},
    "emilio-perez":      {"nombre": "Prof. Emilio Pérez Arnau", "email": "emilio.perez@upr.edu"},
}

# Term activo
TERMS = ["C51"]

# Horas de oficina
OFFICE_HOURS = {
    "luis-colon": [
        {"dia": "Lunes", "inicio": "11:30", "fin": "12:30", "term": TERM_ACTUAL},
        {"dia": "Lunes", "inicio": "14:30", "fin": "15:00", "term": TERM_ACTUAL},
        {"dia": "Miércoles", "inicio": "10:00", "fin": "11:00", "term": TERM_ACTUAL},
    ],
    "aixa-ramirez": [
        {"dia": "Martes", "inicio": "09:00", "fin": "10:00", "term": TERM_ACTUAL},
    ]
}

# Usuarios de prueba (incluyendo subadmin)
USERS = {
    "javier@gmail.com":      {"password": "usuario1234", "role": "user"},
    "javierAdmin@gmail.com": {"password": "admin1234",   "role": "superadmin"},
    "subadmin@upr.edu":      {"password": "subadmin123", "role": "subadmin"},
}


# --- RUTAS DE AUTENTICACIÓN ---

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = USERS.get(email)
        if user and password == user["password"]:
            
            # Guardar sesión
            session["email"] = email
            session["role"] = user["role"]

            # Redirigir según rol
            if user["role"] == "superadmin":
                return redirect(url_for("superadmin_home"))
            elif user["role"] == "subadmin":
                return redirect(url_for("subadmin_home"))
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


# --- RUTAS PRINCIPALES ---

@app.route("/superadmin")
def superadmin_home():
    if session.get("role") != "superadmin":
        flash("Acceso denegado. Inicia sesión como administrador.", "error")
        return redirect(url_for("login"))
    return render_template("superadmin_home.html")

@app.route("/subadmin")
def subadmin_home():
    if session.get("role") != "subadmin":
        flash("Acceso denegado. Permiso de subadministrador requerido.", "error")
        return redirect(url_for("login"))
    return render_template("subadmin_home.html")

@app.route("/inicio")
def index():
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

# --- GESTIÓN DE CUENTAS Y HORAS (ADMIN/SUBADMIN) ---

@app.route("/modificar-cuenta")
def modificar_cuenta():
    # Proteger ruta: solo subadmin y superadmin pueden acceder
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado. Permiso de administrador o subadministrador requerido.", "error")
        return redirect(url_for("login"))
    
    # Pasa las colecciones PROFESORES y OFFICE_HOURS al template
    return render_template("modificar_cuenta.html", profesores=PROFESORES, office_hours=OFFICE_HOURS)

@app.route("/editar-info/<prof_id>")
def editar_info_cuenta(prof_id):
    # Proteger ruta (solo admin/subadmin)
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))
        
    prof = PROFESORES.get(prof_id)
    if not prof:
        return abort(404)
        
    # Lógica para editar info... (Pendiente de implementación)
    return f"Página de edición de información para {prof.get('nombre')}"

@app.route("/editar-horas/<prof_id>")
def editar_horas_oficina(prof_id):
    # Proteger ruta: solo subadmin y superadmin
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))
    
    # Obtener la data del profesor de la lista global
    prof = PROFESORES.get(prof_id)
    if not prof:
        return abort(404)
        
    # Obtener las horas de oficina
    horas = OFFICE_HOURS.get(prof_id, [])
    
    # Pasamos 'prof', 'prof_id' y 'horas' al template
    return render_template("editar_horas_oficina.html", prof=prof, prof_id=prof_id, horas=horas)

@app.route("/agregar-hora/<prof_id>", methods=["GET", "POST"])
def agregar_hora_oficina(prof_id):
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))
    
    prof = PROFESORES.get(prof_id)
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
            "term": TERM_ACTUAL
        }
        
        # Inicializar la lista si no existe
        if prof_id not in OFFICE_HOURS:
            OFFICE_HOURS[prof_id] = []
            
        OFFICE_HOURS[prof_id].append(nueva_hora)
        
        flash(f"Nueva hora agregada para {prof.get('nombre')}.", "success")
        return redirect(url_for("editar_horas_oficina", prof_id=prof_id))
    
    # Renderizar el formulario (GET)
    return render_template("agregar_hora_oficina.html", prof=prof, prof_id=prof_id)


@app.route("/editar-hora/<prof_id>/<int:hora_id>", methods=["GET", "POST"])
def editar_hora(prof_id, hora_id):
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))

    prof = PROFESORES.get(prof_id)
    horas = OFFICE_HOURS.get(prof_id, [])

    if not prof or hora_id >= len(horas):
        flash("Hora de oficina o profesor no encontrado.", "error")
        return redirect(url_for("modificar_cuenta"))

    hora_a_editar = horas[hora_id]

    if request.method == "POST":
        # Actualizar los datos
        hora_a_editar["dia"] = request.form["dia"]
        hora_a_editar["inicio"] = request.form["inicio"]
        hora_a_editar["fin"] = request.form["fin"]
        
        flash("Hora de oficina actualizada exitosamente.", "success")
        return redirect(url_for("editar_horas_oficina", prof_id=prof_id))

    return render_template("editar_hora_detalle.html", 
                           prof=prof, 
                           prof_id=prof_id, 
                           hora_id=hora_id, 
                           hora_a_editar=hora_a_editar)


@app.route("/eliminar-hora/<prof_id>/<int:hora_id>", methods=["POST"])
def eliminar_hora(prof_id, hora_id):
    # Proteger ruta
    role = session.get("role")
    if role not in ["superadmin", "subadmin"]:
        flash("Acceso denegado.", "error")
        return redirect(url_for("login"))

    horas = OFFICE_HOURS.get(prof_id, [])
    
    # Validación de índice
    if hora_id >= len(horas):
        flash("Hora de oficina no encontrada.", "error")
        return redirect(url_for("editar_horas_oficina", prof_id=prof_id))
    
    # Eliminar la hora usando el índice
    del horas[hora_id]
    
    flash("Hora de oficina eliminada exitosamente.", "success")
    return redirect(url_for("editar_horas_oficina", prof_id=prof_id))


if __name__ == "__main__":
    app.run(debug=True)