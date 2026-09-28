from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Clave necesaria para utilizar las sesiones
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave-secreta-reconciliacion"
)


# -------------------------
# BASE DE DATOS
# -------------------------

def crear_base_datos():

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peticiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            peticion TEXT NOT NULL,
            fecha TEXT,
            estado TEXT DEFAULT 'Pendiente'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY,
            cantidad INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO visitas (id, cantidad)
        VALUES (1, 0)
    """)

    columnas = cursor.execute(
        "PRAGMA table_info(peticiones)"
    ).fetchall()

    nombres_columnas = [columna[1] for columna in columnas]

    if "fecha" not in nombres_columnas:

        cursor.execute(
            "ALTER TABLE peticiones ADD COLUMN fecha TEXT"
        )

    if "estado" not in nombres_columnas:

        cursor.execute(
            "ALTER TABLE peticiones ADD COLUMN estado TEXT DEFAULT 'Pendiente'"
        )

    cursor.execute("""
        UPDATE peticiones
        SET fecha = 'Sin fecha'
        WHERE fecha IS NULL
    """)

    cursor.execute("""
        UPDATE peticiones
        SET estado = 'Pendiente'
        WHERE estado IS NULL
    """)

    conexion.commit()
    conexion.close()
    conexion.close()# -------------------------
# PÁGINA PRINCIPAL
# -------------------------

@app.route("/")
def inicio():

    versiculos = [
        {
            "texto": "Acercaos a Dios, y él se acercará a vosotros.",
            "referencia": "Santiago 4:8"
        },
        {
            "texto": "Todo lo puedo en Cristo que me fortalece.",
            "referencia": "Filipenses 4:13"
        },
        {
            "texto": "El Señor es mi pastor; nada me faltará.",
            "referencia": "Salmos 23:1"
        },
        {
            "texto": "Confía en el Señor con todo tu corazón.",
            "referencia": "Proverbios 3:5"
        },
        {
            "texto": "Esfuérzate y sé valiente; no temas ni desmayes.",
            "referencia": "Josué 1:9"
        }
    ]

    from datetime import date

    dia = date.today().timetuple().tm_yday

    versiculo = versiculos[dia % len(versiculos)]
    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE visitas
        SET cantidad = cantidad + 1
        WHERE id = 1
    """)

    conexion.commit()

    cursor.execute("""
        SELECT cantidad
        FROM visitas
        WHERE id = 1
    """)

    visitas = cursor.fetchone()[0]

    conexion.close()
    return render_template(
        "index.html",
        versiculo=versiculo,
        visitas=visitas
    )
# -------------------------
# DEVOCIONALES
# -------------------------

devocionales = [

    {
        "titulo": "Un nuevo comienzo",
        "texto": "Cada día puede ser una oportunidad para volver a acercarte a Dios. No importa cuánto tiempo hayas estado lejos; siempre puedes decidir dar un paso hacia Él.",
        "versiculo": "Acercaos a Dios, y él se acercará a vosotros.",
        "referencia": "Santiago 4:8"
    },

    {
        "titulo": "Confía en Dios",
        "texto": "Hay momentos en los que no sabemos qué camino tomar. En esos momentos podemos aprender a confiar en Dios y buscar su dirección.",
        "versiculo": "Confía en el Señor con todo tu corazón.",
        "referencia": "Proverbios 3:5"
    },

    {
        "titulo": "Dios conoce tu corazón",
        "texto": "Puedes hablar con Dios con sinceridad. Él conoce tus pensamientos, tus preocupaciones y aquello que llevas dentro.",
        "versiculo": "Examíname, oh Dios, y conoce mi corazón.",
        "referencia": "Salmos 139:23"
    },

    {
        "titulo": "No estás solo",
        "texto": "Cuando atraviesas momentos difíciles, recuerda que puedes buscar a Dios. La fe puede ayudarte a encontrar esperanza y fortaleza para continuar.",
        "versiculo": "No temas, porque yo estoy contigo.",
        "referencia": "Isaías 41:10"
    },

    {
        "titulo": "El valor de perdonar",
        "texto": "Perdonar puede ser difícil, pero aprender a dejar atrás el resentimiento puede abrir espacio para la paz y la restauración.",
        "versiculo": "Sed bondadosos unos con otros, misericordiosos.",
        "referencia": "Efesios 4:32"
    },

    {
        "titulo": "Camina paso a paso",
        "texto": "No tienes que cambiar todo de un momento para otro. Puedes comenzar con pequeñas decisiones y buscar a Dios cada día.",
        "versiculo": "Lámpara es a mis pies tu palabra.",
        "referencia": "Salmos 119:105"
    },

    {
        "titulo": "Hay esperanza",
        "texto": "Incluso después de cometer errores, tu historia puede continuar. Puedes aprender, cambiar y comenzar nuevamente con esperanza.",
        "versiculo": "Las misericordias del Señor son nuevas cada mañana.",
        "referencia": "Lamentaciones 3:22-23"
    }

]
# -------------------------
# REFLEXIONES
# -------------------------
# -------------------------
# RECONCILIARSE CON DIOS
# -------------------------

@app.route("/reconciliarse")
def reconciliarse():

    return render_template(
        "reconciliarse.html"
    )
# -------------------------
# VERSÍCULOS
# -------------------------

@app.route("/versiculos")
def versiculos():

    return render_template(
        "versiculos.html"
    )
# -------------------------
# PLAN DE 7 DÍAS
# -------------------------

@app.route("/plan")
def plan():

    return render_template(
        "plan.html"
    )
# -------------------------
# DEVOCIONAL DEL DÍA
# -------------------------

@app.route("/devocional")
def devocional():

    from datetime import date

    dia = date.today().timetuple().tm_yday

    devocional_actual = devocionales[dia % len(devocionales)]

    return render_template(
        "devocional.html",
        devocional=devocional_actual
    )
# -------------------------
# ORACIONES
# -------------------------

@app.route("/oraciones")
def oraciones():

    return render_template(
        "oraciones.html"
    )
@app.route("/reflexiones")
def reflexiones():

    busqueda = request.args.get("buscar", "").strip().lower()

    if busqueda:

        reflexiones_filtradas = [
            reflexion
            for reflexion in reflexiones_data
            if busqueda in reflexion["titulo"].lower()
            or busqueda in reflexion["texto"].lower()
            or busqueda in reflexion["pregunta"].lower()
        ]

    else:

        reflexiones_filtradas = reflexiones_data

    return render_template(
        "reflexiones.html",
        reflexiones=reflexiones_filtradas,
        busqueda=busqueda
    ) 

@app.route("/reflexion-aleatoria")
def reflexion_aleatoria():

    import random

    reflexion = random.choice(reflexiones_data)

    return render_template(
        "reflexion.html",
        reflexion=reflexion
    )
@app.route("/mensaje")
def mensaje():

    return render_template(
        "mensaje.html"
    )
# -------------------------
# DATOS DE LAS REFLEXIONES
# -------------------------

reflexiones_data = [

    {   
        "id": 1,  

        "titulo": "Volver a empezar",

        "texto": "A veces podemos alejarnos de Dios y sentir que hemos tomado demasiados caminos equivocados. Sin embargo, regresar a Él siempre puede ser un nuevo comienzo. La reconciliación comienza cuando reconocemos dónde estamos y decidimos acercarnos nuevamente a Dios.",

        "versiculo": "Acercaos a Dios, y él se acercará a vosotros.",

        "referencia": "Santiago 4:8",

        "pregunta": "¿Hay alguna parte de tu vida en la que sientas que necesitas acercarte nuevamente a Dios?"
    },


    {
        "id": 2,

        "titulo": "El valor del perdón",

        "texto": "Reconocer nuestros errores no siempre es fácil. Pedir perdón requiere sinceridad y humildad, pero también puede abrir el camino hacia una nueva etapa. El perdón nos recuerda que nuestros errores no tienen que definir todo nuestro futuro.",

        "versiculo": "Si confesamos nuestros pecados, él es fiel y justo para perdonar nuestros pecados.",

        "referencia": "1 Juan 1:9",

        "pregunta": "¿Hay algo que necesitas reconocer delante de Dios con sinceridad?"
    },


    {
        "id": 3,

        "titulo": "No estás solo",

        "texto": "Hay momentos en los que podemos sentirnos solos o confundidos. La fe nos recuerda que podemos buscar a Dios incluso en esos momentos. Podemos hablar con Él, confiar y continuar caminando paso a paso.",

        "versiculo": "No temas, porque yo estoy contigo.",

        "referencia": "Isaías 41:10",

        "pregunta": "¿En qué situación de tu vida necesitas recordar que puedes confiar en Dios?"
    },     {
         "id": 4,

        "titulo": "La esperanza permanece",

        "texto": "Incluso cuando atravesamos momentos difíciles, podemos recordar que la esperanza no desaparece. Acercarnos a Dios puede ayudarnos a encontrar fuerzas para continuar y mirar el futuro con confianza.",

        "versiculo": "Los que esperan en el Señor tendrán nuevas fuerzas.",

        "referencia": "Isaías 40:31",

        "pregunta": "¿Qué situación de tu vida necesitas poner hoy en las manos de Dios?"
    },


    {
        "id": 5,

        "titulo": "Un corazón sincero",

        "texto": "Dios conoce nuestro corazón y nuestras luchas. No necesitamos aparentar ser perfectos para acercarnos a Él. Podemos hablarle con sinceridad y reconocer aquello que queremos cambiar.",

        "versiculo": "Crea en mí, oh Dios, un corazón limpio.",

        "referencia": "Salmos 51:10",

        "pregunta": "¿Qué cambio te gustaría comenzar a hacer en tu vida?"
    }

]
@app.route("/reflexion/<int:id>")
def reflexion(id):

    if id < 1 or id > len(reflexiones_data):

        return "Reflexión no encontrada", 404

    reflexion_actual = reflexiones_data[id - 1]

    return render_template(
        "reflexion.html",
        reflexion=reflexion_actual
    )

# -------------------------
# PETICIONES DE ORACIÓN
# -------------------------

@app.route("/peticion", methods=["GET", "POST"])
def peticion():

    if request.method == "POST":

        from datetime import datetime

        nombre = request.form["nombre"]
        mensaje = request.form["peticion"]

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        conexion = sqlite3.connect("database.db")

        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO peticiones
            (nombre, peticion, fecha, estado)
            VALUES (?, ?, ?, ?)
            """,
            (nombre, mensaje, fecha, "Pendiente")
        )

        conexion.commit()

        conexion.close()

        return """
        <h1>🙏 Petición recibida</h1>

        <p>
            Gracias por compartir tu petición.
        </p>

        <a href="/">
            Volver al inicio
        </a>
        """

    return render_template("peticion.html")


# -------------------------
# INICIO DE SESIÓN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form["password"]

        # Contraseña de prueba
        if password == os.environ.get("ADMIN_PASSWORD"):

            session["admin"] = True

            return redirect(url_for("admin"))

        else:

            return render_template(
                "login.html",
                error="Contraseña incorrecta"
            )

    return render_template("login.html")


# -------------------------
# PANEL DE ADMINISTRACIÓN
# -------------------------

# -------------------------
# PANEL DE ADMINISTRACIÓN
# -------------------------

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM peticiones")

    peticiones = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) FROM peticiones WHERE estado = 'Pendiente'"
    )

    pendientes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM peticiones WHERE estado = 'Atendida'"
    )

    atendidas = cursor.fetchone()[0]

    total = len(peticiones)

    conexion.close()

    return render_template(
        "admin.html",
        peticiones=peticiones,
        pendientes=pendientes,
        atendidas=atendidas,
        total=total
    )


# -------------------------
# MARCAR PETICIÓN COMO ATENDIDA
# -------------------------

@app.route("/atender/<int:id>")
def atender(id):

    if not session.get("admin"):

        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE peticiones
        SET estado = 'Atendida'
        WHERE id = ?
        """,
        (id,)
    )

    conexion.commit()

    conexion.close()

    return redirect(url_for("admin"))
# -------------------------
# ELIMINAR PETICIÓN
# -------------------------

@app.route("/eliminar/<int:id>")
def eliminar(id):

    if not session.get("admin"):

        return redirect(url_for("login"))

    conexion = sqlite3.connect("database.db")

    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM peticiones
        WHERE id = ?
        """,
        (id,)
    )

    conexion.commit()

    conexion.close()

    return redirect(url_for("admin"))
#-------------------------
# CERRAR SESIÓN
# -------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -------------------------
# INICIAR SERVIDOR
# -------------------------

if __name__ == "__main__":

    crear_base_datos()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
