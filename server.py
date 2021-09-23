# Importing modules
import smtplib
import random
import math
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import cv2
import numpy as np
from PIL import Image
from instamojo_wrapper import Instamojo

# Setting the API keys for payment gateway
API_KEY = "test_e486fd7dc9a74a4bd030e7e5e0a"

AUTH_TOKEN = "test_c176b5eb749d5d0fe752042e405"

# Initialising the payement gateway API
api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')

# Creating and configuring a flask app
cwd = "sqlite:///"+os.getcwd()+r"\bookify.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cwd

# Creating a sqlalchemy object and attaching it to a model
db = SQLAlchemy(app)
class Transactions(db.Model):
    b_name = db.Column(db.String)
    seller = db.Column(db.String)
    buyer = db.Column(db.String, nullable=True)
    bought = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    age = db.Column(db.String)
    subject = db.Column(db.String)
    stream = db.Column(db.String)
    weight = db.Column(db.Float)
    price = db.Column(db.Float)
    desc = db.Column(db.String, nullable=True)
    tags = db.Column(db.String)
    c_image  = db.Column(db.String)
    id  = db.Column(db.Integer, primary_key=True)

# Function to convert a file into binary
def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()
    return binary

# Function to read a file storage object
def readImage(img_name):
    with open(img_name, 'rb') as file:
        img = file.stream.read()
        return img

# Function to send otp
def otp_send(email, porpouse):
    sender_email = "bookify.suuport@gmail.com"
    receiver_email = email
    password = "bookify12#"
    message = MIMEMultipart()
    message["Subject"] = "OTP For {}".format(porpouse)
    message["From"] = sender_email
    message["To"] = receiver_email
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    text = "Your OTP for {} is {}".format(porpouse, otp)
    content = MIMEText(text, "plain")
    message.attach(content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    return otp


username = ""

# Setting the home route
@app.route('/')
def index():
    global username
    username = ""
    try:
        return render_template('index.html', data=request.args.get('v'))
    except:
        return render_template('index.html', data="e")

# Setting the dashboard route
@app.route('/dashboard/<email>')
def dashboard(email):
    email=str(email)

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, bought, seller, pages, age, subject, stream, weight, price, desc, tags, c_image, buyer, id from transactions order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    print(rows)

    # Changing the tuples to lists
    for i in range(len(rows)):
        rows[i] = list(rows[i])

    # Removing rows of items that have either been bought or added to cart
    for idx,i in enumerate(rows.copy()):
        print(i[1])
        print(i[12])
        print(i)
        if (i[1] == 1):
            rows.remove(i)
        else:
            if (i[12]!= None):
                rows.remove(i)
            else:
                pass
    return render_template("dashboard.html", rows= rows)

# Insrting a new user to the database
@app.route('/signup_check', methods=['POST'])
def signup_check():
    uname = request.form['uname']
    pswd = request.form['pass']
    email = request.form['email']
    phone = request.form['phone']
    phone = int(phone)

    # Connecting to the database
    conn = sqlite3.connect("bookify.db")
    q1 = "select email from users where email = '{em}'".format(
        un=uname, ps=pswd, em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    
    # Checking for duplicate emails as we cannot allow it because email is set as primary key in the users table
    if (len(rows) == 1):
        return redirect(url_for('index', v="b"))

    # Insrting a new row i.e. a new user to a database
    conn = sqlite3.connect("bookify.db")
    q1 = "insert into users (username, email, phone, password) values('{un}','{em}','{ph}','{ps}')".format(un=uname, em=email, ph=phone,  ps=pswd)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect(url_for('index', v="a"))

# Checking a new user's login credentials
@app.route('/login_check', methods=['POST'])
def login_check():
    global username
    email = request.form['email']
    pswd = request.form['pass']

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select username, password, email, p_updated from users where email = '{em}' and password = '{ps}'".format(
        em=email, ps=pswd)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    conn.close()

    # Redirecting to profile page or dashboard page based on if the user has completed filling his/her profile 
    if (len(rows) == 1):
        print(rows[0][3])
        if (rows[0][3]==0):
            return redirect('profile/{}'.format(email))
        else:
            return redirect('dashboard/{}'.format(email))
    else:
        return redirect(url_for('index', v="c"))

# Sending otp for password reset
@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = otp_send(email,"password reset")
    return otp

# Resetting password of an existing user
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email_final']
    pswd = request.form['new_pass']
    conn = sqlite3.connect("bookify.db")
    q1 = "update users set password ='{ps}' where email='{em}'".format(em=email, ps=pswd)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect(url_for('index', v="d"))

# Route for the profile page
@app.route('/profile/<email>')
def profile(email):
    email=str(email)

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select * from users where email = '{em}'".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    rows[0] = list(rows[0])

    # Setting values to be blank if any null value exists
    for i in range(0,len(rows[0])):
        if (rows[0][i] == None):
            rows[0][i] = ""
    print(rows)
    return render_template("profile.html",rows=rows)

# Route for the upload page
@app.route('/upload/<email>')
def upload(email):
    email=str(email)

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select username, email from users where email = '{em}'".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    rows[0] = list(rows[0])

    # Setting values to be blank if any null value exists
    for i in range(0,len(rows[0])):
        if (rows[0][i] == None):
            rows[0][i] = ""
    print(rows)
    return render_template("upload.html",rows=rows)

# Post route for adding a new book
@app.route('/add_book', methods=['POST'])
def add_book():
    bname = request.form['name_book']
    seller= request.form['email']
    buyer = None
    bought = 0
    pages = request.form['pages_book']
    age = request.form['condition_book']
    subject = request.form['sub_book']
    stream = request.form['stream_book']
    weight = float(request.form['weight_book'])
    price = float(request.form['price_book'])
    desc = request.form['desc_book']
    tags = request.form['tags_book']
    c_image = request.files['pic_book']

    # Creating a random filename with the extension of the file entered by the user and saving the file at that location
    _, file_extension = os.path.splitext(c_image.filename)
    filename_1 = str(random.randint(1, 1000000000))
    filename = filename_1 + file_extension
    filepath = os.path.join("./static/uploads/", filename)
    print(filepath,filename,filename_1,file_extension)
    c_image = Image.open(c_image)
    c_image = np.array(c_image)
    c_image  = cv2.cvtColor(c_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filepath, c_image)

    # Instantiating an object of the transaction class and pushing a new item to the transaction table
    upload = Transactions(b_name= bname, seller = seller, buyer = buyer, bought=bought, pages = pages, age = age, subject = subject, stream = stream, weight = weight, price = price, desc = desc, tags= tags, c_image = filepath)
    db.session.add(upload)
    db.session.commit()
    return redirect("/products/{}".format(seller))
    
# Post route for updating user details
@app.route('/update_details', methods=['POST'])
def update_details():
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    social = request.form['social']
    upi  = request.form['upi']

    # Connecting to the database and updating the details
    conn = sqlite3.connect("bookify.db")
    q1 = "update users set phone ='{ph}', address='{ad}', social ='{so}', upi='{upi}', p_updated='{pup}' where email='{em}'".format(em=email, ph=phone, ad=address, so=social, upi=upi, pup=1)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect("/profile/{}".format(email))

# Route for the products page
@app.route('/products/<email>')
def method_name(email):
    email=str(email)

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, buyer, bought, pages, age, subject, stream, weight, price, desc, tags, c_image from transactions where seller = '{em}' order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()

    # Changing the tuples to lists
    for i in range(len(rows)):
        rows[i] = list(rows[i])

    # Setting appropriate values for buyer and bought columns
    for i in range(len(rows)):
        if (rows[i][1] == None):
            rows[i][1] = "N/A"
        else:
            pass
        if (rows[i][2] == 0):
            rows[i][2] = "unsold"
        elif (rows[i][2] == 1):
            rows[i][2] = "sold"
    return render_template("my_products.html", rows=rows)

# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# Post route for adding an object to cart - setting buyer to the logged in account 
@app.route('/add_cart/<id>', methods=['POST'])
def add_cart(id):
    email = request.form['email_send_cont']
    conn = sqlite3.connect("bookify.db")
    q1 = "update transactions set buyer ='{em}' where id='{id}'".format(em=email, id=id)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect("/cart/{}".format(email))

# Route for the cart page
@app.route('/cart/<email>')
def cart(email):
    email=str(email)

    # Connecting to the database
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, bought, seller, pages, age, subject, stream, weight, price, desc, tags, c_image, buyer, id from transactions where buyer = '{em}' order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    q2 = "select phone from users where email = '{em}'".format(em=email)
    rows_1 = conn.execute(q2)
    rows_1 = rows_1.fetchall()

    # Setting tuples to lists
    for i in range(len(rows)):
        rows[i] = list(rows[i])
    print(rows)

    # Removing rows with bought equal to 1
    for i in rows.copy():
        if (i[1] == 1):
            rows.remove(i)
        else:
            pass
    sum = 0.0
    ids = ""
    for i in rows:
        sum += i[8]
        ids += " "+str(i[13])
    print(ids)
    return render_template("cart.html", rows= rows, rows_1 = rows_1, sum=sum, ids=ids)

# Post route for removing a book from the cart - setting buyer to null
@app.route('/remove_book/<id>' , methods=['POST'])
def remove_book(id):
    email = request.form['email_send_cont']
    conn = sqlite3.connect("bookify.db")
    q1 = "update transactions set buyer ={em} where id='{id}'".format(em="NULL", id=id)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect("/dashboard/{}".format(email))

# Post route for buying a book - payment gateway integration 
@app.route('/buy_book/<id>', methods=['POST'])
def buy_book(id):
    email = request.form['email_send_cont']
    price = request.form['price_send_cont']

    # Creating an order to the payment gateway
    response = api.payment_request_create(
        amount=price,
        purpose="Book Buy",
        buyer_name=email,
        send_email=True,
        email=email,
        redirect_url="http://localhost:5000/purchases/{}".format(email)
        )

    # Setting bought = 1 for the item
    conn = sqlite3.connect("bookify.db")
    q1 = "update transactions set bought='1' where id='{id}'".format(id=id)
    conn.execute(q1)
    conn.commit()
    conn.close()
    
    return redirect(response['payment_request']['longurl'])

# Post route for buying many books together - payment gateway integration
@app.route('/buy_lot/<ids>', methods=['POST'])
def buy_lot(ids):
    ids = ids.split(" ")
    email = request.form['email_send_cont']
    price = request.form['price_inp']

    # Creating an order to the payment gateway
    response = api.payment_request_create(
        amount=price,
        purpose="Book Buy",
        buyer_name=email,
        send_email=True,
        email=email,
        redirect_url="http://localhost:5000/purchases/{}".format(email)
        )

    # Setting bought = 1 for all the ids we received on the route request
    conn = sqlite3.connect("bookify.db")
    for id in ids:
        q1 = "update transactions set bought='1' where id='{id}'".format(id=id)
        conn.execute(q1)
        conn.commit()
    conn.close()
    
    return redirect(response['payment_request']['longurl'])

# Setting a route for the login error page
@app.route('/login_error')
def login_error():
    return render_template("login_error.html")

# Setting a route for the purchases page
@app.route('/purchases/<email>')
def purchases(email):
    email=str(email)

    # Connecting to database
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, bought, seller, pages, age, subject, stream, weight, price, desc, tags, c_image, buyer, id from transactions where buyer='{em}' order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    print(rows)

    # Changing tuples to lists
    for i in range(len(rows)):
        rows[i] = list(rows[i])

    # Removing items that are unsold i.e. bought = 0 
    for idx,i in enumerate(rows.copy()):
        print(i[1])
        print(i[12])
        print(i)
        if (i[1] == 0):
            rows.remove(i)
        else:
            pass
    return render_template("my_purchases.html", rows=rows, email=email)

# Creating post route for sending otp to validate email
@app.route('/send_otp_check', methods=['POST'])
def send_otp_check():
    email = request.form['email']
    otp = otp_send(email, "email verification")
    return otp

# Main method (starting point of the program)
if __name__ == '__main__':

    # Running the flask app
    app.run(debug=True)
