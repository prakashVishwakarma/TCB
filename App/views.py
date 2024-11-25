import json
import random
from functools import partial

from django.contrib.auth import authenticate
from django.core import cache
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status, viewsets
from App.models import UserModel, ImageCarousel, Category, Cake
from App.serializers import GetUserSerializer, SignupSerializer, ImageCarouselSerializer, CreateCategorySerializer, \
    CategorySerializer, ContactNumberSerializer, CakeSerializer
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

# class ForgotPasswordAPIView(APIView):
#     """
#     API to request a password reset using a contact number.
#     """
#
#     def post(self, request):
#         try:
#
#             contact_number = request.data.get('contact_number')
#             data = json.loads(contact_number)
#             if not contact_number:
#                 return JsonResponse({"error": "Contact number is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#             try:
#                 user = UserModel.objects.get(mobile_number=contact_number)
#             except UserModel.DoesNotExist:
#                 return JsonResponse({"error": "No user with this contact number exists."}, status=status.HTTP_404_NOT_FOUND)
#
#             serializer = ContactNumberSerializer(data={"data":data})
#             if serializer.is_valid():
#
#                 # Generate a 6-digit OTP
#                 otp = random.randint(100000, 999999)
#                 print('####################################',otp,contact_number, serializer.data)
#
#                 # Store OTP in cache with a timeout (e.g., 5 minutes)
#                 cache.set(f"reset_password_otp_{contact_number}", otp, timeout=300)
#
#                 # Simulate sending OTP (replace this with an SMS service)
#                 print(f"OTP for {contact_number}: {otp}")
#
#                 return JsonResponse(
#                     {"message": "OTP sent to the provided contact number."},
#                     status=status.HTTP_200_OK
#                 )
#             else:
#                 return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#
#             return JsonResponse(
#                 {"message": e},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class ResetPasswordWithOTPAPIView(APIView):
#     """
#     API to reset the password after verifying the OTP.
#     """
#
#     def post(self, request):
#         contact_number = request.data.get('contact_number')
#         otp = request.data.get('otp')
#         new_password = request.data.get('password')
#
#         if not contact_number or not otp or not new_password:
#             return JsonResponse(
#                 {"error": "Contact number, OTP, and new password are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # Retrieve OTP from cache
#         cached_otp = cache.get(f"reset_password_otp_{contact_number}")
#
#         if not cached_otp or str(cached_otp) != str(otp):
#             return JsonResponse({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             user = UserModel.objects.get(usermodel__mobile_number=contact_number)
#         except UserModel.DoesNotExist:
#             return JsonResponse({"error": "No user with this contact number exists."}, status=status.HTTP_404_NOT_FOUND)
#
#         # Set new password
#         user.set_password(new_password)
#         user.save()
#
#         # Invalidate the OTP
#         cache.delete(f"reset_password_otp_{contact_number}")
#
#         return JsonResponse({"message": "Password reset successful."}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's token and delete it to log them out
            token = Token.objects.get(user=request.user)
            token.delete()
            return JsonResponse({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return JsonResponse({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)


class GetCakesByCategory(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            # Check if the category exists and is not marked as deleted
            category = Category.objects.get(pk=pk, is_deleted=False)
        except Category.DoesNotExist:
            return JsonResponse(
                {"error": "Category not found or has been deleted."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch cakes under the category
        cakes = Cake.objects.filter(category=category)
        print("#######",cakes)
        # Handle empty queryset
        if not cakes.exists():
            return JsonResponse(
                {"message": "No cakes found for this category."},
                status=status.HTTP_200_OK
            )

        serializer = CakeSerializer(cakes, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

class CreateCakeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = CakeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse(serializer.errors,str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)