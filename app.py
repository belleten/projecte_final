from flask import Flask, redirect, url_for, request
from flask import render_template
import sqlite3
import ORM

app = Flask(__name__)

#------------------INDEX WEB PAGES----------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/App')
def App():
    return render_template('app.html')

@app.route('/App/gestion_users')
def gestion_users():
    return render_template('gestion_users.html')

@app.route('/App/gestion_kegs')
def gestion_kegs():
    return render_template('gestion_kegs.html')

#------------------CRUD WEBAPP USERS----------------------------------

@app.route('/App/create_user',methods=['POST','GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        real_name= request.form.get('real_name')
        email= request.form.get('email')
        user_id="1"
        ORM.query_DB.create_user(username,user_id,real_name, email)
	return render_template('succes.html')

@app.route('/App/read_users')
def read_users():
    users = ORM.query_DB.get_all_users()
    return render_template('read_users.html',users=users)

@app.route('/App/delete_user',methods=['POST','GET'])
def delete_user():
    if request.method == 'GET':
        return render_template('delete_user.html')
    elif request.method == 'POST':
        user_id= request.form.get('user_id')
        ORM.query_DB.delete_user(user_id)
	return render_template('succes.html')

@app.route('/App/update_user',methods=['POST','GET'])
def update_user():
    if request.method == 'GET':
        return render_template('update_user.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        real_name= request.form.get('real_name')
        email= request.form.get('email')
        amount= request.form.get('amount')
        user_id= request.form.get('user_id')
        ORM.query_DB.update_user(username,user_id,real_name,email,amount)
	return render_template('succes.html')

#------------------CRUD WEBAPP KEGS----------------------------------

@app.route('/App/create_keg',methods=['POST','GET'])
def create_keg():
    if request.method == 'GET':
        return render_template('create_keg.html')
    elif request.method == 'POST':
        keg_id=request.form.get('keg_id')
        amount=request.form.get('amount')
        ORM.query_DB.create_keg(keg_id,amount)
	return render_template('succes.html')

@app.route('/App/delete_keg',methods=['POST','GET'])
def delete_keg():
    if request.method == 'GET':
        return render_template('delete_keg.html')
    elif request.method == 'POST':
        keg_id=request.form.get('keg_id')
        ORM.query_DB.delete_keg(keg_id)
	return render_template('succes.html')

@app.route('/App/update_keg',methods=['POST','GET'])
def update_keg():
    if request.method == 'GET':
        return render_template('update_keg.html')
    elif request.method == 'POST':
        keg_id= request.form.get('keg_id')
        amount= request.form.get('amount')
        ORM.query_DB.update_keg(keg_id,amount)
	return render_template('succes.html')

@app.route('/App/read_kegs')
def read_kegs():
    kegs = ORM.query_DB.get_all_kegs()
    return render_template('read_kegs.html',kegs=kegs)

if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0')
