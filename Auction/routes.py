from operator import itemgetter
from flask import redirect , url_for, render_template, request, session, flash
from Auction import app, db
from Auction.sql_auction import User, Item
import os
import random
from Auction.sql_auction import datetime, timedelta

'''
COMMENTING STYLE:
Unless a single line comment is used it wiill be split into 
- Proccessing
- Inputs
- Returns
'''

'''
unused as i opted for the sql default _id primary key setting
this autoincrements rows when inputed 
def new_id():
    id_check = True
    while id_check:
        id = str(random.randint(1,9))
        for i in range(0,3):
            id += str(random.randint(1,9))
        id = int(id)
        id_check = User.query.filter_by(usr_id=id).first()

    return id
'''

# so image names dont clash this fucntion adds random int to the end
def unique_img_name(img_name_new):
    if Item.query.filter_by(img_name = img_name_new).first():
        img_check = True
        while img_check:
            rnum = str(random.randint(1,9))
            img_name_new += rnum
            img_check = Item.query.filter_by(img_name=img_name_new)
        
        return img_name_new

    else:
        return img_name_new 

# checks if items have passed their end date and then sets the sold attribute to True
def sold_time_out():
    for item in Item.query.all():
        if item.end_date<datetime.utcnow():
            item.sold = True
            db.session.commit()



'''
Home Function:
- checks if a user is logged in (In the session)
- Takes item_id to be passed to item function
- Returns index.html
'''
@app.route("/", methods = ["POST", "GET"])
def home():
    sold_time_out()
    if session:
        info = True
    else:
        info = False

    if request.method == "POST":
        current_item = (request.form['id'])
        session['current_item_id'] = current_item
        return redirect(url_for('item'))
    
    return render_template("index.html", values=Item.query.all(), info_check = info)


'''
Item Function
- querys a row in Item and User tables based on what was saved in the session
- Takes a new bid and inputs into the Item table
- Returns item.html
'''
@app.route('/item', methods = ["POST", "GET"])
def item():
    item = Item.query.filter_by(item_id = session['current_item_id']).first()
    user = User.query.filter_by(username = session['user']).first()

    if request.method == "POST":
        bid = int(request.form['new_bid'])
        if bid > item.current_bid:
            item.current_bid = bid
            db.session.commit()
        else:
            flash("Bid can't be lower than the current bid!")


    return render_template("item.html", item_data = item, user_data = user)

'''
Was used to check users were being correctly stored in table
now redundant
@app.route("/view")
def view():
    return render_template("view.html", values=User.query.all())
'''


'''
Register function:
- Validates inputs, and enters new fields into User table
- Takes username, password, email and phone 
- Returns register.html
'''

@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        log = request.form
        rname = log["Username"]
        password = log["Password"]
        email = log["Email"]
        phone = log["Phone"]

        found_user = User.query.filter_by(username=rname).first()

        if  not rname or not password or not email or not phone:
            flash("Please fill out all fields")
        elif found_user:
            flash("User already exists")
        else:
            new_user = User(rname, email, password, phone )
            db.session.add(new_user)
            db.session.commit()
            flash("New user registered successfully")
            flash("Go to /login to login to your new account")

    return render_template("register.html")


'''
Login function
- checks if input is in User table, and adds user to the session
- Takes username and password
- Returns login.html
'''
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["Username"]
        passw = request.form["Password"]

        found_users = User.query.filter_by(username=user).first()
        if found_users:
            if found_users.password == passw:
                flash(f"{user}, You have logged in successfully.")
                session["user"] = user



            else:
                flash("Incorrect password")
                return redirect(url_for("login"))
        else: 
            flash("User not found")

        return redirect(url_for("user"))

        
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("home"))
        

    return render_template("login.html")

'''
Login Function:
- Removes user from session
- Redirects to the login page
'''

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.clear()
        flash(f"{user}, you have logged out successfully", "info")
    return redirect(url_for("login"))


'''
User function:
- checks for a button click on user page
    - sold button alters field in Item table to True 
    - id (more details) adds id to session and redirects to item page for more details about that item
- Returns user.html
'''

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        user_data = User.query.filter_by(username=user).first()
        user_items = Item.query.filter_by(username=user).all()

        if request.method == "POST":
            if 'id' in request.form:
                current_item = (request.form['id'])
                session['current_item_id'] = current_item
                return redirect(url_for('item'))
            elif 'sold' in request.form:
                current_item = Item.query.filter_by(item_id=request.form['sold']).first()
                current_item.sold = True
                db.session.commit()
                flash("Item sold!")
                return redirect(url_for('user'))


            
        return render_template("user.html",  user = user_data, values = user_items)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

'''
redundant function
was used to get image uploading working 
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["img"]
            print(image.filename)

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            flash("Image saved")
            redirect(request.url)
    return render_template("upload.html")
'''

'''
Sell Function:
- checks if user is in session, 
validates inputs are not NULL,
makes sure image name is unique and saves image it image folder 
adds item name desc and image name to Item table
- Takes item name, description and image
- Returns sell.html
'''

@app.route("/sell" , methods=["POST", "GET"])
def sell():
    if not session:
        flash("Please login")
        return redirect(url_for("login"))

    elif request.method == "POST":
        if request.form['item_name'] != '' and request.form['item_desc'] != '':
            name = request.form['item_name']
            desc = request.form['item_desc']
            if request.files:
                img = request.files['item_img']
                item_user = session["user"]
                img_name = img.filename
                img_name = unique_img_name(img_name)
                img.save(os.path.join(app.config["IMAGE_UPLOADS"], img_name))


                item_data = Item(name, img_name, desc, item_user)


                db.session.add(item_data)
                db.session.commit()

                flash("Item saved successfully")
                return redirect(url_for("sell"))
        else:
            flash("please enter all fields")

    return render_template("sell.html")
