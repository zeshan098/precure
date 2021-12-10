from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [  
    path('vendor_inquiry/', views.vendor_inquiry, name='vendor_inquiry'),
    path('vendor_inquiry_form/', views.vendor_inquiry_form, name='vendor_inquiry_form'), 
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('add_vendor/', views.add_edit_vendor, name='add_new_vendor'),  
    path('edit_vendor/<int:vendor_id>/', views.add_edit_vendor, name='edit_vendor'), 
    path('update_vendor_email/<int:id>/', views.update_vendor_email, name='update_vendor_email'), 
    path('update_vendor_category/<int:id>/', views.update_vendor_category, name='update_vendor_category'), 
    path('update_vendor_menufacture/<int:id>/', views.update_vendor_menufacture, name='update_vendor_menufacture'),
    path('update_vendor_model/<int:id>/', views.update_vendor_model, name='update_vendor_model'), 
    path('view_vendor/<int:id>/', views.view_vendor, name='view_vendor'), 
    path('delete_vendor/<int:id>/', views.delete_vendor, name='delete_vendor'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)