from . import db
from flask_login import UserMixin #custom class helps for login
from sqlalchemy.sql import func


class User(db.Model, UserMixin): #databse layout
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(150))
    lastname=db.Column(db.String(150))
    email=db.Column(db.String(150),unique=True)
    phone=db.Column(db.Integer)
    password=db.Column(db.String(150))
    country=db.Column(db.String(150))
    accounts=db.relationship('Account')

class Account(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150))
    type=db.Column(db.String(150))
    currency=db.Column(db.String(150))
    balance=db.Column(db.Integer)
    description=db.Column(db.String(150))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

