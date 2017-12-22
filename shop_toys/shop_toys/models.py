from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,ForeignKey,Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship
import os

if os.path.exists("avtograf.db"):
    os.remove("avtograf.db")

engine = create_engine('sqlite:///avtograf.db', encoding='utf-8')
Session = sessionmaker()
Base = declarative_base(bind=engine)

class User(Base):
     __tablename__ = "Users"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     Mail = Column(String, nullable = False)
     FirstName = Column(String, nullable = False)
     SecondName = Column(String, nullable = False)
     def __init__(self, Login, Password, Mail, FirstName, SecondName):
          self.Login = Login
          self.Password = Password
          self.Mail = Mail
          self.FirstName = FirstName
          self.SecondName = SecondName

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.Mail + " " +self.FirstName 

class Comments(Base):
     __tablename__ = "Comments"
     id = Column(Integer, nullable=False, primary_key=True)
     Login = Column(String, ForeignKey('Users.Login'),ForeignKey('Users.Login'), nullable = False)
     Name_com = Column(String, nullable = False)
     Text = Column(String, nullable = False)
     Date = Column(Date, nullable = False)

     def __init__(self, Login, Name_com,Text,Date):
          self.Login = Login
          self.Name_com = Name_com
          self.Text = Text
          self.Date = Date

     def __repr__(self):
          return self.Login + " " + self.Name_com + " " + self.Text+ " " +str(self.id)


class bGoods(Base):
     __tablename__ = "bGoods"
     id = Column(Integer, nullable=False, primary_key=True)
     creater = Column(String, ForeignKey('Users.Login'),ForeignKey('Users.Login'), nullable = False)
     manufacturer = Column(Integer, nullable=False)
     text = Column(String, nullable = False)
     date = Column(Date, nullable = False)

     def __init__(self, creater, manufacturer,text,date):
          self.creater = creater
          self.manufacturer = manufacturer
          self.text = text
          self.date = date

     def __repr__(self):
          return self.creater + " " + self.manufacturer + " " + self.text+ " " +str(self.id)

class adress(Base):
     __tablename__ = "adress"
     id = Column(Integer, nullable=False, primary_key=True)
     adress = Column(String, nullable = False)

     def __init__(self, adress):
          self.adress = adress

     def __repr__(self):
          return self.adress+ " " +str(self.id)

class manufactures(Base):
     __tablename__ = "manufactures"
     id = Column(Integer, nullable=False, primary_key=True)
     mName = Column(String, nullable = False)

     def __init__(self, mName):
          self.mName = mName

     def __repr__(self):
          return self.mName+ " " +str(self.id)

