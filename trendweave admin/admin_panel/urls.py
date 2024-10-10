from django.urls import path # type: ignore
from . import views  # Import your views

urlpatterns = [
    path('', views.index, name='index'),  
    path('register/', views.registration_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
    path('profile/', views.profile_view, name='profile'),
    path('category/', views.category_view, name='category'),
]