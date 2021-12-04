from flask import jsonify, request, Blueprint
from flask_praetorian import auth_required, current_user
from app.models import Account, Tweet, guard
from flask_cors import CORS

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

CORS(v1)

# ====================== GET ====================================
@v1.route('/account', methods=['GET'])
@auth_required
def view_profile():
    account = Account.find(current_user().username)
    if account:
        return (jsonify(account.to_dict()), 200)

    else:
        data = {
            "message": "Account not found"
        }

        return (jsonify(data), 200)


@v1.route('/tweets', methods=['GET'])
@auth_required
def get_account_tweets():

    account = Account.find(current_user().username)
    if account:

        tweets_list = list()

        for tweet in account.tweets:
            tweets_list.append(tweet.to_dict())

        return (jsonify(tweets_list), 200)

    else:
        data = {
            "message": "Account not found"
        }

        return (jsonify(data), 200)


# ==================== POST ===================================
@v1.route('/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    old_token = guard.read_token_from_header()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return (jsonify(ret), 200)

@v1.route('/update_password', methods=['POST'])
@auth_required
def update_password():
    req = request.get_json(force=True)
    password = req.get('password')

    account = Account.find(current_user().username)
    account.hashed_password = guard.hash_password(password)
    account.save()

    user = guard.authenticate(account.username, password)

    return (jsonify({'message': 'Password updated'}) , 200)


@v1.route('/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {"access_token": guard.encode_jwt_token(user)}
    return (jsonify(ret), 200)


@v1.route('/signup', methods=['POST'])
def signup():

    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    email = req.get('email', None)

    account = Account(
        hashed_password=guard.hash_password(password),
        username=username,
        email=email
    )

    account.save()

    user = guard.authenticate(username, password)

    if user:
        data = {
            "access_token": guard.encode_jwt_token(user)
        }

        return (jsonify(data), 200)
    else:
        data = {
            "message": "Incorrect username/password"
        }

        return (jsonify(data), 401)


@v1.route('/logout', methods=['GET', 'POST'])
@auth_required
def logout():

    old_token = guard.read_token_from_header()
    data = guard.extract_jwt_token(old_token)
    guard.blacklist.append(data['jti'])

    data = {
        "message": "Logout successful",
    }

    return (jsonify(data), 200)


@v1.route('/delete_tweet/<tweet_id>', methods=['POST'])
@auth_required
def delete_tweet(tweet_id):

    tweet = Tweet.get_tweet(tweet_id)
    if tweet and tweet.account_id == current_user().id:
        tweet.delete()

        data = {
            "message": "Tweet deleted",
        }

        return (jsonify(data), 200)

    else:
        data = {
            "message": "Tweet not found",
        }

        return (jsonify(data), 200)


@v1.route('/tweet', methods=['POST'])
@auth_required
def tweet():

    req = request.get_json(force=True)
    text = req.get('text', None)
    tweet = Tweet(
        text=text,
        account_id=current_user().id
    )

    tweet.save()

    data = {
        "message": 'Tweet Successful',
    }

    return (jsonify(data), 200)
