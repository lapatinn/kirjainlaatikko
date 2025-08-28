import sqlite3
import math
import secrets
import markupsafe

from flask import Flask, render_template, request, redirect, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash

import config
from sql import users, reviews

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        error = "VIRHE: Et ole kirjautunut sisään!"
        return render_template("error_message.html", login_error=error)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def check_movie(title, rating, review, genre, director, year):
    # Check for non-empty title and string length
    if title.isspace() or len(title) <= 0 or len(title) > 75 \
        or len(review) <= 0 or len(review) > 1000 \
        or len(director) <= 0 or len(director) > 50:
        return False

    # Check integers
    if rating == "" or int(rating) <= 0 or int(rating) > 10 \
        or year == "" or int(year) < 1878 or int(year) > 2025:
        return False

    # Check that genre exists
    if genre == "":
        return False

    return True

def check_comment(comment):
    if len(comment) > 100:
        return False
    if comment.isspace():
        return False

    return True

# Newline filter
@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

# Frontpage
@app.route("/")
def index():
    movies = ["Terminator", "Star Wars", "Madagascar", "Autot 2", "Matin ennakkotehtävä (rare)"]
    return render_template("index.html", message="Parhaat elokuvat 2025", items=movies)

# Registration page
@app.route("/register")
def register():
    return render_template("register.html")

# Registration handler
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3:
        error = "VIRHE: Liian lyhyt nimi (väh. 3 merkkiä)!"
        flash(error)
        return render_template("register.html",  username=username, \
                        password1=password1, password2=password2)

    if password1 != password2:
        error = "VIRHE: Salasanat eivät täsmää!"
        flash(error)
        return render_template("register.html", username=username)

    if len(password1) < 3:
        error = "VIRHE: Liian lyhyt salasana (väh. 3 merkkiä)!"
        flash(error)
        return render_template("register.html", username=username)

    password_hash = generate_password_hash(password1)

    try:
        users.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        error = "VIRHE: Tunnus on jo varattu!"
        flash(error)
        return render_template("register.html", username=username, \
                               password1=password1, password2=password2)

    flash(f"Tunnus {username} luotu! Voit nyt kirjautua sisään.")
    return redirect("/")

# Login handler
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username and password:
        res = users.get_hash(username)
    else:
        error = "VIRHE: Tunnus ja salasana vaadittu!"
        flash(error)
        return redirect("/")

    # user.get_hash() returns an sql-object if no errors, 
    # otherwise the error message will be returned:
    if type(res) is str:
        flash(res)
        return redirect("/")
    else:
        user_id = res["id"]
        password_hash = res["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/")
    else:
        error = "VIRHE: väärä tunnus tai salasana!"
        return render_template("error_message.html", login_error=error)

# Logout handler
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        return redirect("/")

# New review page
@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

# New review handler
@app.route("/create_item", methods=["POST"])
def create_item():
    login_error = require_login()
    if login_error:
        return login_error

    check_csrf()

    user_id = session["user_id"]
    movie_title = request.form["title"]
    movie_rating = request.form["rating"]
    movie_review = request.form["review"]

    genre = request.form["genre"]
    director = request.form["director"]
    year = request.form["year"]

    if check_movie(movie_title, movie_rating, movie_review, \
                   genre, director, year):
        reviews.add_review(user_id, movie_title, movie_rating, \
                           movie_review, genre, director, year)
    else:
        error = "VIRHE: Tarkista syöte."
        flash(error)
        return redirect("/new_item")

    return redirect("/movie_reviews")

# New comment handler
@app.route("/create_comment", methods=["POST"])
def create_comment():
    login_error = require_login()
    if login_error:
        return login_error

    check_csrf()

    comment = request.form["comment"]
    user_id =  session["user_id"]
    review_id = request.form["review_id"]

    if check_comment(comment):
        reviews.add_comment(user_id, review_id, comment)
    else:
        error = "VIRHE: Tarkista kommentti"
        flash(error)
        return redirect("/movie_review/" + review_id)

    return redirect("/movie_review/" + review_id)

# Remove comment handler
@app.route("/remove_comment/<int:comment_id>", methods=["GET","POST"])
def remove_comment(comment_id):
    login_error = require_login()
    if login_error:
        return login_error

    comment = reviews.get_comment(comment_id)

    if type(comment) is str:
        return render_template("error_message.html", login_error=comment)

    if request.method == "GET":
        if comment["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden kommentteja!"
            return render_template("error_message.html", login_error=error)

    if request.method == "POST":
        check_csrf()
        if comment["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden kommentteja!"
            return render_template("error_message.html", login_error=error)

        review_id = comment[3]

        if "remove" in request.form:
            reviews.remove_comment(comment_id)
            return redirect("/movie_review/" + str(review_id))
        else:
            return redirect("/movie_review/" + str(review_id))

    return render_template("remove_comment.html", comment=comment)

# Edit review page
@app.route("/edit_review/<int:item_id>")
def edit_item(item_id):
    login_error = require_login()
    if login_error:
        return login_error

    review = reviews.get_review(item_id)
    info = reviews.get_info(item_id)

    if type(review) is str:
        return render_template("error_message.html", rnf_error=review)

    if review["user_id"] != session["user_id"]:
        error = "VIRHE: Et voi muokata muiden arvosteluja!"
        return render_template("error_message.html", rnf_error=error)

    return render_template("edit.html", item=review, info=info[0])

# Edit review handler
@app.route("/update_review", methods=["POST"])
def update_review():
    login_error = require_login()
    if login_error:
        return login_error

    check_csrf()

    review_id = request.form["item_id"]
    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        error = "VIRHE: Et voi muokata muiden arvosteluja!"
        return render_template("error_message.html", login_error=error)

    movie_title = request.form["title"]
    movie_rating = request.form["rating"]
    movie_review = request.form["review"]

    genre = request.form["genre"]
    director = request.form["director"]
    year = request.form["year"]

    if check_movie(movie_title, movie_rating, movie_review, genre, director, year):
        reviews.update_review(review_id, movie_title, movie_rating, movie_review,
                              genre, director, year)
    else:
        error = "VIRHE: Tarkista syöte!"
        flash(error)
        return redirect("/edit_review/" + str(review_id))

    return redirect("/movie_review/" + review_id)

# Remove review page
@app.route("/remove_review/<int:item_id>", methods=["GET","POST"])
def remove_review(item_id):
    login_error = require_login()
    if login_error:
        return login_error

    if request.method == "GET":
        review = reviews.get_review(item_id)
        if review["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden arvosteluja!"
            return render_template("error_message.html", login_error=error)

        return render_template("remove_review.html", item=review)

    # Remove review handler
    if request.method == "POST":
        check_csrf()
        review = reviews.get_review(item_id)

        if "remove" in request.form:
            if review["user_id"] != session["user_id"]:
                error = "VIRHE: Et voi poistaa muiden arvosteluja!"
                return render_template("error_message.html", login_error=error)
            else:
                reviews.remove_review(item_id)
                return redirect("/movie_reviews")
        else:
            return redirect("/movie_review/" + str(item_id))

# Search page
@app.route("/find_review")
def search_review():
    query = request.args.get("query")
    if query:
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []

    return render_template("find_review.html", query=query, results=results)

# All reviews page
@app.route("/movie_reviews")
@app.route("/movie_reviews/<int:page>")
def movie_reviews(page=1):
    page_size = 10
    review_count = reviews.review_count()[0]
    page_count = math.ceil(int(review_count) / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/movie_reviews/1")
    if page > page_count:
        return redirect("/movie_reviews/" + str(page_count))

    all_reviews = reviews.fetch_reviews(page, page_size)
    return render_template("movie_reviews.html", items=all_reviews,
                           page=page, page_count=page_count)

# Show review page
@app.route("/movie_review/<int:item_id>")
def page(item_id):
    review = reviews.get_review(item_id)
    info = reviews.get_info(item_id)
    comments = reviews.fetch_comments(item_id)

    if type(review) is str:
        # rnf = Review Not Found
        return render_template("error_message.html", rnf_error=review)
    else:
        return render_template("show_review.html", item=review, info=info, comments=comments)

# Show user page
@app.route("/show_user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if type(user) is str:
        # unf = User Not Found
        return render_template("error_message.html", unf_error=user)
    else:
        items = users.get_users_reviews(user_id)
        return render_template("show_user.html", user=user, reviews=items)

# All users page
@app.route("/all_users")
@app.route("/all_users/<int:page>")
def all_users(page=1):
    page_size = 20
    user_count = users.users_count()[0]
    page_count = math.ceil(int(user_count) / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/all_users/1")
    if page > page_count:
        return redirect("/all_users/" + str(page_count))

    all_users = users.fetch_users(page, page_size)
    return render_template("all_users.html", users=all_users,\
                        page=page, page_count=page_count)

if __name__ == "__main__":
    app.run(debug=False)
