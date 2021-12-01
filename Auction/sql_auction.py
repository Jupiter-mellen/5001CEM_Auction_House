from Auction import db
from datetime import datetime, timedelta

'''
User Table
takes:
Username , Password , Email , Phone Number
'''
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)

    def __init__(self, name, email, password, phone):
        self.username = name
        self.password = password
        self.email = email
        self.phone = phone

'''
User Table
takes:
Item Name , Image Name , Item Description , Start Date , End Date , Username(Forign key from User Table) , Current Bid , Sold 
'''
class Item(db.Model):
    item_id = db.Column(db.Integer,  primary_key= True, nullable=False)
    name = db.Column(db.String(50))
    img_name = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    start_date = db.Column(db.DateTime, default = datetime.utcnow())
    end_date = db.Column(db.DateTime, default = datetime.utcnow()+timedelta(hours = 12))
    username = db.Column(db.String, db.ForeignKey("user.username"))
    current_bid = db.Column(db.Integer, default = 0)
    sold = db.Column(db.Boolean, default = False)

    def __init__(self, name, img_name, desc, username):
        self.name = name
        self.img_name = img_name
        self.desc = desc
        self.username = username

db.create_all()
