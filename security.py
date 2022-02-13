from hmac import compare_digest
from user import User

users = [
    User(3, 'felita', 'patedecampagne')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None) # default None if username doesn't exist
    if user and compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
