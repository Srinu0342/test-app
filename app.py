from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

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


app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    name='Default'
    sex='male'
    age='20'
    pclass='1'
    #name=request.args.get('name')
    try:
        name=request.form['name']
        if name==None:
            name='Default'
    except:
        name='Default'

    name1=name.rstrip().split()[0]

    #sex=request.args.get('sex')   for get method in form
    try:
        sex=request.form['sex']
        if sex==None:
            sex='male'
    except:
        sex='male'

    #age=request.args.get('age')
    try:
        age=request.form['age']#for post method in form
        if age==None:
            age='20'
    except:
        age='20'
    #pclass=request.args.get('class')
    try:
        pclass=request.form['class']
        if pclass==None:
            pclass='1'
    except:
        pclass='1'

    a=[name1,sex.rstrip(),age.rstrip(),pclass.rstrip()]
    f=open("model.dat","rb")
    pre=pickle.load(f)
    x=dataprep(a)
    ans=pre.predict(x)

    if name!='Default':
        if ans[0]==0 :
            prediction='Passenger will not survive'
        else:
            prediction='Passenger will survive'
    else:
        prediction='first fill up the form properly'

    return render_template('ml_projects.html', prediction=prediction, name=name)

@app.route('/titanic')
def titanic():
    return render_template('titanic.html')

@app.route('/titanic/result',methods=['GET','POST'])
def Tresult():
    name=request.args.get('name').rstrip()
    name1=name.split()[0]
    sex=request.args.get('sex').rstrip()
    age=request.args.get('age').rstrip()
    pclass=request.args.get('class').rstrip()
    a=[name1,sex,age,pclass]
    f=open("model.dat","rb")
    pre=pickle.load(f)
    x=dataprep(a)
    ans=pre.predict(x)
    if ans[0]==0:
        prediction='Passenger will not survive'
    else:
        prediction='Passenger will survive'

    return render_template('titanic_result.html',prediction=prediction)

if __name__=='__main__':
    app.run(debug=True)
