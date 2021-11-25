from flask import Flask, redirect , url_for, render_template

app = Flask(__name__)
a = False


@app.route("/")
def home():
    return render_template("index.html", content='test' )

app.run(debug=True)