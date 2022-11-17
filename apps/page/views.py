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
        'follow': FollowPageUpdateSerializer,
        'approve_follow': FollowPageUpdateSerializer
    }
    action_permissions = {
        'follow': (IsAuthenticated, IsPageNotBlocked),
        'approve_follow': (IsAuthenticated, IsOwnerOrReadOnly, IsPageNotBlocked)
    }
    queryset = Page.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.pop("pk", None))
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=('patch',), url_path='send-request')
    def follow(self, request, **kwargs):
        page = self.get_object()
        return PageServices.update_follow(request, page)

    @action(detail=True, methods=('patch', ), url_path='approve')
    def approve_follow(self, request, **kwargs):
        # partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        return Response(status=HTTP_200_OK)
