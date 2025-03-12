from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tervetuloa kirjainlaatikkoon, tämä on elokuvien arvostelupalvelu"
