from django.urls import path # type: ignore
from . import views  # Import your views

urlpatterns = [
     path('', views.index, name='index'),  # Assuming index is your main view in Userpanel
    path('register/', views.register, name='register'),  # Registration route
    path('verify-otp/<str:username>/', views.verify_otp, name='verify_otp'), 
]