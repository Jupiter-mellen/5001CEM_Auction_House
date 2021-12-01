from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os



# Setting flask configs like the path for images to be uploaded  

app = Flask(__name__)

app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Sets directory for images no matter where the folder origin is
path = os.path.dirname(os.path.abspath(__file__))
app.config["IMAGE_UPLOADS"] = os.path.dirname(os.path.join(path+"\\static\\images\\"))
db = SQLAlchemy(app)
#imports after main imports so everything initialises correctly
from Auction import routes



