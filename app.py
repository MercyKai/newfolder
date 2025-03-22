from flask import Flask,render_template,request,session,redirect,url_for,Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
from camera import Video

app=Flask(__name__)

app.secret_key='default_key'


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='continue'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/therapists')
def therapists():
    return render_template('therapists.html')

@app.route('/login',methods=['GET','POST'])
def login():
    #store the messages for errors
    msg=''
    #check if the request method is POST
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        #create a cursor
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s',(email,password))
        account=cursor.fetchone()
        #check if account exists
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['email']=account['email']
            session['usertype']=account['usertype']
            #redirect to the correct dashboard
            if account['usertype']=='user':
                return redirect(url_for('user_dashboard'))
            elif account['usertype']=='therapist':
                return redirect(url_for('therapist_dashboard'))
        else:
            #if account does not exist, show an error message
            msg='Invalid email or password!'
    return render_template('login.html',msg=msg)

#register route
@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST':
        #get the form data
        usertype =request.form['usertype']
        fName=request.form['fName']
        lName=request.form['lName']
        email=request.form['email']
        password=request.form['password']
        cursor =mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email=%s',(email,))
        #check if the email already exists
        account=cursor.fetchone()
        if account:
            #display an error message, if the email already exists
            msg='Email already exists!'
        else:
            cursor.execute('INSERT INTO users (usertype,fName,lName,email,password) VALUES (%s,%s,%s,%s,%s)',(usertype,fName,lName,email,password))
            #commit the data to the database
            mysql.connection.commit()
            #send to the login page, if successful
            msg='You have successfully registered!'
            return redirect(url_for('login',msg=msg))
    return render_template('register.html',msg=msg)

#user dashboard route
@app.route('/user_dashboard')
def user_dashboard():
    if 'loggedin' in session and session['usertype'] == 'user':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # collect therapists from the database and display
        cursor.execute("SELECT fName,lName,email FROM users WHERE usertype='therapist'")
        therapists =cursor.fetchall()
        return render_template('user_dashboard.html', email=session['email'],therapists=therapists)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/main')
def main():
    return render_template('main.html')

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/therapist_dashboard')
def therapist_dashboard():
    if 'loggedin' in session and session['usertype']=='therapist':
        return render_template('therapist_dashboard.html',email=session['email'])
    return redirect(url_for('login'))

# logout user when they press logout
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('email',None)
    session.pop('usertype',None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)