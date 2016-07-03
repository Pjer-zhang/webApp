#! /usr/bin/python
from flask import Flask, render_template, json, request,redirect,session,url_for
from flask.ext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from codecs import  *


mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'something_else'
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '19940718'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET'] =  'utf8'
mysql.init_app(app)


@app.route('/')
def main():
    if session.get('user'):
        return render_template('logined_index.html')
    else:
        return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')


@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return redirect(url_for('userHome',user_name=session['username']))
    else:
        return render_template('signin.html')


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html',user_name=session['username'])
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    con = mysql.connect()
    cursor = con.cursor()
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql


        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if str(data[0][3])==_password:#check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                session['username'] = data[0][1]
                return redirect( url_for( 'userHome',user_name=session['username']))
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL


            _hashed_password = _password# generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name.decode().encode('utf-8'), _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/addWish',methods=['POST'])
def addWish():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        if session.get('user'):
            _num = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')

            cursor.callproc('sp_addWish',(_num,_description,_user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect( url_for('userHome',user_name=session['username']))
            else:
                message = str(data[0])
                return render_template('error.html',error = message[3:-3])

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getWish')
def getWish():
    con = mysql.connect()
    cursor = con.cursor()
    try:
        if session.get('user'):
            _user = session.get('user')

            cursor.callproc('sp_GetWishByUser', (_user,))
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                    'Id': wish[0],
                    'Title': wish[1],
                    'Description': wish[2],
                    'Date': wish[4]}
                wishes_dict.append(wish_dict)

            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))



if __name__ == "__main__":
    app.run(port=5002)
