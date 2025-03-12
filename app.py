from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    movies = ["Terminator", "Star Wars", "Madagascar",]
    return render_template("index.html", message="Parhaat elokuvat 2025", items=movies)

@app.route("/page1")
def page1():
    return "Tämä on sivu 1, tänne tulee varmaan jotain joskus"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2, tännekin saatta joskus tulla jotain"

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