from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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

class PageBlockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("is_blocked", "unblock_date")


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image", "is_private", "tags", "is_blocked")


class FollowPageUpdateSerializer(serializers.Serializer):
    follow_pk = serializers.IntegerField(required=False)
    approve = serializers.BooleanField()

    def update(self, instance, validated_data):
        try:
            approve = validated_data.pop("approve")
            request_pk = validated_data.pop("follow_pk")
        except KeyError:
            if approve is True:
                for request_user in instance.follow_requests.all():
                    instance.followers.add(request_user)
                    instance.follow_requests.remove(request_user.pk)
            elif approve is False:
                for request_user in instance.follow_requests.all():
                    instance.follow_requests.remove(request_user.pk)
            return instance

        follower = get_object_or_404(instance.follow_requests, pk=request_pk)
        if approve:
            instance.followers.add(follower)
        instance.follow_requests.remove(request_pk)
        return instance

class FollowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "requests")
        extra_kwargs = {"requests": {"required": False}}

class PostCreateSerializer(serializers.ModelSerializer):
    # page = PageSerializer()
    # owner = UserSerializer()
    class Meta:
        model = Post
        fields = ("content", "owner", "reply_to")
        extra_kwargs = {"reply_to": {"required": False}}

    def create(self, validated_data):
        owner = CustomUser.objects.get(pk=validated_data.pop('owner'))
        try:
            reply_to = Post.objects.get(pk=validated_data.pop('reply_to'))
            post = Post.objects.create(reply_to=reply_to, page=self.instance, owner=owner, **validated_data)
            return post
        except KeyError:
            post = Post.objects.create(page=self.instance, owner=owner, **validated_data)
            return post

class PostUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =("content",)

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("page", "content", "reply_to")

class LikedPostListSerializer(serializers.ModelSerializer):
    post = PostListSerializer()
    class Meta:
        model = Reaction
        fields = ("post",)
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("like", "dislike")
        extra_kwargs = {"like": {"required": False}, "dislike": {"required": False}}


    def create_reaction(self, request):
        # reaction = Reaction(post=self.instance, owner=request.user, **self.validated_data)
        reaction = self.instance.reactions.get_or_create(owner=request.user)[0]
        try:
            reaction.like = self.validated_data.pop('like')
        except KeyError:
            reaction.like = reaction.like
        try:
            reaction.dislike = self.validated_data.pop('dislike')
        except KeyError:
            reaction.dislike = reaction.dislike
        reaction.save()
        return reaction.like, reaction.dislike
