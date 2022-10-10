from django.urls import path, include
from .views import SignUPUserView, SignInUserView, refresh_token_view, ListUser
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'signup', SignUPUserView, basename="User")
router.register(r'signin', SignInUserView, basename="User")

urlpatterns = [
        path('refresh/', refresh_token_view, name='refresh'),
        path('', include(router.urls))
    ]
