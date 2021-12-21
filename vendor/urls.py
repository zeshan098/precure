from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [  
    path('vendor_inquiry/', views.vendor_inquiry, name='vendor_inquiry'),
    path('get_category_tag/', views.get_category_tag, name='get_category_tag'), 
    path('get_menufacture_tag/', views.get_menufacture_tag, name='get_menufacture_tag'),
    path('get_model_tag/', views.get_model_tag, name='get_model_tag'),
    path('vendor_inquiry_form/', views.vendor_inquiry_form, name='vendor_inquiry_form'), 
    path('vendor_list/', views.vendor_list, name='vendor_list'),
    path('add_vendor/', views.add_edit_vendor, name='add_new_vendor'),  
    path('edit_vendor/<int:vendor_id>/', views.add_edit_vendor, name='edit_vendor'), 
    path('delete_vendor_email/<int:id>/', views.delete_vendor_email, name='delete_vendor_email'),
    path('update_vendor_email/<int:id>/', views.update_vendor_email, name='update_vendor_email'), 
    path('add_vendor_email/<int:id>/', views.add_vendor_email, name='add_vendor_email'), 
    path('update_vendor_category/<int:id>/', views.update_vendor_category, name='update_vendor_category'),
    path('delete_vendor_category/<int:id>/', views.delete_vendor_category, name='delete_vendor_category'), 
    path('add_vendor_category/<int:id>/', views.add_vendor_category, name='add_vendor_category'), 
    path('update_vendor_menufacture/<int:id>/', views.update_vendor_menufacture, name='update_vendor_menufacture'),
    path('add_vendor_menufacture/<int:id>/', views.add_vendor_menufacture, name='add_vendor_menufacture'),
    path('delete_vendor_menufacture/<int:id>/', views.delete_vendor_menufacture, name='delete_vendor_menufacture'),
    path('update_vendor_model/<int:id>/', views.update_vendor_model, name='update_vendor_model'), 
    path('delete_vendor_model/<int:id>/', views.delete_vendor_model, name='delete_vendor_model'), 
    path('add_vendor_model/<int:id>/', views.add_vendor_model, name='add_vendor_model'), 
    path('view_vendor/<int:id>/', views.view_vendor, name='view_vendor'), 
    path('delete_vendor/<int:id>/', views.delete_vendor, name='delete_vendor'), 

    # Vendor Quotation Pages Admin Side
    path('quotation_list/', views.quotation_list, name='quotation_list'),
    path('add_vendor_quotation/', views.add_vendor_quotation, name='add_vendor_quotation'),
    path('get_buyer_email/', views.get_buyer_email, name='get_buyer_email'), 
    path('send_quotation/', views.send_quotation, name='send_quotation'), 

    path('view_vendor_inquiry/<int:id>/', views.view_vendor_inquiry, name='view_vendor_inquiry'),
    path('view_send_inquiry/<int:id>/', views.view_send_inquiry, name='view_send_inquiry'),
    path('send_quotation_to_buyer_email/', views.send_quotation_to_buyer_email, name='send_quotation_to_buyer_email'), 
    path('delete_vendor_quotation/<int:id>/', views.delete_vendor_quotation, name='delete_vendor_quotation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)