from rest_framework import serializers

from apps.user.models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):
    verify_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def save(self, *args, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        # response = Response()
        # refresh_token = generate_refresh_token(user)
        # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        # response.data = {
        #     'access_token': generate_access_token(user),
        # }
        return user

    def validate(self, data):
        password = data['password']
        verify_password = data['verify_password']

        if password != verify_password:
            raise serializers.ValidationError({password: "Passwords are not the same"})

        return data

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password", "verify_password")


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        if email is None:
            raise serializers.ValidationError({email: "An email address is required to log in"})

        if password is None:
            raise serializers.ValidationError({password: "An password address is required to log in"})

        user = CustomUser.objects.filter(email=email).first()

        if not user.check_password(password):
            raise serializers.ValidationError('wrong password')

        if user is None:
            raise serializers.ValidationError("The user with this password and email are not exist")

        if not user.is_active:
            raise serializers.ValidationError("The user has been deactivate")

        return data

class CustomUserBlockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("is_blocked",)
