from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status

from App.models import CustomToken
from App.serializers import UserSerializer
from rest_framework.authtoken.models import Token


# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = CustomToken.objects.get_or_create(user=user)
            return JsonResponse({"message": "User registered successfully!","token": token.key,"isCeated":created }, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)