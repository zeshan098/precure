from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [  
    path('buyer_inquiry/', views.buyer_inquiry, name='buyer_inquiry'), 
    path('buyer_category/', views.buyer_category, name='buyer_category'), 
    path('buyer_menufacture/', views.buyer_menufacture, name='buyer_menufacture'),
    path('buyer_model/', views.buyer_model, name='buyer_model'),
    path('buyer_inquiry_form/', views.buyer_inquiry_form, name='buyer_inquiry_form'), 
    path('buyer_list/', views.buyer_list, name='buyer_list'),
    path('add_buyer/', views.add_edit_buyer, name='add_new_buyer'), 
    path('edit_buyer/<int:buyer_id>/', views.add_edit_buyer, name='edit_buyer'),
    path('update_buyer_email/<int:id>/', views.update_buyer_email, name='update_buyer_email'),
    path('update_buyer_category/<int:id>/', views.update_buyer_category, name='update_buyer_category'), 
    path('update_buyer_menufacture/<int:id>/', views.update_buyer_menufacture, name='update_buyer_menufacture'),
    path('update_buyer_model/<int:id>/', views.update_buyer_model, name='update_buyer_model'), 
    path('view_buyer/<int:id>/', views.view_buyer, name='view_buyer'),  
    path('delete_buyer/<int:id>/', views.delete_buyer, name='delete_buyer'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)