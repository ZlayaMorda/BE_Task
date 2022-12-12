from django.urls import path, include
from .views import AuthenticationView, BlockUserView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'auth', AuthenticationView, basename="User")
router.register(r'user-block', BlockUserView, basename="User")

urlpatterns = [
        path('', include(router.urls))
    ]
