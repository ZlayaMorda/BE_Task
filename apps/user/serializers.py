from rest_framework import serializers
from apps.user.models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    def save(self, *args, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        password = data['password']
        password2 = data['password2']

        if password != password2:
            raise serializers.ValidationError({password: "Passwords are not the same"})

        return data

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password", "password2"]
