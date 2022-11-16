from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.user.services.authentication import SafeJWTAuthentication


class AuthMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):

        try:
            jwt_auth = SafeJWTAuthentication().authenticate(request)
            request.user = jwt_auth
        except Exception as e:
            print(e)
            request.user = AnonymousUser()


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
