#! /usr/bin/python
#coding:utf-8
from flask import Flask, render_template, json, request,redirect,session,url_for
from flask.ext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


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
        return render_template('logined_index.html', user_name=session['username'])
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

@app.route('/contact')
def contactPage():
    return render_template('contact.html')


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
            cursor.execute("SET NAMES 'utf8';")
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
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

            cursor.execute("SET NAMES 'utf8';")
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
    conn = mysql.connect()
    cursor = conn.cursor()
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
    finally:
        cursor.close()
        conn.close()



@app.route('/getAllWish')
def getAllWish():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
            cursor.callproc('sp_Getallwish',(1,))
            wishes = cursor.fetchall()

            haves_dict = []
            for wish in wishes:
                have_dict = {
                    'name': wish[0],
                    'num': wish[1]}
                haves_dict.append(have_dict)
            return json.dumps(haves_dict)
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getAllHave')
def getAllHave():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
            cursor.callproc('sp_Getallhave',(1,))
            wishes = cursor.fetchall()

            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                    'name': wish[0],
                    'num': wish[1]}
                wishes_dict.append(wish_dict)
            return json.dumps(wishes_dict)
    except Exception as e:
        return render_template('error.html', error=str(e))

    finally:
        cursor.close()
        conn.close()




@app.route('/getHave')
def getHave():
    con = mysql.connect()
    cursor = con.cursor()
    try:
        if session.get('user'):
            _user = session.get('user')

            cursor.callproc('sp_GetHaveByUser', (_user,))
            ring_have = cursor.fetchall()
            print ring_have
            print len(ring_have)
            print len(ring_have[0])
            if len(ring_have[0])>5:
                have_dict={
                    'ihavenum':ring_have[0][4],
                    'ihavedes':ring_have[0][5]
                }
            else:
                have_dict={
                    'ihavenum': ring_have[0][4],
                    'ihavedes': 'no description'
                }
            print have_dict

            return json.dumps(have_dict)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))



@app.route('/getWishById', methods=['POST'])
def getWishById():
    try:
        if session.get('user'):

            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById', (_id, _user))
            result = cursor.fetchall()

            wish = []
            wish.append({'Id': result[0][0], 'Title': result[0][1], 'Description': result[0][2]})

            return json.dumps(wish)
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error=str(e))





@app.route('/updateWish', methods=['POST'])
def updateWish():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _wish_id = request.form['id']


            cursor.callproc('sp_updateWish', (_title, _description, _wish_id, _user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'ERROR'})
    except Exception as e:
        return render_template('error.html',error=str(e))#json.dumps({'status': e})
    finally:
        cursor.close()
        conn.close()



@app.route('/updateHave', methods=['POST'])
def updateHave():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            #_wish_id = request.form['id']


            cursor.callproc('sp_updateHave', (_title, _description, _user))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'ERROR'})
    except Exception as e:
        return render_template('error.html',error=str(e))#json.dumps({'status': e})
    finally:
        cursor.close()
        conn.close()



@app.route('/deleteWish', methods=['POST'])
def deleteWish():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')

            cursor.callproc('sp_deleteWish', (_id, _user))
            result = cursor.fetchall()

            if len(result) is 0:
                conn.commit()
                return json.dumps({'status': 'OK'})
            else:
                return json.dumps({'status': 'An Error occured'})
        else:
            return render_template('error.html', error='Unauthorized Access')
    except Exception as e:
        return json.dumps({'status': str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(port=5002)
