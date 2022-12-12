from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.page.models import Page, Tag, Reaction, Post


class PageServices:
    @staticmethod
    def get_filter_queryset(self):
        queryset = Page.objects.all()
        page_name = self.request.query_params.get('name')
        page_uuid = self.request.query_params.get('uuid')
        page_tags = self.request.query_params.getlist('tags')

        if page_name is not None:
            temp_query = queryset.filter(name=page_name)
            if temp_query:
                queryset = temp_query
        if page_uuid is not None:
            temp_query = queryset.filter(uuid=page_uuid)
            if temp_query:
                queryset = temp_query
        if page_tags is not None:
            for tag in page_tags:
                try:
                    temp_query = queryset.filter(tags=Tag.objects.get(name=tag).pk)
                    if temp_query:
                        queryset = temp_query
                except ObjectDoesNotExist:
                    continue
        return queryset

    @staticmethod
    def update_follow(request, page):
        user = request.user
        if page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)
        return Response(status=HTTP_200_OK)

    @staticmethod
    def get_followers_queryset(self):
        queryset = Page.objects.all()
        obj = get_object_or_404(queryset, pk=self.request.query_params.get('uuid'))
        self.check_object_permissions(self.request, obj)
        return obj.follow_requests.all()

    @staticmethod
    def get_liked_posts(self):
        queryset = Reaction.objects.filter(owner=self.request.user, like=True)
        return queryset

    @staticmethod
    def get_page_posts(self):
        queryset = Post.objects.filter(page=self.request.query_params.get('pk'))
        return queryset
