from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from apps.page.models import Post
from utils.paginations import BasePaginationClass
from utils.serializers import EmptySerializer


class BaseViewSet(GenericViewSet):
    """
    GenericViewSet with permissions and serializers by action

    action_serializers = {
        'list': DefaultListSerializer,
    }
    action_permissions = {
        'list': (AllowAny,),
    }
    """

    pagination_class = BasePaginationClass
    serializer_class = EmptySerializer
    action_permissions = {}
    action_serializers = {}

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, self.serializer_class)

    def get_permissions(self):
        permissions = self.action_permissions.get(self.action, self.permission_classes)
        return (permission() for permission in permissions)


class BasePostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.kwargs.pop("pk", None))
        self.check_object_permissions(self.request, obj.page)
        return obj
