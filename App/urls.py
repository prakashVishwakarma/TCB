"""
URL configuration for TCB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from App.views import GetAllUsers, SignupView, ImageCarouselViewSet, ImageCarouselListView, SoftDeleteImageCarousel, \
    ImageCarouselPatchView, CreateCategory, GetAllCategory, UpdateCategory, DeleteCategory, UserLoginView, \
    LogoutView, GetCakesByCategory, CreateCakeView, GetAllCakes, PostClientsSayAboutUs, GetAllClientsSayAboutUs, \
    DeleteClientsSayAboutUsById, UpdateClientsSayAboutUs, PostAddToCart, GetAddToCartByUser, DeleteAddToCartById, \
    QuantityHandler, CreateAddress, GetAddress, UpdateAddress, DeleteAddress, AddPersonalization, create_razorpay_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='SignUpView'),
    path('getallusers/', GetAllUsers.as_view(), name='GetAllUsers'),
    path('postcaroucel/', ImageCarouselViewSet.as_view({'post': 'create'}), name='ImageCarouselViewSet'),
    path('getallcaroucel/', ImageCarouselListView.as_view(), name='ImageCarouselListView'),
    path('image-carousel/delete/<int:pk>/', SoftDeleteImageCarousel.as_view(), name='soft-delete-image-carousel'),
    path('image-carousel/update/<int:pk>/', ImageCarouselPatchView.as_view(), name='ImageCarouselPatchViewel'),
    path('create-category/', CreateCategory.as_view(), name='CreateCategory'),
    path('get-all-category/', GetAllCategory.as_view(), name='GetAllCategory'),
    path('update-category/<int:pk>/', UpdateCategory.as_view(), name='UpdateCategory'),
    path('delete-category/<int:pk>/', DeleteCategory.as_view(), name='DeleteCategory'),
    path('login/', UserLoginView.as_view(), name='UserLoginView'),
    # path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    # path('reset-password/', ResetPasswordWithOTPAPIView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-cake-by-category-id/<int:pk>/', GetCakesByCategory.as_view(), name='GetCakesByCategory'),
    path('cakes-create/', CreateCakeView.as_view(), name='create-cake'),
    path('get-all-cakes/', GetAllCakes.as_view(), name='GetAllCakes'),
    path('client-say-about-us/', PostClientsSayAboutUs.as_view(), name='PostClientsSayAboutUs'),
    path('get-all-client-say-about-us/', GetAllClientsSayAboutUs.as_view(), name='GetAllClientsSayAboutUs'),
    path('delete-client-say-about-us/<int:pk>/', DeleteClientsSayAboutUsById.as_view(), name='DeleteClientsSayAboutUsById'),
    path('update-client-say-about-us/<int:pk>/', UpdateClientsSayAboutUs.as_view(), name='UpdateClientsSayAboutUs'),
    path('add-to-cart/', PostAddToCart.as_view(), name='PostAddToCart'),
    path('get-add-to-cart/<int:user_id>/', GetAddToCartByUser.as_view(), name='GetAddToCartByUser'),
    path('delete-add-to-cart/<int:pk>/', DeleteAddToCartById.as_view(), name='DeleteAddToCartById'),
    path('update-quantity-of-add-to-cart/<int:user_id>/', QuantityHandler.as_view(), name='QuantityHandler'),
    path('create-address/<int:user_id>/', CreateAddress.as_view(), name='QuantityHandler'),
    path('get-address/<int:user_id>/', GetAddress.as_view(), name='GetAddress'),
    path('update-address/<int:user_id>/', UpdateAddress.as_view(), name='UpdateAddress'),
    path('delete-address/<int:user_id>/', DeleteAddress.as_view(), name='DeleteAddress'),
    path('add-persionalization/<int:user_id>/', AddPersonalization.as_view(), name='AddPersonalization'),
    path('create-razorpay-order/', create_razorpay_order, name='create-razorpay-order'),
]
