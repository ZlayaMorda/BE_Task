from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.page.serializers import PageCreateSerializer
from utils.views import BaseViewSet


class PageCreateView(BaseViewSet, mixins.CreateModelMixin):
    action_serializers = {
        'create': PageCreateSerializer,
    }

    action_permissions = {
        'create': (IsAuthenticated, ),
    }
