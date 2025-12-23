from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# CONFIG MYSQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "juegos_db"

mysql = MySQL(app)

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE usuario=%s AND password=SHA2(%s,256)",
            (user, password)
        )
        admin = cur.fetchone()
        cur.close()

        if admin:
            session["admin"] = True
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


# ---------- INDEX ----------
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM juegos")
    juegos = cur.fetchall()
    cur.close()
    return render_template("index.html", juegos=juegos)


# ---------- AGREGAR ----------
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        link = request.form["link"]
        imagen = request.form["imagen"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO juegos (nombre, link, imagen) VALUES (%s,%s,%s)",
            (nombre, link, imagen)
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("index"))

    return render_template("agregar.html")


# ---------- ELIMINAR ----------
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM juegos WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
