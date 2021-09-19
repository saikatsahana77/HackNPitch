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
    c_image  = db.Column(db.LargeBinary)
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


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


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
        return redirect(url_for('dashboard'))
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

    upload = Transactions(b_name= bname, seller = seller, buyer = buyer, bought=bought, pages = pages, age = age, subject = subject, stream = stream, weight = weight, price = price, desc = desc, tags= tags, c_image = c_image.read())

    db.session.add(upload)
    db.session.commit()
    return redirect("/upload/{}".format(seller))
    

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


if __name__ == '__main__':
    app.run(debug=True)