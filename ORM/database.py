
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     # this field will identify uniquely any user in the database
     # more info here -> http://www.w3schools.com/sql/sql_primarykey.asp
     id = Column(Integer, primary_key=True)
     username = Column(String)
     user_id = Column(String)
     real_name = Column(String)
     email = Column(String)
     amount = Column(Float)

     def __repr__(self):
        return "<user(username='%s', user_id='%s' ,real_name='%s', email='%s', amount='%f' )>" % (
                             self.username, self.user_id, self.real_name, self.email,self.amount)

     def __json__ (self):
        dict_user ={}
        dict_user["id"] = self.id
        dict_user["username"] = self.username
        dict_user["user_id"] = self.user_id
        dict_user["realname"] = self.real_name
        dict_user["email"] = self.email
        dict_user["amount"] = self.amount
        return dict_user


class Keg(Base):
     __tablename__ = 'keg'
     # this field will identify uniquely any user in the database
     # more info here -> http://www.w3schools.com/sql/sql_primarykey.asp
     id = Column(Integer, primary_key=True)
     kegid = Column(String)
     amount = Column(Float)

     def __repr__(self):
        return "keg(kegid='%s', amount='%f')>" % (
                             self.kegid,self.amount)

     def __json__ (self):
        dict_keg ={}
        dict_keg["id"] = self.id
        dict_keg["kegid"] = self.kegid
        dict_keg["amount"] = self.amount
        return dict_keg



engine = create_engine('sqlite:///ORM/mydatabase.db')
Base.metadata.create_all(engine)



