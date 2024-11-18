from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    mobile_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email', 'mobile_number')

    def validate_username(self, value):
        # Check if the username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError( {
                "message": "This username is already taken. Please choose a different one."
            })

        # Add any additional username validation here
        # For example, restrict certain characters or minimum length
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        UserModel.objects.create(
            user=user,
            mobile_number=validated_data.get('mobile_number', '')
        )
        return user

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['full_name', 'email', 'password', 'mobile_number']