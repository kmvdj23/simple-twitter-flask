import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database.db'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['CORS_EXPOSE_HEADERS'] = [ "Content-Type", "X-CSRFToken", 'content-type', 'x-csrftoken' ]
app.config['DEBUG'] = True

db = SQLAlchemy(app)
guard = Praetorian()
cors = CORS(app)
ma = Marshmallow()

guard.blacklist = list()
