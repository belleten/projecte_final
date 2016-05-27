from flask import Flask, redirect, url_for, request
from flask import render_template
import sqlite3
import ORM

app = Flask(__name__)

@app.route('/')
def index():
#    ORM.query_DB.create_user()
    return render_template('index.html')

@app.route('/gestion_users')
def gestion_users():
    return render_template('gestion_users.html')

@app.route('create_user')
def create_user():
    ORM.query_DB.create_user()
    return render_template('create_user.html')

@app.route('delete_user')
def delete_user():
    ORM.query_DB.delete_user()
    return render_template('delete_user.html')

@app.route('update_user')
def update_user():
    ORM.query_DB.update_user()
    return render_template('update_user.html')

@app.route('/gestion_kegs')
def gestion_kegs():
    return render_template('gestion_kegs.html')

@app.route('create_keg')
def create_keg():
    ORM.query_DB.create_keg()
    return render_template('create_keg.html')

@app.route('delete_keg')
def delete_keg():
    ORM.query_DB.delete_keg()
    return render_template('delete_keg.html')

@app.route('update_keg')
def update_keg():
    ORM.query_DB.update_keg()
    return render_template('update_keg.html')

if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0')
