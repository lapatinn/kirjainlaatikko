from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"

@app.route("/numbers")
def numbers():
    content = ""
    for i in range(1,101):
        content += str(i) + " "
    return content

if __name__ == "__main__":
    app.run(debug=False)