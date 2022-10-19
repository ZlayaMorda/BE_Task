from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.views import BaseViewSet
from rest_framework import mixins

from apps.user.models import CustomUser
from apps.user.serializers import CustomUserCreateSerializer, CustomUserLoginSerializer
from apps.user.services.generate_jwt import CustomJwt


class AuthenticationView(BaseViewSet, mixins.CreateModelMixin):
    action_serializers = {
        'sign_up': CustomUserCreateSerializer,
        'sign_in': CustomUserLoginSerializer,
    }

    action_permissions = {
        'sign_up': (AllowAny, ),
        'sign_in': (AllowAny, ),
        'refresh_token': (AllowAny, ),
    }

    permission_classes = []

    @action(detail=False, methods=('post', ), url_path='sign-up')
    def sign_up(self, request):
        serializer = self.get_serializer_class()
        serialized_user = serializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        serialized_user.save()
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=('post',), url_path='sign-in')
    def sign_in(self, request):
        serializer = self.get_serializer_class()
        serialized_user = serializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email=request.data['email'])

        data = {
            'access_token': CustomJwt().generate_access_token(user),
            'refresh_token': CustomJwt().generate_refresh_token(user)
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='refresh-token')
    def refresh_token(self, request):
        """
        To obtain a new access_token this view expects 2 important things:
            1. a cookie that contains a valid refresh_token
            2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
        """
        user = CustomJwt().get_user_from_refresh(request)

        access_token = CustomJwt().generate_access_token(user)
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)
