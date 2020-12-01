from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import re

from todo.models import Task, Member
from users.models import User
from users.utils import generate_access_token, generate_refresh_token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone', 'full_name']

    def validate(self, attrs):
        # email = attrs.get('email', '')
        username = attrs.get('username', '')
        phone = attrs.get('phone', '')
        # full_name = attrs.get('full_name', '')
        regex = r'^\+?\d{9,12}$'
        x = re.search(regex, phone)
        if not username.isalnum():
            raise serializers.ValidationError({'username': 'The username should only contain alphanumeric characters'})
        if not x:
            raise serializers.ValidationError({'phone': 'Enter a valid phone number'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=255)
    password = serializers.CharField(
        max_length=68, write_only=True)
    email = serializers.EmailField(
        max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(username=username)
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())


    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'full_name', 'phone', 'task']
        read_only_fields = ('email', 'username', 'task')

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        if validated_data.get('phone'):
            phone = validated_data.get('phone')
            # print(phone)
            regex = r'^\+?\d{9,12}$'
            x = re.search(regex, phone)
            if not x:
                raise serializers.ValidationError({'phone': 'Enter a valid phone number'})
            instance.phone = phone
        instance.save()
        user = self.context.get('request').user
        print(user)
        return instance
