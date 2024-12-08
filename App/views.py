import json
import random
from functools import partial
from symtable import Class

from django.contrib.auth import authenticate
from django.core import cache
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, viewsets
from App.models import UserModel, ImageCarousel, Category, Cake, ClientsSayAboutUs, AddToCart, CakeFlavour, SpongeType, \
    FinishType, Addresses, Personalization
from App.serializers import GetUserSerializer, SignupSerializer, ImageCarouselSerializer, CreateCategorySerializer, \
    CategorySerializer, ContactNumberSerializer, CakeSerializer, ClientsSayAboutUsSerializer, AddToCartSerializer, \
    AddressesSerializer, PersonalizationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Logger.myLogger import Logger
from Services.response import api_response

logger =Logger("View")
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

class PostClientsSayAboutUs(APIView):
    def post(self, request):
        try:
            serializer = ClientsSayAboutUsSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return api_response(status=201, message=str("Category created successfully"), data={})

            return api_response(status=400, message=str(serializer.errors), data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class DeleteClientsSayAboutUsById(APIView):
    def delete(self, request, pk):
        try:
            data=ClientsSayAboutUs.objects.get(pk=pk)
            data.delete()
            return api_response(status=200, message="Deleted successfully", data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e),data={})

class UpdateClientsSayAboutUs(APIView):
    def put(self, request, pk):
        try:
            data = ClientsSayAboutUs.objects.get(pk=pk)
            print("##################################################",data)
            serializer = ClientsSayAboutUsSerializer(data, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse({"message":"updated successfully"},status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Invalid data", "errors": serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)

        except ClientsSayAboutUs.DoesNotExist:
            # If the object doesn't exist, return a 404 error
            return JsonResponse({"message": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

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
        except Exception as e:
            logger.error(str(e))
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCakes(APIView):
    def get(self, request):
        try:
            cakes = Cake.objects.all()

            if not cakes.exists():
                return JsonResponse({'message': 'No cakes found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CakeSerializer(cakes, many=True)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

        except Exception as e:
            logger.error(str(e))
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetAllClientsSayAboutUs(APIView):
    def get(self, request):
        try:
            data = ClientsSayAboutUs.objects.all()
            if not data.exists():
                return api_response(status=404, message=str("No review found"), data={})

            serializer = ClientsSayAboutUsSerializer(data, many=True)
            # if serializer.is_valid():
            return api_response(status=200, message=str("review found successfully"), data=serializer.data)
            # return api_response(status=404, message=str("No review found over here"), data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class PostAddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            # Validate user_model
            user_model = UserModel.objects.get(id=data.get('user_model'))

            # Retrieve or validate cake
            try:
                cake = Cake.objects.get(id=data.get('cake'))
            except Cake.DoesNotExist:
                return JsonResponse({"error": "Cake not found"}, status=status.HTTP_404_NOT_FOUND)

            # Validate and associate cake options
            try:
                cake_flavour = CakeFlavour.objects.get(id=data.get('cake_flavour'))
                sponge_type = SpongeType.objects.get(id=data.get('sponge_type'))
                finish_type = FinishType.objects.get(id=data.get('finish_type'))
            except (CakeFlavour.DoesNotExist, SpongeType.DoesNotExist, FinishType.DoesNotExist) as e:
                return JsonResponse(
                    {"error": f"Invalid cake options provided: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Assign fields to the cake instance
            cake.cake_flavour = cake_flavour
            cake.sponge_type = sponge_type
            cake.finish_type = finish_type

            # Save the cake instance
            cake.save()

            # Create a new AddToCart entry
            cart_item = AddToCart.objects.create(
                user_model=user_model,
                cake=cake,
                quantity=data.get('quantity', 1)
            )

            # Serialize and return the created cart item
            serializer = AddToCartSerializer(cart_item)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        except UserModel.DoesNotExist:
            return JsonResponse({"error": "UserModel not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class GetAddToCartByUser(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            try:
                user = UserModel.objects.get(id=user_id)

            except UserModel.DoesNotExist:
                return JsonResponse({"error": "user not found or has been deleted."},status=status.HTTP_404_NOT_FOUND )

            cart_items = AddToCart.objects.filter(user_model=user, is_deleted=False)
            serializer = AddToCartSerializer(cart_items, many=True )

            # Handle empty queryset
            if not cart_items.exists():
                return JsonResponse({"message": "No cart items found"}, status=status.HTTP_200_OK )

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class DeleteAddToCartById(APIView):
    def delete(self, request, pk):
        try:
            try:
                user = UserModel.objects.get(pk=pk)
            except UserModel.DoesNotExist:
                return JsonResponse({"error": "user not found or has been deleted."},status=status.HTTP_404_NOT_FOUND )

            cart_items = AddToCart.objects.filter(user_model=user, is_deleted=False)

            # Filter the specific cart item based on the id
            cart_item_id = request.data.get("cart_item_id")  # Assuming you pass `cart_item_id` in the request
            cart_item = cart_items.filter(id=cart_item_id).first()

            if not cart_item:
                return JsonResponse(
                    {"error": "Cart item not found or already deleted."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AddToCartSerializer(cart_item, data={"is_deleted": True}, partial=True )  # Allow partial updates ,partial=True

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse({"message":"deleted successfully","data":serializer.data}, status=status.HTTP_204_NO_CONTENT )

            return JsonResponse( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class QuantityHandler(APIView):
    def patch(self, request, user_id):
        try:
            try:
                user = UserModel.objects.get(id=user_id)
            except UserModel.DoesNotExist:
                return JsonResponse({"error": "user not found or has been deleted."}, status=status.HTTP_404_NOT_FOUND)

            cart_items = AddToCart.objects.filter(user_model=user, is_deleted=False)

            # Filter the specific cart item based on the id
            cart_item_id = request.data.get("cart_item_id")  # Assuming you pass `cart_item_id` in the request
            quantity = request.data.get("quantity")  # Assuming you pass `cart_item_id` in the request
            cart_item = cart_items.filter(id=cart_item_id).first()

            if not cart_item:
                return JsonResponse(
                    {"error": "Cart item not found or already deleted."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AddToCartSerializer(cart_item, data={"quantity": quantity}, partial=True )  # Allow partial updates ,partial=True

            if serializer.is_valid():
                serializer.save()  # Save the changes
                return JsonResponse({"message":"quantity updated successfully","data":serializer.data}, status=status.HTTP_204_NO_CONTENT )

            return JsonResponse( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class CreateAddress(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            # Use the serializer only for validation
            serializer = AddressesSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                # Fetch the user model instance based on the provided user_model ID
                user_model = get_object_or_404(UserModel, id=user_id)  # Fetch the UserModel instance

                # Create the address with the foreign key object
                address = Addresses.objects.create(user_model=user_model, **data)

                # Prepare response
                response_data = {
                    "id": address.id,
                    "message": "Address created successfully."
                }
                return JsonResponse(response_data, status=status.HTTP_201_CREATED)
            else:
                # Return validation errors
                return api_response(status=500, message=str(serializer.errors), data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class GetAddress(APIView):
    def get(self, request, user_id):
        try:
            try:
                # Attempt to fetch the user
                user_model = get_object_or_404(UserModel, id=user_id)
            except Exception as e:
                # Handle any unexpected issues gracefully
                return api_response(status=400, message=f"User with id {user_id} not found.", data={})

            all_addresses = Addresses.objects.filter(user_model=user_model)
            serializer = AddressesSerializer(instance=all_addresses, many=True)
            return api_response(status=200, message=str("getting address successfully"), data={})

        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class UpdateAddress(APIView):
    def put(self, request, user_id):
        try:
            user_model = UserModel.objects.get(id=user_id)
            address_id = request.data.get('address_id')
            address = Addresses.objects.get(user_model=user_model, id=address_id)

            # OPTIMIZED CODE FROM CHATgPT

            # # Define a list of fields to update
            # updatable_fields = [
            #     'flat_no', 'street', 'society_name', 'area', 'landmark',
            #     'google_location_url', 'pincode', 'city', 'mobile_number',
            #     'alternate_mobile_number', 'address_type'
            # ]
            #
            # # Update fields dynamically
            # for field in updatable_fields:
            #     if field in request.data:
            #         setattr(address, field, request.data[field])

            address.flat_no=request.data.get('flat_no', address.flat_no)
            address.street=request.data.get('street', address.street)
            address.society_name=request.data.get('society_name', address.society_name)
            address.area=request.data.get('area', address.area)
            address.landmark=request.data.get('landmark', address.landmark)
            address.google_location_url=request.data.get('google_location_url', address.google_location_url)
            address.pincode=request.data.get('pincode', address.pincode)
            address.city=request.data.get('city', address.city)
            address.mobile_number=request.data.get('mobile_number', address.mobile_number)
            address.alternate_mobile_number=request.data.get('alternate_mobile_number', address.alternate_mobile_number)
            address.address_type=request.data.get('address_type', address.address_type)

            address.save()
            # serializer = AddressesSerializer(address, data=request.data, partial=True)
            #
            # if serializer.is_valid():
            #     serializer.save()
            #     return api_response(status=201, message="Updated successfully", data={})

            return api_response(status=201, message="Updated successfully", data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class DeleteAddress(APIView):
    def delete(self, request, user_id):
        try:
            user_model = UserModel.objects.get(id=user_id)
            address_id = request.data.get('address_id')

            address = Addresses.objects.filter(user_model=user_model,id=address_id)
            address.delete()

            return api_response(status=200, message="Deleted successfully", data={})
        except Exception as e:
            logger.error(str(e))
            api_response(status=500, message=str(e), data={})

class AddPersonalization(APIView):
    def post(self, request, user_id):
        try:
            # Log or print the data for debugging
            print("####### add_delivery_date:", request.data.get("add_delivery_date"))

            # Validate serializer
            serializer = PersonalizationSerializer(data=request.data)
            if not serializer.is_valid():
                return api_response(status=status.HTTP_400_BAD_REQUEST, message="Invalid data", data=serializer.errors)

            # Fetch related objects
            user_model = get_object_or_404(UserModel, id=request.data.get("user_model"))
            add_to_cart = get_object_or_404(AddToCart, id=request.data.get("add_to_cart"))

            # Create the Personalization instance
            personalization = Personalization.objects.create(
                user_model=user_model,
                add_to_cart=add_to_cart,
                add_delivery_date=request.data.get("add_delivery_date"),
                add_delivery_time=request.data.get("add_delivery_time"),
                personal_message=request.data.get("personal_message"),
                name=request.data.get("name"),
                number=request.data.get("number"),
            )

            # Return success response
            response_data = PersonalizationSerializer(personalization).data
            return api_response(status=status.HTTP_201_CREATED, message="Personalization created successfully", data=response_data)

        except Exception as e:
            # Log the error and return server error response
            logger.error(f"Error while creating personalization: {str(e)}")
            return api_response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="An error occurred while creating personalization", data={})


