from flask_login import UserMixin
from app.config import app, db, ma, guard
from app.lib import ResourceMixin


class Account(db.Model, UserMixin, ResourceMixin):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    roles = db.Column(db.Text)
    hashed_password = db.Column(db.String(1024), nullable=False)
    is_active = db.Column(db.Boolean, default=True, server_default="true")



    @property
    def identity(self):
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*
        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*
        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*
        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    @classmethod
    def get_users(cls):
        return Account.query.all()


    @classmethod
    def find(cls, identity):
        return Account.query.filter(
            (cls.email == identity) | (cls.username == identity)
        ).first()

    def to_dict(self, decode=False):
        schema = AccountSchema()
        _dict = schema.dump(self)

        return _dict

class Tweet(db.Model, ResourceMixin):

    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship("Account", backref=db.backref("tweets", lazy=True))

    @classmethod
    def get_tweet(cls, tweet_id):
        return Tweet.query.filter(cls.id == tweet_id).first()

    def to_dict(self, decode=False):
        schema = TweetSchema()
        _dict = schema.dump(self)

        return _dict


#=========================== SCHEMA =================================
class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account
        include_fk = True
        tweets = ma.Nested('TweetSchema', exclude=('tweet',), many=True, dump_only=True)


class TweetSchema(ma.ModelSchema):
    class Meta:
        model = Tweet
        include_fk = True
        account = ma.Nested('AccountSchema', exclude=('account',), many=False, dump_only=True)


def is_blacklisted(jti):
    return jti in guard.blacklist


guard.init_app(app, Account, is_blacklisted=is_blacklisted)
