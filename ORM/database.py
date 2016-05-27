
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

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




from sqlalchemy import create_engine
path_to_db = "ORM/mydatabase.db"
engine = create_engine('sqlite:///' + path_to_db)
Base.metadata.create_all(engine)
