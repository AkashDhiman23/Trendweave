from django.urls import path # type: ignore
from . import views  # Import your views
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
urlpatterns = [
      path('', views.index, name='index'),  # Assuming index is your main view in Userpanel
      path('register/', views.register, name='register'),  # Registration route
      path('login/', views.login, name='login'),
      path('checkout/', views.checkout, name='checkout'),
      path('contact/', views.contact, name='contact'),
      path('shop/', views.shop, name='shop'),
      path('cart/', views.shop, name='cart'),
      path('search/', views.search, name='search'),
      path('product/<int:product_id>/', views.product, name='product'),
      path('add-to-cart/<int:product_id>/', views.add_cart, name='add_cart'),
      path('logout/', views.logout, name='logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
