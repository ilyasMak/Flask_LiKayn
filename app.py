from flask import Flask , render_template , request , redirect , url_for  , session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, UserMixin

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "likayn"
mysql = MySQL(app)
app.secret_key = '0000'  




@app.route('/')
def base():
        return render_template('base.html')

@app.route('/sign',methods=['GET','POST'])
def Sign():  
        return render_template('sign.html' )

@app.route('/signUp',methods=['POST'])
def SignUp():
        if request.method == 'POST' :
              firstName = request.form['fn']
              lastName = request.form['ln']
              username = request.form['un']
              password = request.form['p']
              cur = mysql.connection.cursor()
              cur.execute("INSERT INTO users (firstname, lastname, username, password) VALUES (%s, %s, %s, %s)", (firstName, lastName, username, password))
              inserted_id = cur.lastrowid
              mysql.connection.commit()
              cur.close()
              cursor = mysql.connection.cursor()
              cursor.execute("SELECT * FROM message WHERE id = %s", (id,))
              messages = cursor.fetchall()
              cursor.close()
        return redirect(url_for('HT', id=inserted_id, fn=firstName, ln=lastName, msgs=messages))

@app.route('/signIn',methods=['POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()  

        if user:  
            id= user[0]
            firstName = user[1]
            lastName = user[2]
            session['user_id'] = id
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM message WHERE id = %s", (id,))
            messages = cursor.fetchall()
            cursor.close()
           
            return redirect(url_for('HT', id=id, fn=firstName, ln=lastName, msgs=messages))
        else:
        
            return render_template('sign.html' )  
           
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Supprimer l'ID de l'utilisateur de la session
    return redirect(url_for('Sign'))


@app.route('/Profile/<int:id>')
def HT(id):
    if 'user_id' in session and session['user_id'] == id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s ", (id,))
        user = cur.fetchone()  
        firstName = user[1]
        lastName = user[2]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM message WHERE id = %s", (id,))
        messages = cursor.fetchall()
        cursor.close()

        return render_template('Receive.html', id=id,fn=firstName,ln=lastName,msgs = messages)
    else:
        return redirect(url_for('Sign'))  




@app.route('/sendMsg/<int:id>')
def sendMsg(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s ", (id,))

    user = cur.fetchone() 
    if user:
        firstName = user[1]
        lastName = user[2]
        return render_template('sendMsg.html', id=id,fn=firstName,ln=lastName)
    else:
        return redirect(url_for('Sign'))  
    

@app.route('/Send/<int:id>',methods=['POST','GET'])
def Send(id):
     if request.method == 'POST':
        name = request.form['name']
        msg = request.form['Msg']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO message (id, Nom, Message) VALUES (%s, %s, %s)", (id, name, msg))
        mysql.connection.commit()
        cur.close()
     cur2 = mysql.connection.cursor()
     cur2.execute("SELECT * FROM users WHERE id = %s ", (id,))
   
     user = cur2.fetchone() 
     return redirect(url_for('sendMsg', id=id, fn=user[1], ln=user[2]))
@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM message WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('Sign'))
     


if __name__ == '__main__' :
    app.run(debug=True)



