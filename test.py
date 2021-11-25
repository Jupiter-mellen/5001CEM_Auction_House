import re
from flask import Flask, redirect , url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
import os
app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
image_folder = os.path.join('images')
app.config["UPLOAD_FOLDER"] = image_folder   
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/display")
def display():
    return render_template("display.html")

    
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user

        found_users = users.query.filter_by(name=user).first()
        if found_users:
            session["email"] = found_users.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash(f"{user}, You have logged in successfully.")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_users = users.query.filter_by(name=user).first()
            found_users.email = email
            db.session.commit()

            flash("Email saved successfully")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email = email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        print(session)
        session.pop("user", None)
        session.pop("email", None)
        print(session)
        flash(f"{user}, you have logged out successfully", "info")
    return redirect(url_for("login"))

app.config["IMAGE_UPLOADS"] = "C:/Users/peter/Documents/GitHub/New folder/5001CEM_Auction_House/static/images"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["img"]
            print(image.filename)

            file_ext = image.filename.split(".")
            file_ext = file_ext[1]
            filename = session["user"]+"."+file_ext

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            flash("Image saved")
            redirect(request.url)
    return render_template("upload.html")

@app.route("/sell" , methods=["POST", "GET"])
def sell():
    if request.method == "POST":
        name = request.form['item_name']
        desc = request.form['item_desc']
        if request.files['item_img']:
            img = request.files['item_img']
            print(name,desc, img.filename)
        else:
            print(name,desc)

        redirect(request.url)

    return render_template("sell.html")


db.create_all()

if __name__ == "__main__":

    app.run(debug=True)

