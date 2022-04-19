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

