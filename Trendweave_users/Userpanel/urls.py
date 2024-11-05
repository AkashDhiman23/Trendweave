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
   
   
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
