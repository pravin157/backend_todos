"""
Serializers for authentication and task management.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Todo


class UserSerializer(serializers.ModelSerializer):
    """Serializer for public user profile details."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering new users with validation."""

    password = serializers.CharField(write_only=True, required=True, min_length=6)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    """Serializer for user credentials validation."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo tasks with user-scoped protection."""

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
