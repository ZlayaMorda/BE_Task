from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.page.models import Page, Tag
from apps.page.paginations import PageListPaginationClass
from apps.page.permissions import IsPageNotBlocked
from apps.page.serializers import PageCreateSerializer, PageUpdateSerializer, PageListSerializer, \
    FollowPageUpdateSerializer
from apps.page.services.page import PageServices
from apps.user.permissions import IsOwnerOrReadOnly
from utils.views import BaseViewSet


class PageCreateView(BaseViewSet, mixins.CreateModelMixin):
    action_serializers = {
        'create': PageCreateSerializer,
    }
    action_permissions = {
        'create': (IsAuthenticated,),
    }


class PageUpdateView(BaseViewSet, mixins.UpdateModelMixin):
    action_serializers = {
        'update': PageUpdateSerializer,
    }
    action_permissions = {
        'update': (IsOwnerOrReadOnly, IsPageNotBlocked)
    }
    queryset = Page.objects.all()


class PageListView(BaseViewSet, mixins.ListModelMixin):
    action_serializers = {
        'list': PageListSerializer,
    }
    action_permissions = {
        'list': (IsAuthenticated,)
    }
    pagination_class = PageListPaginationClass

    def get_queryset(self):
        return PageServices.get_filter_queryset(self)


class FollowPageUpdateView(BaseViewSet, mixins.UpdateModelMixin):
    action_serializers = {
        'update': FollowPageUpdateSerializer,
    }
    action_permissions = {
        'update': (IsAuthenticated, IsPageNotBlocked)
    }
    queryset = Page.objects.all()

    def get_object(self, **kwargs):
        pk = kwargs.get("pk", None)
        obj = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, **kwargs):
        page = self.get_object(**kwargs)
        return PageServices.update_follow(request, page)


class AllowFollowUpdateView(BaseViewSet, mixins.UpdateModelMixin):
    action_serializers = {
        'update': FollowPageUpdateSerializer
    }

    action_permissions = {
        'update': (IsAuthenticated, IsOwnerOrReadOnly, IsPageNotBlocked)
    }
