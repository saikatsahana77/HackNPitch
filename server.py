import smtplib
import random
import math
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from io import BufferedReader
from flask_sqlalchemy import SQLAlchemy
import os
import cv2
import numpy as np
from PIL import Image



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\Users\Asus\Desktop\HackNPitch\bookify.db"
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


def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()
    return binary

def readImage(img_name):
    with open(img_name, 'rb') as file:
        img = file.stream.read()
        return img


def otp_send(email):
    sender_email = "bookify.suuport@gmail.com"
    receiver_email = email
    password = "bookify12#"
    message = MIMEMultipart()
    message["Subject"] = "OTP For password reset"
    message["From"] = sender_email
    message["To"] = receiver_email
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    text = "Your OTP for password reset is {}".format(otp)
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


@app.route('/')
def index():
    global username
    username = ""
    try:
        return render_template('index.html', data=request.args.get('v'))
    except:
        return render_template('index.html', data="e")


@app.route('/dashboard/<email>')
def dashboard(email):
    email=str(email)
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, bought, seller, pages, age, subject, stream, weight, price, desc, tags, c_image from transactions order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    for i in range(len(rows)):
        rows[i] = list(rows[i])
    for i in range(len(rows.copy())):
        if (rows[i][1] == 1):
            rows.remove(rows[i][1])
        else:
            pass
        if (rows[i][4]== 1):
            rows[i][4] = "Less than 1 year"
        elif (rows[i][4]== 2):
            rows[i][4] = "Less than 2 years"
        elif (rows[i][4]== 3):
            rows[i][4] = "Less than 5 years"
        else:
            rows[i][4] = "More than 5 years"
    return render_template("dashboard.html", rows= rows)


# Less than 1 year
# Less than 2 years
# Less than 5 years
# More than 5 years

@app.route('/signup_check', methods=['POST'])
def signup_check():
    uname = request.form['uname']
    pswd = request.form['pass']
    email = request.form['email']
    phone = request.form['phone']
    phone = int(phone)


    conn = sqlite3.connect("bookify.db")
    q1 = "select email from users where email = '{em}'".format(
        un=uname, ps=pswd, em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    if (len(rows) == 1):
        return redirect(url_for('index', v="b"))


    conn = sqlite3.connect("bookify.db")
    q1 = "insert into users (username, email, phone, password) values('{un}','{em}','{ph}','{ps}')".format(un=uname, em=email, ph=phone,  ps=pswd)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect(url_for('index', v="a"))


@app.route('/login_check', methods=['POST'])
def login_check():
    global username
    email = request.form['email']
    pswd = request.form['pass']
    conn = sqlite3.connect("bookify.db")
    q1 = "select username, password, email from users where email = '{em}' and password = '{ps}'".format(
        em=email, ps=pswd)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    conn.close()
    if (len(rows) == 1):
        username = rows[0][0]
        return redirect('dashboard/{}'.format(email))
    else:
        return redirect(url_for('index', v="c"))

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = otp_send(email)
    return otp

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

@app.route('/profile/<email>')
def profile(email):
    email=str(email)
    conn = sqlite3.connect("bookify.db")
    q1 = "select * from users where email = '{em}'".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    rows[0] = list(rows[0])
    for i in range(0,len(rows[0])):
        if (rows[0][i] == None):
            rows[0][i] = ""
    print(rows)
    return render_template("profile.html",rows=rows)

@app.route('/upload/<email>')
def upload(email):
    email=str(email)
    conn = sqlite3.connect("bookify.db")
    q1 = "select username, email from users where email = '{em}'".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    rows[0] = list(rows[0])
    for i in range(0,len(rows[0])):
        if (rows[0][i] == None):
            rows[0][i] = ""
    print(rows)
    return render_template("upload.html",rows=rows)

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
    _, file_extension = os.path.splitext(c_image.filename)
    filename_1 = str(random.randint(1, 1000000000))
    filename = filename_1 + file_extension
    filepath = os.path.join("./static/uploads/", filename)
    print(filepath,filename,filename_1,file_extension)
    c_image = Image.open(c_image)
    c_image = np.array(c_image)
    c_image  = cv2.cvtColor(c_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filepath, c_image)
    upload = Transactions(b_name= bname, seller = seller, buyer = buyer, bought=bought, pages = pages, age = age, subject = subject, stream = stream, weight = weight, price = price, desc = desc, tags= tags, c_image = filepath)
    db.session.add(upload)
    db.session.commit()
    return redirect("/products/{}".format(seller))
    

@app.route('/update_details', methods=['POST'])
def update_details():
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    social = request.form['social']
    upi  = request.form['upi']
    conn = sqlite3.connect("bookify.db")
    q1 = "update users set phone ='{ph}', address='{ad}', social ='{so}', upi='{upi}' where email='{em}'".format(em=email, ph=phone, ad=address, so=social, upi=upi)
    conn.execute(q1)
    conn.commit()
    conn.close()
    return redirect("/profile/{}".format(email))


@app.route('/products/<email>')
def method_name(email):
    email=str(email)
    conn = sqlite3.connect("bookify.db")
    q1 = "select b_name, buyer, bought, pages, age, subject, stream, weight, price, desc, tags, c_image from transactions where seller = '{em}' order by id desc".format(em=email)
    rows = conn.execute(q1)
    rows = rows.fetchall()
    for i in range(len(rows)):
        rows[i] = list(rows[i])
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

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)