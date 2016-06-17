from flask import Flask, redirect, url_for, request, make_response, abort, jsonify
from flask import render_template
import sqlite3
import ORM
from ORM import User, Base, Keg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ORM/mydatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

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

@app.route('/WS')
def WS():
    return render_template('ws.html')

#------------------ERROR HANDLER WS----------------------------------

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

#------------------CRUD WS USERS-------------------------------------

@app.route('/WS/user/one/<username>', methods=['GET'])
def get_user_one(username):
    try:
        user_query = session.query(User).filter_by(username=username).one()
        session.commit()
    except:
        abort(404)
    return jsonify(id=user_query.id,
                   username=user_query.username,
                   user_id=user_query.user_id,
                   real_name=user_query.real_name,
                   email=user_query.email,
                   amount=user_query.amount), 201

@app.route('/WS/user/all', methods=['GET'])
def get_user_all():
    users_query = session.query(User).all()
    session.commit()
    users=[user.__json__() for user in users_query]
    if len(users) == 0:
        abort(404)
    return jsonify({'users': users}), 201

@app.route('/WS/user', methods=['POST'])
def create_user_ws():
    if not request.json or not 'username' in request.json or not 'user_id' in request.json or not 'realname' in request.json or not 'email' in request.json or not 'amount' in request.json:
        abort(400)
    if ORM.query_DB.user_exist(request.json['username']):
        abort(400)
    new_user = User(username=request.json['username'],
                    user_id=request.json['user_id'],
                    real_name=request.json['realname'],
                    email=request.json['email'],
                    amount=request.json['amount']) 

    session.add(new_user)
    session.commit()
    return jsonify(id=new_user.id,
                   username=new_user.username,
                   user_id=new_user.user_id,
                   realname=new_user.real_name,
                   email=new_user.email,
                   amount=new_user.amount), 201

@app.route('/WS/user/<username>', methods=['PUT'])
def update_user_ws(username):
    try:
        user_query = session.query(User).filter_by(username=username).one()
        session.commit()
    except:
        abort(404)
    if not request.json:
        abort(400)
    user_query.username = request.json['username']
    user_query.user_id = request.json['user_id']
    user_query.real_name = request.json['realname']
    user_query.email = request.json['email']
    user_query.amount = request.json['amount']
    session.commit()
    return jsonify(id=user_query.id,
                   username=user_query.username,
                   user_id=user_query.user_id,
                   realname=user_query.real_name,
                   email=user_query.email,
                   amount=user_query.amount), 201

@app.route('/WS/user/<username>', methods=['DELETE'])
def delete_user_ws(username):
    try:
        user_query = session.query(User).filter_by(username=username).one()
    except:
        abort(404)
    session.delete(user_query)
    session.commit()
    return jsonify(id=user_query.id,
                   username=user_query.username,
                   user_id=user_query.user_id,
                   real_name=user_query.real_name,
                   email=user_query.email,
                   amount=user_query.amount), 201


#------------------CRUD WEBAPP USERS---------------------------------

@app.route('/App/create_user',methods=['POST','GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        real_name= request.form.get('real_name')
        email= request.form.get('email')
        user_id="1"
        succes=ORM.query_DB.create_user(username,user_id,real_name, email)
        if succes==True:
	    return render_template('succes.html')
        elif succes==False:
            return render_template('error.html', var="already exists")

@app.route('/App/edit_user',methods=['POST','GET'])
def edit_users():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        try:
            user = ORM.query_DB.get_user(username)
            return render_template('edit_user.html',user=user, username=username)
        except:
            return render_template('error.html', var="user not found")            

@app.route('/App/read_users')
def read_users():
    users = ORM.query_DB.get_all_users()
    return render_template('read_users.html',users=users)

@app.route('/App/read_user',methods=['POST','GET'])
def read_user():
    if request.method == 'GET':
        return render_template('read_user_form.html')
    elif request.method == 'POST':
        username= request.form.get('username')
        try:
            users = ORM.query_DB.get_user(username)
            return render_template('read_user.html',users=users)
        except:
            return render_template('error.html', var="user not found") 

@app.route('/App/delete_user',methods=['POST'])
def delete_user():
    (word,username)= request.form.get('username').split(' ')
    try:
        ORM.query_DB.delete_user(username)
        return render_template('succes.html')
    except:
        return render_template('error',var="not a user")

@app.route('/App/update_user',methods=['POST'])
def update_user():
    username= request.form.get('username')
    real_name= request.form.get('real_name')
    email= request.form.get('email')
    amount= request.form.get('amount')
    user_id= request.form.get('user_id')
    (word,original_username)= request.form.get('original_username').split(' ')
    ORM.query_DB.update_user(original_username,username,user_id,real_name,email,amount)
    return render_template('succes.html')

#------------------CRUD WS KEGS-------------------------------------

@app.route('/WS/keg/one/<int:keg_id>', methods=['GET'])
def get_keg_one(keg_id):
    try:
        keg_query = session.query(Keg).filter_by(kegid=keg_id).one()
        session.commit()
    except:
        abort(404)
    return jsonify(id=keg_query.id,
                   keg_id=keg_query.kegid,
                   amount=keg_query.amount), 201

@app.route('/WS/keg/all', methods=['GET'])
def get_keg_all():
    kegs_query = session.query(Keg).all()
    session.commit()
    kegs=[keg.__json__() for keg in kegs_query]
    if len(kegs) == 0:
        abort(404)
    return jsonify({'kegs': kegs}), 201


@app.route('/WS/keg', methods=['POST'])
def create_keg_ws():
    if not request.json or not 'kegid' in request.json or not 'amount' in request.json:
        abort(400)
    if ORM.query_DB.keg_exist(request.json['kegid']):
        abort(400)
    try:
        new_keg = Keg(kegid=request.json['kegid'],
                    amount=request.json['amount']) 
        session.add(new_keg)
        session.commit()
    except:
        abort(404)
    return jsonify(id=new_keg.id,
                   keg_id=new_keg.kegid,
                   amount=new_keg.amount), 201

@app.route('/WS/keg/<keg_id>', methods=['PUT'])
def update_keg_ws(keg_id):

    try:
        keg_query = session.query(Keg).filter_by(kegid=keg_id).one()
        keg_query.kegid = request.json['kegid']
        keg_query.amount = request.json['amount']
        session.add(keg_query)
        session.commit()
    except:
        abort(404)

    if not request.json:
        abort(400)
    return jsonify(id=keg_query.id,
                   kegid=keg_query.kegid,
                   amount=keg_query.amount), 201

@app.route('/WS/keg/<int:keg_id>', methods=['DELETE'])
def delete_keg_ws(keg_id):
    try:
        keg_query = session.query(Keg).filter_by(kegid=keg_id).one()
    except:
        abort(404)
    session.delete(keg_query)
    session.commit()
    return jsonify(id=keg_query.id,
                   keg_id=keg_query.kegid,
                   amount=keg_query.amount), 201

#------------------CRUD WEBAPP KEGS----------------------------------

@app.route('/App/create_keg',methods=['POST','GET'])
def create_keg():
    if request.method == 'GET':
        return render_template('create_keg.html')
    elif request.method == 'POST':
        keg_id=request.form.get('keg_id')
        amount=request.form.get('amount')
        succes = ORM.query_DB.create_keg(keg_id,amount)
        if succes==True:
	    return render_template('succes.html')
        elif succes==False:
            return render_template('error.html', var="keg already exists")

@app.route('/App/delete_keg',methods=['POST','GET'])
def delete_keg():
    if request.method == 'GET':
        return render_template('delete_keg.html')
    elif request.method == 'POST':
        (word1,word2,keg_id)= request.form.get('keg_id').split(' ')
        ORM.query_DB.delete_keg(keg_id)
	return render_template('succes.html')

@app.route('/App/edit_keg',methods=['POST','GET'])
def edit_kegs():
    if request.method == 'GET':
        return render_template('login_keg.html')
    elif request.method == 'POST':
        keg_id= request.form.get('keg_id')
        try:
            keg = ORM.query_DB.get_keg(keg_id)
            return render_template('edit_keg.html',keg=keg, keg_id=keg_id)
        except:
            return render_template('error.html', var="keg not found") 

@app.route('/App/update_keg',methods=['POST','GET'])
def update_keg():
    if request.method == 'GET':
        return render_template('update_keg.html')
    elif request.method == 'POST':
        keg_id= request.form.get('keg_id')
        amount= request.form.get('amount')
        (word1,word2,original_id) = request.form.get('original_id').split(' ')
        ORM.query_DB.update_keg(original_id,keg_id,amount)
	return render_template('succes.html')

@app.route('/App/read_kegs')
def read_kegs():
    kegs = ORM.query_DB.get_all_kegs()
    return render_template('read_kegs.html',kegs=kegs)

@app.route('/App/read_keg',methods=['POST','GET'])
def read_keg():
    if request.method == 'GET':
        return render_template('read_keg_form.html')
    elif request.method == 'POST':
        keg_id= request.form.get('keg_id')
        try:
            keg = ORM.query_DB.get_keg(keg_id)
            return render_template('read_keg.html',keg=keg)
        except:
            return render_template('error.html', var="keg not found") 

if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0')
