from flask_login import UserMixin
from app.config import db
from app.lib import ResourceMixin



class Account(db.Model, UserMixin, ResourceMixin):

    __tablename__ = "account"


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)

    @classmethod
    def find(cls, identity):
        return Account.query.filter(
            (cls.email == identity) | (cls.username == identity)
        ).first()



class Tweet(db.Model, ResourceMixin):

    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)

    @classmethod
    def get_tweet(cls, tweet_id):
        return Tweet.query.filter(id == tweet_id).first()
