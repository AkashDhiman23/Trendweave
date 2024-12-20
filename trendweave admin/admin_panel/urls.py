from django.urls import path # type: ignore
from . import views
from django.conf import settings# type: ignore
from django.conf.urls.static import static# type: ignore


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
    path('edit_product/', views.edit_product, name='edit_product'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('subcategory/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('edit-category/', views.edit_category, name='edit_category'),
    path('order_view/', views.order_view, name='order_view'),
    path('edit-subcategory/', views.edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/', views.delete_subcategory, name='delete_subcategory'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('user_view/', views.user_view, name='user_view'),
     path('update-order-status/', views.update_order_status, name='update_order_status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)