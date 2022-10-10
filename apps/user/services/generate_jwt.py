import datetime
import jwt
from innotter.settings import SECRET_KEY


def generate_token(user, days=0, minutes=0):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, minutes=minutes),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    return token


def generate_access_token(user):
    return generate_token(user, minutes=5)


def generate_refresh_token(user):
    return generate_token(user, days=7)
