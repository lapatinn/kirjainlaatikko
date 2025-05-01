from flask import Flask
from flask import render_template, request, redirect, session, abort, flash # flask
from werkzeug.security import generate_password_hash, check_password_hash # werkzeug
import sqlite3 # sql
import config, reviews, users # omat moduulit

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        error = "VIRHE: Et ole kirjautunut sisään."
        return render_template("error_message.html", login_error=error)
    
def check_movie(title, rating, review, genre, director, year):
    # Kaikki olemassa
    if title and rating and review and genre and director and year: 
        data_exists = True
    else:
        return False
    
    # Merkkijonot oikean pituiset
    if len(title) > 0 and len(title) <= 75 and len(review) > 0 and len(review) <= 1000 and len(director) > 0 and len(director) <= 50:
        # Tarkistan vaan titlen koska ainoo joka aiheuttaa ongelmii kosk arvosteluu ei voi klikkaa
        # muut saa periaattees olla tyhjii iha sama ei ne vaikuta mihkää mitenkää
        if title == " " or title == "  " or title == "   " or title == "    " or title == "     ": 
        # Ihan vitun luolamies logiikkaketju mut sano mun sanoneen tää on bulletproof :DD
        # Ei kukaa laittais yli 5 välilyöntii jos tarkotuksena on tehä "empty title troll"
            return False
        string_length = True
    else:
        return False
    
    # Kokonaisluvut oikealla lukuvälillä
    if int(rating) >= 0 and int(rating) <= 10 and int(year) >= 1878 and int(year) <= 2025:
        int_values = True
    else:
        return False
    
    if data_exists and string_length and int_values:
        return True
    else:
        return False

@app.route("/")
def index():
    movies = ["Terminator", "Star Wars", "Madagascar", "Autot 2", "Matin ennakkotehtävä"]
    return render_template("index.html", message="Parhaat elokuvat 2025", items=movies)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"]) # Luo tunnus
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3:
        error = "VIRHE: Liian lyhyt nimi (väh. 3 merkkiä)!"
        flash(error)
        return redirect("/register")
    if password1 != password2:
        error = "VIRHE: Salasanat eivät täsmää!"
        flash(error)
        return redirect("/register")
    if len(password1) < 3:
        error = "VIRHE: Liian lyhyt salasana (väh. 3 merkkiä)!"
        flash(error)
        return redirect("/register") 
       
    password_hash = generate_password_hash(password1)

    try:
        users.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    
    flash(f"Tunnus {username} luotu! Voit nyt kirjautua sisään.")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username and password:
        res = users.get_hash(username)
    else:
        error = "VIRHE: Et voi kirjautua ilman tunnusta!"
        flash(error)
        return redirect("/")

    # get_hash palauttaa sqlite-olion jos käyttäjä ja salasana löytyy, muuten virheviestin:
    if type(res) is str: 
        flash("VIRHE: Tunnus/salasana eivät ole tietokannassa!")
        return redirect("/")
    else:
        user_id = res["id"]
        password_hash = res["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        error = "VIRHE: väärä tunnus tai salasana!"
        return render_template("error_message.html", login_error=error)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        return redirect("/")

@app.route("/new_item") # uusi arvostelu
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    login_error = require_login()
    if login_error:
        return login_error
    
    user_id = session["user_id"] # Session on oltava olemassa jotta arvostelu voidaan jättää
    movie_title = request.form["title"]
    movie_rating = request.form["rating"]
    movie_review = request.form["review"]

    genre = request.form["genre"]
    director = request.form["director"]
    year = request.form["year"]

    if check_movie(movie_title, movie_rating, movie_review, genre, director, year):
        reviews.add_review(user_id, movie_title, movie_rating, movie_review, genre, director, year)
    else:
        error = "VIRHE: Tarkista syöte."
        flash(error)
        return redirect("/new_item")

    return redirect("/movie_reviews")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    login_error = require_login()
    if login_error:
        return login_error
    
    comment = request.form["comment"]
    user_id =  session["user_id"]
    review_id = request.form["review_id"]

    if len(comment) <= 100:
        reviews.add_comment(user_id, review_id, comment)   
    else:
        error = "VIRHE: Kommenttisi on liian pitkä"
        return render_template("error_message.html", comment_error=error)
    
    return redirect("/movie_reviews/" + review_id)

@app.route("/remove_comment/<int:comment_id>", methods=["GET","POST"])
def remove_comment(comment_id):
    login_error = require_login()
    if login_error:
        return login_error
    
    comment = reviews.get_comment(comment_id)

    if type(comment) is str:
        # Tähän login error koska vain etusivulle nappi
        return render_template("error_message.html", login_error=comment)

    if request.method == "GET":
        if comment["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden kommentteja."
            return render_template("error_message.html", login_error=error)

    if request.method == "POST":
        if comment["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden kommentteja."
            return render_template("error_message.html", login_error=error)
        
        review_id = comment[3]

        if "remove" in request.form:
            reviews.remove_comment(comment_id)
            return redirect("/movie_reviews/" + str(review_id))
        else:
            return redirect("/movie_reviews/" + str(review_id))

    return render_template("remove_comment.html", comment=comment)

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
        error = "VIRHE: Et voi muokata muiden arvosteluja."
        return render_template("error_message.html", rnf_error=error)

    return render_template("edit.html", item=review, info=info[0])

@app.route("/update_review", methods=["POST"])
def update_review():
    login_error = require_login()
    if login_error:
        return login_error
    
    review_id = request.form["item_id"]
    review = reviews.get_review(review_id)

    if review["user_id"] != session["user_id"]:
        error = "VIRHE: Et voi muokata muiden arvosteluja."
        return render_template("error_message.html", login_error=error)

    movie_title = request.form["title"]
    movie_rating = request.form["rating"]
    movie_review = request.form["review"]

    genre = request.form["genre"]
    director = request.form["director"]
    year = request.form["year"]

    if check_movie(movie_title, movie_rating, movie_review, genre, director, year):
        reviews.update_review(review_id, movie_title, movie_rating, movie_review, genre, director, year)
    else:
        error = "VIRHE: Älä jaksa oikeesti kokoajan tehä kepposia.. (Tarkista syöte)"
        flash(error)
        return redirect("/edit_review/" + str(review_id))

    return redirect("/movie_reviews/" + review_id)

@app.route("/remove_review/<int:item_id>", methods=["GET","POST"])
def remove_review(item_id):
    login_error = require_login()
    if login_error:
        return login_error
    
    if request.method == "GET":
        review = reviews.get_review(item_id)
        if review["user_id"] != session["user_id"]:
            error = "VIRHE: Et voi poistaa muiden arvosteluja."
            return render_template("error_message.html", login_error=error)
        
        return render_template("remove_review.html", item=review)
    
    if request.method == "POST":
        review = reviews.get_review(item_id)

        if "remove" in request.form:
            if review["user_id"] != session["user_id"]:
                error = "VIRHE: Et voi poistaa muiden arvosteluja."
                return render_template("error_message.html", login_error=error)
            else:
                reviews.remove_review(item_id)
                return redirect("/movie_reviews")
        else:
            return redirect("/movie_reviews/" + str(item_id))
        
@app.route("/find_review")
def search_review():
    query = request.args.get("query")
    if query:
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []

    return render_template("find_review.html", query=query, results=results)

@app.route("/movie_reviews")
def movie_reviews():
    all_reviews = reviews.fetch_reviews()
    return render_template("movie_reviews.html", items=all_reviews)

@app.route("/movie_reviews/<int:item_id>")
def page(item_id):
    review = reviews.get_review(item_id) # Hakee id:llä kaiken arvosteluun liittyvän tiedon
    info = reviews.get_info(item_id) # Hakee luokat
    comments = reviews.fetch_comments(item_id)

    if type(review) is str:
        # rnf = Review Not Found 
        return render_template("error_message.html", rnf_error=review)
    else:
        return render_template("show_review.html", item=review, info=info, comments=comments) # passataan id ja info html tiedostoon

@app.route("/show_user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if type(user) is str:
        # unf = User Not Found
        return render_template("error_message.html", unf_error=user)
    else:
        items = users.get_users_reviews(user_id)
        return render_template("show_user.html", user=user, reviews=items)

@app.route("/all_users")
def all_users():
    guys = users.fetch_users()
    return render_template("all_users.html", users=guys)

if __name__ == "__main__":
    app.run(debug=False)