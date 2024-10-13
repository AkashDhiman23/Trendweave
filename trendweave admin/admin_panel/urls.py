from django.urls import path # type: ignore
from . import views  # Import your views

urlpatterns = [
    path('', views.index, name='index'),  
    path('register/', views.registration_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
    path('profile/', views.profile_view, name='profile'),
    path('category/', views.category_view, name='category'),
    path('subcategory_view/' , views.subcategory_view , name='subcategory_view'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('product/', views.product, name='product'),
    path('add_product/', views.add_product, name='add_product'),
]