from flask import Flask, render_template, request, redirect, session
import mysql.connector
from sentiments import second
import os


app = Flask(__name__)

#cookie
app.secret_key = os.urandom(24)

#calls second file
app.register_blueprint(second)

#connecting to mysql database
try:
    con = mysql.connector.connect(host='localhost',user='root',
                                  password='',database='SentimentAnalysisUser')
    curs = con.cursor()
except:
    print('Error')

#call login template
@app.route('/')
def login():
    return render_template('login.html')

#call register template
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    curs.execute(
        """SELECT * from `Users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = curs.fetchall()
    # check if a user has already logged in
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
    # get user login data and pass the data to database
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    curs.execute("""INSERT INTO `users` (`username`,`email`,`password`) VALUES ('{}','{}','{}')""".format(
        name, email, password))
    con.commit()
    curs.execute(
        """SELECT * from `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = curs.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    # close the session
    session.pop('user_id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)