import jwt
from rest_framework import exceptions

from apps.user.models import CustomUser
from innotter.settings import SECRET_KEY


class SafeJWTAuthentication:
    @staticmethod
    def authenticate(request):

        User = CustomUser
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            raise exceptions.AuthenticationFailed('missing header')
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return user
