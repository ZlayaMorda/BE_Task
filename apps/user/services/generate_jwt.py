import datetime
import jwt
from django.contrib.auth import get_user_model
from rest_framework import exceptions

from innotter.settings import SECRET_KEY


class CustomJwt:
    @staticmethod
    def _generate_token(user, days=0, minutes=0):
        token_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, minutes=minutes),
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
        return token

    def generate_access_token(self, user):
        return self._generate_token(user, minutes=5)

    def generate_refresh_token(self, user):
        return self._generate_token(user, days=7)

    @staticmethod
    def get_user_from_refresh(request):
        User = get_user_model()
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return user
