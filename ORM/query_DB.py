from database import User, Base, Keg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ORM/mydatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()



#queries for users-----------------------------------------------------

def delete_user(given_user_id):
    session.query(User).filter_by(user_id=given_user_id).delete()
    session.commit()

def create_user(username,user_id,real_name, email):
    new_user = User(username=username, user_id=user_id, real_name=real_name, email=email, amount=0)
    session.add(new_user)
    session.commit()

def update_user(username, given_user_id, real_name, email,amount):
    user_to_update = session.query(User).filter_by(user_id=given_user_id).one()
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

#queries for kegs-----------------------------------------------------


def delete_keg(given_keg_id):
    session.query(Keg).filter_by(kegid=given_keg_id).delete()
    session.commit()

def create_keg(keg_id, amount):
    new_keg = Keg(kegid=keg_id, amount=amount)
    session.add(new_keg)
    session.commit()

def get_all_kegs():
    data = [row for row in session.query(Keg.kegid, Keg.amount)]
    print data
    return data

def update_keg(given_keg_id, amount):
    keg_to_update = session.query(Keg).filter_by(kegid=given_keg_id).one()
    if keg_to_update != []:
        keg_to_update.amount=amount
        keg_to_update.kegid=given_keg_id
        session.add(keg_to_update)
        session.commit()


