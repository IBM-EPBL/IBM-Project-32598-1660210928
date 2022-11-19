from flask import*
from datetime import date
import ibm_db
import re
import requests


app=Flask(__name__)

app.secret_key = 'abc'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nbc49111;PWD=NfHOkug6Kyn7Fgjj",'','')

@app.route('/')
def homer():
    return render_template('login.html')

@app.route('/backlogin')
def backlogin():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html') 

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('login.html')

     

@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''

    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM login WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            url = "https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=7e1737d3191d4fe894fc579df01b7bde"
            r= requests.get(url).json()
            case = {
                'articles': r['articles']
            }
            return render_template('index.html', cases = case)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        phone_num = request.form['phone_num']
        password = request.form['confirm_password']
        sql = "SELECT * FROM login WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
            return render_template('login.html', msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        elif not re.match(r'[0-9]+', phone_num):
            msg = 'phone number must contain only numbers !'
        else:
            insert_sql = "INSERT INTO user_details VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phone_num)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)

            insert_sql_1 = "INSERT INTO login VALUES (?, ?)"
            prep_stmt_1 = ibm_db.prepare(conn, insert_sql_1)
            ibm_db.bind_param(prep_stmt_1, 1, username)
            ibm_db.bind_param(prep_stmt_1, 2, password)
            ibm_db.execute(prep_stmt_1)
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return render_template('register.html', msg = msg)
    return render_template('register.html', msg = msg)  




@app.route('/index')
def index():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('index.html',cases = case)    

@app.route('/sports')
def sports():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('sports.html',cases = case)

@app.route('/business')
def business():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('business.html',cases = case)

@app.route('/technology')
def technology():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('technology.html',cases = case)

@app.route('/science')
def science():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('science.html',cases = case)

@app.route('/health')
def health():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('health.html',cases = case)

@app.route('/entertainment')
def entertainment():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('entertainment.html',cases = case)    

@app.route('/search', methods =['GET', 'POST'])
def search():
    s = request.form['search']
    today = date.today()
    dat = today.strftime("%Y/%m/%d")
    url ="https://newsapi.org/v2/everything?q="+s+"&from="+ dat+"&sortBy=popularity&apiKey=660a62eb9a6445a7b887ad991e40f4cb"
    r= requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('search.html',cases = case)       


if __name__=='__main__':
    app.run()
