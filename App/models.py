from django.db import models
# from django.contrib.auth.hashers import make_password

# Create your models here.
class ImageCarousel(models.Model):
    cake_image = models.URLField(max_length=500)

# one-to-many relationship - start

class Category(models.Model):
    cake_image = models.URLField(max_length=500)
    category_name = models.CharField(max_length=255)
    
class CakeImage(models.Model):
    cake_image = models.URLField(max_length=500)

class CakeFlavour(models.Model):
    cake_flavour = models.CharField(max_length=500)

class SpongeType(models.Model):
    sponge_type = models.CharField(max_length=500)

class FinishType(models.Model):
    finish_type = models.CharField(max_length=500)

# _______________________________________
class KindlyNote(models.Model):
    kindly_note = models.CharField(max_length=255)

class DeliverySpecifics(models.Model):
    delivery_specifics = models.CharField(max_length=255)

class CakeCareGuidelines(models.Model):
    cake_care_guidelines = models.CharField(max_length=255)

class ProductDescription(models.Model):
    kindly_note = models.ForeignKey(KindlyNote, on_delete=models.CASCADE)
    delivery_specifics = models.ForeignKey(DeliverySpecifics, on_delete=models.CASCADE)
    cake_care_guidelines = models.ForeignKey(CakeCareGuidelines, on_delete=models.CASCADE)

# _______________________________________

class Cake(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cake_image = models.ForeignKey(CakeImage, on_delete=models.CASCADE)
    cake_flavour = models.ForeignKey(CakeFlavour, on_delete=models.CASCADE)
    sponge_type = models.ForeignKey(SpongeType, on_delete=models.CASCADE)
    finish_type = models.ForeignKey(FinishType, on_delete=models.CASCADE)
    product_pescription = models.ForeignKey(ProductDescription, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    earliest_delivery = models.CharField(max_length=255)
    unique_quality = models.CharField(max_length=255)
    CakeMessage = models.CharField(max_length=255)

# one-to-many relationship - end

class CakeCategory(models.Model):
    cake_image = models.URLField(max_length=500)
    category_name = models.CharField(max_length=255)

class TrendingNow(models.Model):
    cake_image = models.URLField(max_length=500)
    cake_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OurBestsellers(models.Model):
    cake_image = models.URLField(max_length=500)
    cake_name = models.CharField(max_length=255)

class ExploreMoreWithUs(models.Model):
    cake_image = models.URLField(max_length=500)
    cake_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ClientsSayAboutUs(models.Model):
    client_says = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)

class UserModel(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     # Hash the password before saving
    #     self.password = make_password(self.password)
    #     super(UserModel, self).save(*args, **kwargs)
    
class AddToCart(models.Model):
    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

class Addresses(models.Model):
    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    society_name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    landmark  = models.CharField(max_length=255)
    google_location_url = models.URLField(max_length=255)
    pincode = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address_type = models.CharField(max_length=255)
#
# class CakeOrderHistory(models.Model):
#     user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     order_placed = models.CharField(max_length=255)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     recipient_name = models.CharField(max_length=255)
#     order_id = models.DecimalField(max_digits=100, decimal_places=2)
#     status  = models.CharField(max_length=255)

class Personalization(models.Model):
    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    add_to_cart = models.ForeignKey(AddToCart, on_delete=models.CASCADE)
    add_delivery_date = models.DecimalField(max_digits=10, decimal_places=2)
    add_delivery_time = models.DecimalField(max_digits=10, decimal_places=2)
    personal_message = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    number = models.DecimalField(max_digits=15, decimal_places=2)

class CakeOrderHistory(models.Model):
    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cake_image = models.ForeignKey(CakeImage, on_delete=models.CASCADE)
    cake_flavour = models.ForeignKey(CakeFlavour, on_delete=models.CASCADE)
    sponge_type = models.ForeignKey(SpongeType, on_delete=models.CASCADE)
    finish_type = models.ForeignKey(FinishType, on_delete=models.CASCADE)
    product_pescription = models.ForeignKey(ProductDescription, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    earliest_delivery = models.CharField(max_length=255)
    unique_quality = models.CharField(max_length=255)
    cake_message = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_on = models.CharField(max_length=255)
    order_id = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
