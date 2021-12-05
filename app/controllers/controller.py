from flask_restx import apidoc, Resource, reqparse
from app.config import app, api
from app.controllers.api import v1

# ================= BLUEPRINTS ==================
app.register_blueprint(v1)
# ==================== PAGES ====================

@api.route('/api/v1/login')
@api.doc(params={ 'username' : 'Username', 'password': 'Password'})
class AccountLogin(Resource):
    def post(self, username, password):
        return {}


@api.route('/api/v1/signup')
@api.doc(params={ 'username': 'Username', 'email': 'Email', 'password': 'Password'})
class AccountSignup(Resource):
    def post(self, username, email, password):
        return {}


@api.route('/api/v1/tweet')
@api.doc(params={ 'text': 'Tweet text'})
class AccountTweet(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def post(self):
        return {}


@api.route('/api/v1/logout')
class AccountLogout(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def post(self):
        return {}


@api.route('/api/v1/account')
class Profile(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def get(self):
        return {}


@api.route('/api/v1/tweets')
class ProfileTweets(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def get(self):
        return {}


@api.route('/api/v1/account/<username>')
class Account(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def get(self):
        return {}


@api.route('/api/v1/account/<username>/tweets')
class AccountTweets(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def get(self):
        return {}


@api.route('/api/v1/users')
class Users(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def get(self):
        return {}


@api.route('/api/v1/update_password')
class PasswordUpdate(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def post(self):
        return {}

    @api.doc(security={'Authorization' : 'auth_token'})
    def put(self):
        return {}


@api.route('/api/v1/delete_tweet/<tweet_id>')
class DeleteTweet(Resource):
    @api.doc(security={'Authorization' : 'auth_token'})
    def delete(self):
        return {}


@app.route('/')
def start_page():
    return apidoc.ui_for(api)
