from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from datetime import datetime
from send_email import send_email

app = Flask(__name__)
app.config["SECRET_KEY"] = dotenv_values().get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 456
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = dotenv_values().get("GMAIL_USER")
app.config["MAIL_PASSWORD"] = dotenv_values().get("GMAIL_PASS")

db = SQLAlchemy(app)


class Form(db.Model):
    """
    Structures the table that will hold the applicant information in the database
    """
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
    Renders the application web page. If user has sent information via post
    request, their information is stored in a database.
    :return: A call to render the web page
    """
    if request.method == "POST":
        # Get user data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"].strip()
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        employment_status = request.form["employment_status"]

        # Add user data to database
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    employment_status=employment_status)
        db.session.add(form)
        db.session.commit()

        # Send confirmation email
        message_body = f"Thank you for your application, {first_name}!"
        send_email(email, message_body)
        flash("Application sent successfully", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
