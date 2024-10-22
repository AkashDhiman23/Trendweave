from django.contrib import admin# type: ignore
from django.urls import path, include# type: ignore

from admin_panel import views

urlpatterns = [
       path('', views.index, name='dashboard'),
       path('admin_panel/', include('admin_panel.urls')), 
    
]