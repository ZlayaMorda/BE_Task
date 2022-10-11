from django.urls import path, include
from .views import AuthenticationView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'authentication', AuthenticationView, basename="User")
# router.register(r'signin', SignInUserView, basename="User")

urlpatterns = [
        path('', include(router.urls))
    ]
