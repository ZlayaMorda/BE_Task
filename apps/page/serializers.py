from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from apps.page.models import Reaction, Tag, Page, Post
from apps.user.models import CustomUser


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        validators = []


class PageCreationTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)


class PageCreateSerializer(serializers.ModelSerializer):
    tags = PageCreationTagSerializer(required=False, many=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        page = Page.objects.create(**validated_data)
        for tag in tags_data:
            new_tag = Tag.objects.get_or_create(**tag)
            page.tags.add(new_tag[0])
        return page

    class Meta:
        model = Page
        fields = ("name", "description", "owner", "image", "is_private", "tags")


class PageUpdateSerializer(serializers.ModelSerializer):
    tags = PageCreationTagSerializer(required=False, many=True)
    description = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        for tag in tags_data:
            new_tag = Tag.objects.get_or_create(**tag)
            instance.tags.add(new_tag[0])

        return super(PageUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image", "is_private", "tags")


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image", "is_private", "tags", "is_blocked")


class FollowPageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
