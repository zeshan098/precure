from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'), 
    path('order_list/', views.order_list, name='order_list'),  
    # path('GeneratePdf/', views.GeneratePdf, name='GeneratePdf'), 

]