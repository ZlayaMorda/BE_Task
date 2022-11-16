from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'create', PageCreateView, basename="Page")
router.register(r'update', PageUpdateView, basename="Page")
router.register(r'list', PageListView, basename="Page")
router.register(r'follow', FollowPageUpdateView, basename="Page")

urlpatterns = [
        path('', include(router.urls))
    ]
