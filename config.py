from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3308/swapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
