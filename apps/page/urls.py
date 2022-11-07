from django.urls import path, include
from .views import PageCreateView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'create', PageCreateView, basename="Page")

urlpatterns = [
        path('', include(router.urls))
    ]
