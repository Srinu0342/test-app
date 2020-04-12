import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

#f=open(r'C:\Users\bigGs\Desktop\titanic\model.dat',"rb")

#obj=pickle.load(f)

def dataprep(a):
    a=[a]
    x=pd.DataFrame(a,index=[1],columns='Name  Sex  Age  Pclass'.split())

    sd=pd.get_dummies(x['Sex'])
    if sd.columns[0]=='male':
        sd=pd.concat([pd.DataFrame([0],index=[1],columns=['female']),sd],axis=1)
    else:
        sd=pd.concat([sd,pd.DataFrame([0],index=[1],columns=['male'])],axis=1)

    cd=pd.get_dummies(x['Pclass'])

    if cd.columns[0]=='1':
        cd=pd.concat([cd,pd.DataFrame([[0,0]],index=[1],columns=['2','3'])],axis=1)
    elif cd.columns[0]=='2':
        cd=pd.concat([pd.DataFrame([0],index=[1],columns=['1']),cd,pd.DataFrame([0],index=[1],columns=['3'])],axis=1)
    elif cd.columns[0]=='3':
        cd=pd.concat([pd.DataFrame([[0,0]],index=[1],columns=['1','2']),cd],axis=1)

    x=pd.concat([x,sd,cd],axis=1)
    x.drop(['Name','Sex','Pclass'],axis=1,inplace=True)
    return x

#a=input('Enter Data:\nName  Sex  Age  Pclass:\n').split()

#x=dataprep(a)
#f.close
#a=obj.predict(x)

#print(a[0])

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL']='sqlite:///'+os.path.join(basedir,'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
#flask app is linked with the database

class T_Passenger_info(db.Model):
    __table__="T_Passenger_infos"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    sex=db.Column(db.Text)
    age=db.Column(db.Text)
    Pclass=db.Column(db.Text)
    def __init__(self,name,sex,age,Pclass):
        self.name=name
        self.sex=sex
        self.age=age
        self.Pclass=Pclass

    def __repr__(self):
        return f"Passenger info name:{self.name}, sex:{self.sex}, age:{self.age}, Passenger Class:{self.Pclass}"
