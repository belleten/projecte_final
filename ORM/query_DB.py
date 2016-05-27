from database import User, Base, Keg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()



#queries-----------------------------------------------------

def get_user():
    pass

def get_all():
    pass

def create_user():
    new_user1 = User(username='c3po', user_id="00x21", real_name="C3PO", email="c3po@therealandroids.com", amount=22.5)
    session.add(new_user1)

def delete_user():
    pass
