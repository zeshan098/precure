from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), 
    path('buyer_inquiry/', views.buyer_inquiry, name='buyer_inquiry'),
    path('vendor_inquiry/', views.vendor_inquiry, name='vendor_inquiry'),
]
