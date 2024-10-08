from django.contrib import admin
from django.urls import path, include

from admin_panel import views

urlpatterns = [
       path('', views.index, name='dashboard'),
       path('admin_panel/', include('admin_panel.urls')), 
    
]