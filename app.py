from flask import Flask, render_template, request, flash, redirect, session, abort
from flaskext.mysql import MySQL
import os

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'allini'
app.config['MYSQL_DATABASE_PASSWORD'] = 'icilaWb0!'
app.config['MYSQL_DATABASE_DB'] = 'qhacks'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def home(username="", qid=1):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = username

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT question FROM questions WHERE id=" + str(qid[0]))
        question = str(cursor.fetchone()[0])
        
        return render_template('index.html', name=name, question=question)

@app.route('/showquotes')
def showQuotes():
    return render_template('quotes.html')

@app.route('/showgsettings')
def showsettings():
    return render_template('general.html')

@app.route('/showqsettings')
def showqsettings():
    return render_template('question.html')

@app.route('/showhelp')
def showhelp():
    return render_template('help.html')

#@app.route("/getuser")
#def loogedIn():
#    _name = request.args.get('name')
#    conn = mysql.connect()
#    cursor = conn.cursor()
#
#    cursor.execute("SELECT name FROM users WHERE name='" + _name + "'")
#    name = cursor.fetchone()
#
#    cursor.execute("SELECT question FROM users WHERE name='" + _name + "'")
#    question = cursor.fetchone()
#    
#    return render_template('index.html', name=name, question=question)

@app.route("/getquestion", methods=['POST'])
def dispay_question():
    category = request.form['category']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT question FROM questions WHERE category='" + category + "'")
    data = cursor.fetchall()

    return render_template('showquestions.html', question=data)

@app.route("/save", methods=['POST'])
def save_settings():
    _userQ = request.form['q']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (question) VALUES (" + _userQ + ")")
    data = cursor.fetchall()

    if len(data) is 0:
        return "Error"
    else:
        return "Success"
           
@app.route("/signup", methods=['POST'])
def signUp():
    _name = request.form['name']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name) VALUES ('" + _name + "')");
    data = cursor.fetchone()

    if len(data) is 0:
        return "Error"
    else:
        return "Success"
                               
@app.route('/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    qid = 1
    if request.form['password'] == 'password' and request.form['username'] == 'qhacks':
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT question FROM users WHERE name='" + username + "'")
        result = cursor.fetchone()

        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home(username, result)


 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
