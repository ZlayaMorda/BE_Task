from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from apps.page.models import Page, Tag, Post, Reaction
from apps.page.paginations import PageListPaginationClass
from apps.page.permissions import IsPageNotBlocked, IsPageFollower
from apps.page.serializers import PageCreateSerializer, PageUpdateSerializer, PageListSerializer, \
    FollowPageUpdateSerializer, FollowerListSerializer, PostCreateSerializer, PostUpdateDeleteSerializer, \
    LikedPostListSerializer, LikeCreateSerializer, PostSerializer, PageBlockUpdateSerializer
from apps.page.services.page import PageServices
from apps.user.permissions import IsOwnerOrReadOnly, IsOwner, IsNotBlocked, IsAdmin, IsModerator
from utils.views import BaseViewSet, BasePostViewSet


class PageCreateView(BaseViewSet, mixins.CreateModelMixin):
    action_serializers = {
        'create': PageCreateSerializer,
    }
    action_permissions = {
        'create': (IsAuthenticated, IsNotBlocked),
    }


class PageUpdateView(BaseViewSet, mixins.UpdateModelMixin):
    action_serializers = {
        'partial_update': PageUpdateSerializer,
    }
    action_permissions = {
        'partial_update': (IsOwnerOrReadOnly, IsPageNotBlocked, IsNotBlocked)
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
        'approve_follow': (IsAuthenticated, IsOwnerOrReadOnly, IsPageNotBlocked, IsNotBlocked)
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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        return Response(status=HTTP_200_OK)

class PageBlockUpdateView(BaseViewSet, mixins.UpdateModelMixin):
    action_serializers = {
        'update': PageBlockUpdateSerializer
    }

    action_permissions = {
        'update': (IsAuthenticated, IsAdmin or IsModerator)
    }

    queryset = Page.objects.all()

class FollowPageListView(BaseViewSet, mixins.ListModelMixin):
    action_serializers = {
        'list': FollowerListSerializer,
    }

    action_permissions = {
        'list': (IsAuthenticated, (IsPageNotBlocked and IsOwner) or (IsAdmin or IsModerator))
    }

    pagination_class = PageListPaginationClass

    def get_queryset(self):
        return PageServices.get_followers_queryset(self)

class PostCreateView(BaseViewSet):
    action_serializers = {
        "create_post": PostCreateSerializer,
    }
    action_permissions = {
        "create_post": (IsAuthenticated, IsPageNotBlocked, IsOwner, IsNotBlocked),
    }
    queryset = Page.objects.all()
    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.pop("pk", None))
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=('post',), url_path='create-post')
    def create_post(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(request.data)
        return Response(status=HTTP_201_CREATED)

class PostUpdateView(BasePostViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    action_serializers = {
        "partial_update": PostUpdateDeleteSerializer,
    }

    action_permissions = {
        "partial_update": (IsAuthenticated, IsPageNotBlocked, IsOwner, IsNotBlocked),
    }

class PostDeleteView(BasePostViewSet, mixins.DestroyModelMixin):
    action_serializers = {
        "destroy": PostUpdateDeleteSerializer,
    }

    action_permissions = {
        "destroy": (IsAuthenticated, (IsPageNotBlocked and IsOwner and IsNotBlocked) or (IsAdmin or IsModerator)),
    }

class PostListView(BasePostViewSet, mixins.ListModelMixin):
    action_serializers = {
        "list": PostSerializer,
    }

    action_permissions = {
        "list": (IsAuthenticated, (IsNotBlocked and (IsOwner or IsPageFollower)) or (IsAdmin or IsModerator))
    }

    pagination_class = PageListPaginationClass

    def get_queryset(self):
        return PageServices.get_page_posts(self)


class ListLikedPostView(BaseViewSet, mixins.ListModelMixin):
    action_serializers = {
        "list": LikedPostListSerializer,
    }

    action_permissions = {
        "list": (IsAuthenticated, IsNotBlocked),
    }

    pagination_class = PageListPaginationClass

    def get_queryset(self):
        return PageServices.get_liked_posts(self)

class CreateLikeView(BasePostViewSet):
    action_serializers = {
        "create_reaction": LikeCreateSerializer,
    }

    action_permissions = {
        "create_reaction": (IsAuthenticated, IsNotBlocked, IsPageNotBlocked,),
    }

    queryset = Post.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.pop("pk", None))
        self.check_object_permissions(self.request, obj.page)
        return obj

    @action(detail=True, methods=('post',), url_path='create-reaction')
    def create_reaction(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        reaction = serializer.create_reaction(request)
        return Response(reaction, status=HTTP_201_CREATED)
