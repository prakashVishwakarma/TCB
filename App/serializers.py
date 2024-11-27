from rest_framework import serializers
from .models import UserModel, ImageCarousel, Category, Cake, ClientsSayAboutUs, CakeCareGuidelines, DeliverySpecifics, \
    KindlyNote
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import (
    Cake, Category, CakeImage, CakeFlavour,
    SpongeType, FinishType, ProductDescription
)

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
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    # password = serializers.CharField(source='user.password',read_only=True)

    class Meta:
        model = UserModel
        fields = ['id','username', 'email', 'mobile_number']


class ImageCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCarousel
        fields =  ['id', 'cake_image']

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cake_image','category_name','is_deleted']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'cake_image', 'category_name']

class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['mobile_number']

# class CakeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cake
#         fields = '__all__'

class ClientsSayAboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientsSayAboutUs
        fields = '__all__'


# Nested Serializers for related models
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'cake_image']

class CakeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeImage
        fields = ['id', 'cake_image']

class CakeFlavourSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeFlavour
        fields = ['id', 'cake_flavour']

class SpongeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpongeType
        fields = ['id', 'sponge_type']

class FinishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishType
        fields = ['id', 'finish_type']

class CakeCareGuidelinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCareGuidelines
        fields = ['id', 'cake_care_guidelines']


class DeliverySpecificsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverySpecifics
        fields = ['id', 'delivery_specifics']


class KindlyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindlyNote
        fields = ['id', 'kindly_note']

class ProductDescriptionSerializer(serializers.ModelSerializer):
    cake_care_guidelines = CakeCareGuidelinesSerializer(read_only=True)
    delivery_specifics = DeliverySpecificsSerializer(read_only=True)
    kindly_note = KindlyNoteSerializer(read_only=True)
    class Meta:
        model = ProductDescription
        fields = ['id', 'kindly_note', 'delivery_specifics', 'cake_care_guidelines']

# Main Cake Serializer with nested relationships
class CakeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    cake_image = CakeImageSerializer(read_only=True)
    cake_flavour = CakeFlavourSerializer(read_only=True)
    sponge_type = SpongeTypeSerializer(read_only=True)
    finish_type = FinishTypeSerializer(read_only=True)
    product_pescription = ProductDescriptionSerializer(read_only=True)

    class Meta:
        model = Cake
        fields = '__all__'