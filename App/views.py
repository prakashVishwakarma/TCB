from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status

from App.models import CustomToken, UserModel
from App.serializers import GetUserSerializer, SignupSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsers(generics.ListAPIView):
        queryset = UserModel.objects.all()
        permission_classes = [IsAuthenticated]

        # Do not use serializer_class here
        def get(self, request, *args, **kwargs):
            # Manually instantiate the serializer with queryset data
            serializer = GetUserSerializer(self.get_queryset(), many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)