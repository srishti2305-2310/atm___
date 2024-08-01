import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_LIFETIME = timedelta(minutes=10)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)

def generate_access_token(user):
    expiration = datetime.utcnow() + ACCESS_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def generate_refresh_token(user):
    expiration = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
