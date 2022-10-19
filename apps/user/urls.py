from django.urls import path, include
from .views import AuthenticationView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'auth', AuthenticationView, basename="User")

urlpatterns = [
        path('', include(router.urls))
    ]
