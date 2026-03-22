from django.contrib.auth.models import User
from rest_framework import serializers
from auth_app.validators import CustomPasswordValidator
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    def validate_password(self, value):
        if CustomPasswordValidator().validate(value):
            raise serializers.ValidationError(CustomPasswordValidator().get_help_text())
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # To include the username field

    class Meta:
        model = UserProfile
        fields = ['username', 'profile_picture', 'profile_bio']
