from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Form(db.Model):
    MAX_INPUT_LEN = 80
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(MAX_INPUT_LEN))
    last_name = db.Column(db.String(MAX_INPUT_LEN))
    email = db.Column(db.String(MAX_INPUT_LEN))
    date = db.Column(db.Date)
    employment_status = db.Column(db.String(MAX_INPUT_LEN))


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Stores data entered by user if sent via post request, otherwise displays
    the web page
    :return: A call to render the web page
    """
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        employment_status = request.form["employment_status"]

        print(f"{first_name} {last_name} {email} {date} {employment_status}")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
