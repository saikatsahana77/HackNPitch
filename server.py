import smtplib
import random
import math
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)



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
    global username
    if (username != ""):
        return render_template("dashboard.html",username=username)
    else:
        return render_template("login_error.html")


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
    print(rows)
    conn.close()
    if (len(rows) == 1):
        username = rows[0][0]
        return redirect(url_for('dashboard',username=username))
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
    

if __name__ == '__main__':
    app.run(debug=True)