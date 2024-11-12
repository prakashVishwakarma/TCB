from rest_framework import serializers
from .models import UserModel
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['full_name', 'email', 'password', 'mobile_number']

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_mobile_number(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("Mobile number should contain only digits.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash the password
        return super().create(validated_data)
