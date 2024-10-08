from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.index, name='index'),  
    path('register/', views.registration_view, name='register'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('logout/', views.logout_view, name='logout'),  
]