import json
from flask import jsonify, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Account, Tweet
from lib import generate_random_password as generate_auth_token, decrypt_password, encrypt_password, generate_uuid

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')



#====================== GET ====================================

@v1.route('/account', methods=['GET'])
@token_required
@login_required
def view_profile():
    pass


@v1.route('/<username>', methods=['GET'])
@token_required
@login_required
def view_other_profile(username):
    pass

# ==================== POST ===================================
@v1.route('/add_account', methods=['POST'])
def signup():

    request.form.get('username')
    request.form.get('email')
    request.form.get('password')

    account = Account(
        first_name=first_name,
        last_name=last_name,
        password=encrypt_password(password),
        username=username,
        email=email,
        mobile=mobile
    )

    account.save()

    if login_user(account) and account.is_active():
        account.update_activity_tracking(request.remote_addr)

        data = {
            'auth_token' : generate_auth_token(len=50),
            'account' : current_user.to_dict()
        }

    else:
        data = {
            'message' : 'Account not created',
            'status' : 503
        }

    return json.dumps(data)


@v1.route('/logout', methods=['GET', 'POST'])
@token_required



@v1.route('/delete_tweet/<tweet_id>', methods=['POST'])
@token_required
@login_required
def delete_tweet(tweet_id):
    pass


@v1.route('/tweet', methods=['POST'])
@token_required
@login_required
def tweet():

    request.form.get('text')
    tweet = Tweet(text=text)
    tweet.save()

    data = {
        "message": 'Tweet Successful',
        "status" : 200
    }

    return json.dumps(data)
