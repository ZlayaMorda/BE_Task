from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.user.urls')),
    path('pages/', include('apps.page.urls')),
]
