import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

df=pd.read_csv(r'C:\Users\bigGs\Desktop\titanic\titanic.csv')
df['Age'].fillna(df['Age'].median(),inplace=True)

df=df[df['Age']<100]

sex_dummies=pd.get_dummies(df['Sex'])

class_dummies=pd.get_dummies(df['Pclass'])

df1=df

df=pd.concat([df,sex_dummies,class_dummies],axis=1)

df1=df

df.drop(['Name', 'Siblings/Spouses Aboard', 'Parents/Children Aboard', 'Fare','Sex','Pclass'],axis=1,inplace=True)

model=LogisticRegression()



y=df['Survived']

df1=df
df1.drop(['Survived'],axis=1,inplace=True)

x=df1

x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.1)

model.fit(x_train,y_train)

f=open("model.dat","wb")

pickle.dump(model,f)

f.close()

predictions=model.predict(x_test)

a=accuracy_score(y_test,predictions)*100

print(a)

a=input('Enter Data:\nName  Sex  Age  Pclass:\n').split()

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

x=dataprep(a)

a=model.predict(x)

print(a[0])
