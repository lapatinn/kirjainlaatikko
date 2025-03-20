from flask import Flask
from flask import render_template, request, redirect, session # flask
from werkzeug.security import generate_password_hash, check_password_hash # werkzeug
import sqlite3 # sql
import db, config # omat moduulit

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    movies = ["Terminator", "Star Wars", "Madagascar", "Vamppyyri elokuva", "Matin ennakkotehtävä"]
    return render_template("index.html", message="Parhaat elokuvat 2025", items=movies)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"]) # Luo tunnus
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])[0]
    user_id = result["id"]
    password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/new_item") # uusi arvostelu
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    movie_title = request.form["title"]
    movie_rating = request.form["rating"]
    movie_review = request.form["review"]
    user_id = session["user_id"]

    sql = "INSERT INTO reviews (user_id, movie, rating, review) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, movie_title, movie_rating, movie_review])

    return redirect("/")

@app.route("/numbers")
def numbers():
    content = ""
    for i in range(1,101):
        content += str(i) + " "
    return content

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    message = request.form["message"]
    return render_template("result.html", message=message)

if __name__ == "__main__":
    app.run(debug=False)