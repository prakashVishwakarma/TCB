from functools import partial

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status, viewsets
from App.models import UserModel, ImageCarousel, Category
from App.serializers import GetUserSerializer, SignupSerializer, ImageCarouselSerializer, CreateCategorySerializer, \
    CategorySerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#####################################   ADMIN   #####################################

class ImageCarouselPatchView(APIView):
    def patch(self, request, pk):
        try:
            # Fetch the object by primary key (id)
            image_carousel = ImageCarousel.objects.get(pk=pk)

            # Use the serializer to validate and update the data
            serializer = ImageCarouselSerializer(
                image_carousel,
                data=request.data,
                partial=True  # Allow partial updates
            )
            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse(
                    serializer.data,  # Return the updated object
                    status=status.HTTP_200_OK
                )
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except ImageCarousel.DoesNotExist:
            return JsonResponse(
                {"error": "ImageCarousel not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class SoftDeleteImageCarousel(APIView):
    def delete(self, request, pk):
        try:

            # Fetch the object by primary key (id)
            image_carousel = ImageCarousel.objects.get(pk=pk)

            # Check if the object is already soft-deleted
            if image_carousel.is_deleted:
                return JsonResponse(
                    {"error": "ImageCarousel is already deleted."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ImageCarouselSerializer(
                image_carousel,
                data={"is_deleted": True},
                partial=True  # Allow partial updates
            )

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse(
                    {"message":"deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return JsonResponse(
                {"error": e},
                status=status.HTTP_404_NOT_FOUND
            )

class CreateCategory(APIView):
    def post(self,request):
        try:
            serializer = CreateCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message":"Category created successfully"},status =status.HTTP_201_CREATED )

            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            JsonResponse(e, status=status.HTTP_404_NOT_FOUND)

class GetAllUsers(generics.ListAPIView):
        queryset = UserModel.objects.all()
        permission_classes = [IsAuthenticated]

        # Do not use serializer_class here
        def get(self, request, *args, **kwargs):
            # Manually instantiate the serializer with queryset data
            serializer = GetUserSerializer(self.get_queryset(), many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False , content_type='application/json')

class ImageCarouselViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ImageCarouselSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 'ok',
                'message': 'Image carousel entry created successfully.',
            }
            return JsonResponse(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'status': 'fail',
                'message': 'Please provide a valid cake image URL.'
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

#####################################   FRONTEND   #####################################

class SignupView(APIView):
    def post(self, request):
        try:
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # Save new user if data is valid

                # Generate token for the new user
                token, created = Token.objects.get_or_create(user=user)

                return JsonResponse({
                    "message": "User created successfully",
                    "token": token.key
                }, status=status.HTTP_201_CREATED)

            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({"error": "Something went wrong. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageCarouselListView(APIView):
    def get(self, request):
        images = ImageCarousel.objects.filter(is_deleted = False)  # Retrieve all image carousel entries
        serializer = ImageCarouselSerializer(images, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

class GetAllCategory(APIView):
    def get(self, request):
        try:
            # Fetch all Category objects
            categories = Category.objects.filter(is_deleted=False)

            # Serialize the data
            serializer = CategorySerializer(categories, many=True)

            # Validate serialization (typically not necessary for GET)
            if serializer.data:  # Ensure serialized data is not empty
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse(
                    {"error": "No categories found or serialization failed."},
                    status=status.HTTP_204_NO_CONTENT
                )

        except Exception as e:
            return JsonResponse(
                {"error": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateCategory(APIView):
    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CreateCategorySerializer(category, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse({"message":"updated successfully"},status=status.HTTP_200_OK)

            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

        except Exception as e:
            return JsonResponse(
                {"error": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteCategory(APIView):
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            print('category',category.is_deleted)
            # Check if the object is already soft-deleted
            if category.is_deleted:
                return JsonResponse(
                    {"error": "category is already deleted."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CreateCategorySerializer(
                category,
                data={"is_deleted": True},
                partial=True  # Allow partial updates
            )

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse(
                    {"message":"deleted successfully","data":serializer.data},
                    status=status.HTTP_204_NO_CONTENT
                )

            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return JsonResponse(
                {"error": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserLoginView(APIView):
    """
    API for logging in a user.
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse(
                {"token": token.key, "message": "Login successful."},
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )
