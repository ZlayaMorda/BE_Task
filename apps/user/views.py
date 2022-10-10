import jwt
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.views import BaseViewSet
from rest_framework import mixins

from innotter.settings import SECRET_KEY

from apps.user.models import CustomUser
from apps.user.serializers import CustomUserCreateSerializer, CustomUserLoginSerializer, CustomUserListSerializer
from apps.user.services.generate_jwt import generate_access_token, generate_refresh_token


class ListUser(mixins.ListModelMixin, BaseViewSet):
    serializer_class = CustomUserListSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()


@method_decorator(csrf_protect, name='create')
class SignUPUserView(mixins.CreateModelMixin, BaseViewSet):
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]


class SignInUserView(BaseViewSet):
    serializer_class = CustomUserLoginSerializer
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=('post',))
    def login_user(self, request):
        serialized_user = self.serializer_class(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email=request.data['email'])
        response = Response()
        response.set_cookie(key='refreshtoken', value=generate_refresh_token(user), httponly=True)
        response.data = {
            'access_token': generate_access_token(user),
        }

        return response


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    """
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    """
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

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})
