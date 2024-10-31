from django.urls import path # type: ignore
from . import views  # Import your views
from django.conf import settings# type: ignore
from django.conf.urls.static import static# type: ignore

urlpatterns = [
     path('', views.index, name='index'),  # Assuming index is your main view in Userpanel
    path('register/', views.register, name='register'),  # Registration route
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
     path('contact/', views.contact, name='contact'),
      path('shop/', views.shop, name='shop'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)