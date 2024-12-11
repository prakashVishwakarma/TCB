from rest_framework import serializers
from .models import UserModel, ImageCarousel, Category, Cake, ClientsSayAboutUs, CakeCareGuidelines, DeliverySpecifics, \
    KindlyNote, AddToCart, Addresses, Personalization, CakeOrderHistory
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
        fields = ['id', 'cake_image', 'category_name', 'is_deleted']

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

class KindlyNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindlyNote
        fields = ['id', 'kindly_note']

class DeliverySpecificsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverySpecifics
        fields = ['id', 'delivery_specifics']

class CakeCareGuidelinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CakeCareGuidelines
        fields = ['id', 'cake_care_guidelines']

class ProductDescriptionSerializer(serializers.ModelSerializer):
    kindly_note = KindlyNoteSerializer()
    delivery_specifics = DeliverySpecificsSerializer()
    cake_care_guidelines = CakeCareGuidelinesSerializer()

    class Meta:
        model = ProductDescription
        fields = ['id', 'kindly_note', 'delivery_specifics', 'cake_care_guidelines']

    def create(self, validated_data):
        kindly_note_data = validated_data.pop('kindly_note')
        delivery_specifics_data = validated_data.pop('delivery_specifics')
        cake_care_guidelines_data = validated_data.pop('cake_care_guidelines')

        kindly_note = KindlyNote.objects.create(**kindly_note_data)
        delivery_specifics = DeliverySpecifics.objects.create(**delivery_specifics_data)
        cake_care_guidelines = CakeCareGuidelines.objects.create(**cake_care_guidelines_data)

        return ProductDescription.objects.create(
            kindly_note=kindly_note,
            delivery_specifics=delivery_specifics,
            cake_care_guidelines=cake_care_guidelines,
            **validated_data
        )


class CakeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    cake_image = CakeImageSerializer()
    cake_flavour = CakeFlavourSerializer()
    sponge_type = SpongeTypeSerializer()
    finish_type = FinishTypeSerializer()
    product_pescription = ProductDescriptionSerializer()

    class Meta:
        model = Cake
        fields = [
            'id', 'category', 'cake_image', 'cake_flavour', 'sponge_type', 'finish_type',
            'product_pescription', 'discount', 'name', 'price', 'weight',
            'earliest_delivery', 'unique_quality', 'CakeMessage'
        ]

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        cake_image_data = validated_data.pop('cake_image')
        cake_flavour_data = validated_data.pop('cake_flavour')
        sponge_type_data = validated_data.pop('sponge_type')
        finish_type_data = validated_data.pop('finish_type')
        product_pescription_data = validated_data.pop('product_pescription')

        category = Category.objects.create(**category_data)
        cake_image = CakeImage.objects.create(**cake_image_data)
        cake_flavour = CakeFlavour.objects.create(**cake_flavour_data)
        sponge_type = SpongeType.objects.create(**sponge_type_data)
        finish_type = FinishType.objects.create(**finish_type_data)
        product_pescription = ProductDescriptionSerializer().create(product_pescription_data)

        return Cake.objects.create(
            category=category,
            cake_image=cake_image,
            cake_flavour=cake_flavour,
            sponge_type=sponge_type,
            finish_type=finish_type,
            product_pescription=product_pescription,
            **validated_data
        )

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializer for UserModel
class UserModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested User serializer

    class Meta:
        model = UserModel
        fields = ['user', 'mobile_number']

class AddToCartSerializer(serializers.ModelSerializer):
    cake = CakeSerializer(read_only=True)
    user_model = UserModelSerializer(read_only=True)

    class Meta:
        model = AddToCart
        fields = ['quantity','cake','user_model','is_deleted']

class AddressesSerializer(serializers.ModelSerializer):
    user_model = UserModelSerializer(read_only=True)

    class Meta:
        model = Addresses
        fields = ['id','user_model','flat_no','street','society_name','area','landmark','google_location_url','pincode','city','mobile_number','alternate_mobile_number','address_type']

class PersonalizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personalization
        fields = ['id','user_model','add_to_cart','add_delivery_date','add_delivery_time','personal_message','name','number']

class CreateOrderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CakeOrderHistory
        fields = '__all__'
