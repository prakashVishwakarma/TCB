from django.contrib import admin
from App.models import UserModel, ImageCarousel, Category, CakeImage, CakeFlavour, SpongeType, FinishType, KindlyNote, \
    DeliverySpecifics, CakeCareGuidelines, ProductDescription, Cake, CakeCategory, TrendingNow, OurBestsellers, \
    ExploreMoreWithUs, ClientsSayAboutUs, AddToCart, Addresses, CakeOrderHistory, Personalization


# Register your models here.
#  old way
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id','full_name','email','password','mobile_number']
#
# admin.site.register(UserModel, UserAdmin)

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'mobile_number']


@admin.register(ImageCarousel)
class ImageCarouselAdmin(admin.ModelAdmin):
    list_display = ['id','cake_image','is_deleted']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cake_image','category_name','is_deleted']

@admin.register(CakeImage)
class CakeImageAdmin(admin.ModelAdmin):
    list_display = ['id','cake_image']

@admin.register(CakeFlavour)
class CakeFlavourAdmin(admin.ModelAdmin):
    list_display = ['id','cake_flavour']

@admin.register(SpongeType)
class SpongeTypeAdmin(admin.ModelAdmin):
    list_display = ['id','sponge_type']

@admin.register(FinishType)
class FinishTypeAdmin(admin.ModelAdmin):
    list_display = ['id','finish_type']

@admin.register(KindlyNote)
class FinishTypeAdmin(admin.ModelAdmin):
    list_display = ['id','kindly_note']

@admin.register(DeliverySpecifics)
class DeliverySpecificsAdmin(admin.ModelAdmin):
    list_display = ['id','delivery_specifics']

@admin.register(CakeCareGuidelines)
class CakeCareGuidelinesAdmin(admin.ModelAdmin):
    list_display = ['id','cake_care_guidelines']

@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['id','kindly_note','delivery_specifics','cake_care_guidelines']

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['id','category','cake_image','cake_flavour','sponge_type','finish_type','product_pescription','discount','name','price','weight','earliest_delivery','unique_quality','CakeMessage']

@admin.register(CakeCategory)
class CakeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cake_image','category_name']

@admin.register(TrendingNow)
class TrendingNowAdmin(admin.ModelAdmin):
    list_display = ['id','price','cake_name','cake_image']

@admin.register(OurBestsellers)
class OurBestsellersAdmin(admin.ModelAdmin):
    list_display = ['id','cake_name','cake_image']

@admin.register(ExploreMoreWithUs)
class ExploreMoreWithUsAdmin(admin.ModelAdmin):
    list_display = ['id','price','cake_name','cake_image']

@admin.register(ClientsSayAboutUs)
class ClientsSayAboutUsAdmin(admin.ModelAdmin):
    list_display = ['id','client_name','client_says']

@admin.register(AddToCart)
class AddToCartAdmin(admin.ModelAdmin):
    list_display = ['id','user_model','cake','quantity', 'is_deleted']

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ['id','user_model','flat_no','street','society_name','area','landmark','google_location_url','pincode','city','mobile_number','alternate_mobile_number','address_type']

# @admin.register(CakeOrderHistory)
# class CakeOrderHistoryAdmin(admin.ModelAdmin):
#     list_display = ['id','user_model','order_placed','total','recipient_name','order_id','status']

@admin.register(Personalization)
class PersonalizationAdmin(admin.ModelAdmin):
    list_display = ['id','user_model','add_to_cart','add_delivery_date','add_delivery_time','personal_message','name','number']

@admin.register(CakeOrderHistory)
class CakeOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','user_model','category','cake_image','cake_flavour','sponge_type','finish_type','product_pescription','discount','name','price','weight','earliest_delivery','unique_quality','cake_message','quantity','ordered_on','order_id','status','shipping_address','payment_method','payment_id','razorpay_signature']
