from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'create', PageCreateView, basename="Page")
router.register(r'update', PageUpdateView, basename="Page")
router.register(r'block', PageBlockUpdateView, basename="Page")
router.register(r'list', PageListView, basename="Page")
router.register(r'follow', FollowPageUpdateView, basename="Page")
router.register(r'list-followers', FollowPageListView, basename="Page")
router.register(r'post', PostCreateView, basename="Post")
router.register(r'post/update', PostUpdateView, basename="Post")
router.register(r'post/delete', PostDeleteView, basename="Post")
router.register(r'post/list', PostListView, basename="Post")
router.register(r'liked-posts', ListLikedPostView, basename="Reaction")
router.register(r'post', CreateLikeView, basename="Reaction")

urlpatterns = [
        path('', include(router.urls))
    ]
