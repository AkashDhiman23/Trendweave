from django.urls import path # type: ignore
from . import views  # Import your views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('', views.index, name='index'),  # Assuming index is your main view in Userpanel
    path('register/', views.register, name='register'),  # Registration route
    path('login/', views.login, name='login'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search, name='search'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('logout/', views.logout, name='logout'),

    path('wish/', views.wish, name='wish'),
    path('add-cart/<int:product_id>/',views.add_cart, name='add_cart'),
    path('profile/', views.profile, name='profile'),
    path('wish/add/<int:pid>/', views.add_wish, name='add_wish'),
    path('filter-products/', views.filter_products, name='filter_products'),
    path('home/', views.home, name='home'),
    path('plus-cart/<int:cart_item_id>/',views.plus_cart,name='plus_cart'),
    path('minus-cart/<int:cart_item_id>/',views.minus_cart,name='minus_cart'),
    path('delete-cart/<int:cart_item_id>/',views.delete_cart,name='delete_cart'),
    path('myorders/',views.myorders,name='myorders'),
    path('confirmorder/<int:order_id>',views.confirmorder,name='confirmorder'),
    path('payment/stripe/<int:oid>/', views.PaymentView.as_view(), name='payment'),
    path('order-cancel/<int:order_id>',views.order_cancel,name='order_cancel'),
 
    path('shop_o/', views.shop_o, name='shop_o'),
    path('password_reset/', views.password_reset, name='password_reset'),  # Step 1: Email input
   
    path('password_reset/verify_and_reset/', views.verify_and_reset, name='verify_and_reset'),  # Step 2: OTP verification + reset password
]
   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
