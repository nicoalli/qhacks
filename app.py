from flask import Flask, render_template, request
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
    name = request.args.get('name')
    qid = request.args.get('qid')
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE name='" + name + "';")
    uname = cursor.fetchone()

    cursor.execute("SELECT question FROM questions WHERE id=" + qid)
    question = cursor.fetchone()
    
    return render_template('index.html', name=uname, question=question)

@app.route("/question", methods=['POST'])
def dispay_question():
    category = request.form['category']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT question FROM questions WHERE category='" + category + "'")
    data = cursor.fetchall()

    return render_template('question.html', question=data)

@app.route("/save", methods=['POST'])
def save_settings():
    userQ = request.form['q']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (question) VALUES (" + userQ + ")")
    data = cursor.fetchall()

    if len(data) is 0:
        return "Error"
    else:
        return "Success"
           
@app.route("/signup", methods=['POST'])
def signUp():
    uname = request.form['name']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name) VALUES ('" + uname + "')");
    data = cursor.fetchone()

    if data is None:
        return "Error"
    else:
        return "Success"


 
if __name__ == "__main__":
    app.run()
