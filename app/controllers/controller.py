from flask_restx import apidoc, Resource, reqparse
import json
from app.config import app, api
from app.controllers.api import v1

# ================= BLUEPRINTS ==================
app.register_blueprint(v1)
# ==================== PAGES ====================

@api.route('/api/v1/login')
@api.doc(params={ 'username' : 'Username', 'password': 'Password'})
class AccountLogin(Resource):
    def post(self, username, password):
        return json.dumps({
            "username" : username,
            "password" : password
        })

@api.route('/api/v1/signup')
@api.doc(params={ 'username': 'Username', 'email': 'Email', 'password': 'Password'})
class AccountSignup(Resource):
    def post(self, username, email, password):
        return {}

@api.route('/api/v1/tweet')
@api.doc(params={ 'text': 'Tweet text'})
class AccountTweet(Resource):
    def post(self):
        return {}


@app.route('/')
def start_page():
    return apidoc.ui_for(api)
