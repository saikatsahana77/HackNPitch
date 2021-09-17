import sqlite3
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

username = ""


@app.route('/')
def index():
    global username
    username = ""
    try:
        return render_template('index.html', data=request.args.get('v'))
    except:
        return render_template('index.html', data="d")


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
def method_name():
    print("running123")
    return "running"

if __name__ == '__main__':
    app.run(debug=True)