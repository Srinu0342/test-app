import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from test import db,T_Passenger_info

#creates all model tables to -->db _tables
db.create_all()

srinu=T_Passenger_info('Srinu','male','22','1')
tuli=T_Passenger_info('Tuli','female','33','2')

db.session.add_all([srinu,tuli])
#can also be used db.session_add()

db.session.commit()
