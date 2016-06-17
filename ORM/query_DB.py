from database import User, Base, Keg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ORM/mydatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


def user_exist(username):
    if session.query(User).filter_by(username=username).all()==[]:
         return False
    else:
         return True

def keg_exist(keg_id):
    if session.query(Keg).filter_by(kegid=keg_id).all()==[]:
         return False
    else:
         return True

#queries for users-----------------------------------------------------

def delete_user(username):
    session.query(User).filter_by(username=username).delete()
    session.commit()

def create_user(username,user_id,real_name, email):
    new_user = User(username=username, user_id=user_id, real_name=real_name, email=email, amount=0)
    data = get_all_users()
    exist = user_exist(username)
    if exist==False:
        session.add(new_user)
        session.commit()
        return True
    elif exist==True:
        return False
        

def update_user(original_username,username, given_user_id, real_name, email,amount):
    user_to_update = session.query(User).filter_by(username=original_username).one()
    if user_to_update != []:
        user_to_update.username=username
        user_to_update.user_id=given_user_id
        user_to_update.real_name=real_name
        user_to_update.email=email
        user_to_update.amount=amount
        session.add(user_to_update)
        session.commit()

def get_all_users():
    data = [row for row in session.query(User.username, User.user_id, User.email, User.real_name, User.amount)]
    return data

def get_user(username):
    user = [session.query(User.username, User.user_id, User.email, User.real_name, User.amount).filter_by(username=username).one()]
    return user

#queries for kegs-----------------------------------------------------


def delete_keg(given_keg_id):
    session.query(Keg).filter_by(kegid=given_keg_id).delete()
    session.commit()

def create_keg(keg_id, amount):
    new_keg = Keg(kegid=keg_id, amount=amount)
    data = get_all_kegs()
    exist = keg_exist(keg_id)
    if exist==False:
        session.add(new_keg)
        session.commit()
        return True
    elif exist==True:
        return False

def get_all_kegs():
    data = [row for row in session.query(Keg.kegid, Keg.amount)]
    return data

def get_keg(keg_id):
    keg = [session.query(Keg.kegid, Keg.amount).filter_by(kegid=keg_id).one()]
    return keg

def update_keg(original_id,keg_id, amount):
    keg_to_update = session.query(Keg).filter_by(kegid=original_id).one()
    if keg_to_update != []:
        keg_to_update.amount=amount
        keg_to_update.kegid=keg_id
        session.add(keg_to_update)
        session.commit()


