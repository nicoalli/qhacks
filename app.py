from flask import Flask, render_template, request, flash redirect, session, abort
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'allini'
app.config['MYSQL_DATABASE_PASSWORD'] = 'icilaWb0!'
app.config['MYSQL_DATABASE_DB'] = 'qhacks'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('signup.html')

@app.route("/index")
def loogedIn():
    _name = request.args.get('name')
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE name='" + _name + "'")
    name = cursor.fetchone()

    cursor.execute("SELECT question FROM users WHERE name='" + _name + "'")
    question = cursor.fetchone()
    
    return render_template('index.html', name=name, question=question)

@app.route("/question", methods=['POST'])
def dispay_question():
    _category = request.form['category']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT question FROM questions WHERE category='" + _category + "'")
    data = cursor.fetchall()

    return render_template('question.html', question=data)

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
    
    
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')
                               
@app.route('/login', methods=['POST'])
def do_admin_login():          
    if request.form['password'] == 'password' and request.form['username'] == 'qhacks':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
