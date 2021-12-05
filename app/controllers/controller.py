from flask_restplus import apidoc, Resource
from app.config import app, api
from app.controllers.api import v1

# ================= BLUEPRINTS ==================
app.register_blueprint(v1)
# ==================== PAGES ====================

@api.route('/api/v1/login')
@api.doc(params={ 'username' : 'Username', 'password': 'Password'})
class AccountLogin(Resource):
    def post(self, username, password):
        return {
            "username" : username,
            "password" : password
        }

@api.route('/api/v1/signup')
@api.doc(params={ 'username': 'Username', 'email': 'Email', 'password': 'Password'})
class AccountSignup(Resource):
    def post(self, username, email, password):
        return {}


@app.route('/')
def start_page():
    return apidoc.ui_for(api)
