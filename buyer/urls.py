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

    # Admin Side Urls
    path('buyer_list/', views.buyer_list, name='buyer_list'),
    path('add_buyer/', views.add_edit_buyer, name='add_new_buyer'), 
    path('edit_buyer/<int:buyer_id>/', views.add_edit_buyer, name='edit_buyer'),
    path('update_buyer_email/<int:id>/', views.update_buyer_email, name='update_buyer_email'),
    path('add_buyer_email/<int:id>/', views.add_buyer_email, name='add_buyer_email'),
    path('delete_buyer_email/<int:id>/', views.delete_buyer_email, name='delete_buyer_email'),
    path('update_buyer_category/<int:id>/', views.update_buyer_category, name='update_buyer_category'), 
    path('add_buyer_category/<int:id>/', views.add_buyer_category, name='add_buyer_category'), 
    path('delete_buyer_category/<int:id>/', views.delete_buyer_category, name='delete_buyer_category'),
    path('update_buyer_menufacture/<int:id>/', views.update_buyer_menufacture, name='update_buyer_menufacture'),
    path('add_buyer_menufacture/<int:id>/', views.add_buyer_menufacture, name='add_buyer_menufacture'),
    path('delete_buyer_menufacture/<int:id>/', views.delete_buyer_menufacture, name='delete_buyer_menufacture'),
    path('update_buyer_model/<int:id>/', views.update_buyer_model, name='update_buyer_model'), 
    path('add_buyer_model/<int:id>/', views.add_buyer_model, name='add_buyer_model'), 
    path('delete_buyer_model/<int:id>/', views.delete_buyer_model, name='delete_buyer_model'),
    path('delete_buyer_attachment/<int:id>/', views.delete_buyer_attachment, name='delete_buyer_attachment'),
    path('update_buyer_attachment/<int:id>/', views.update_buyer_attachment, name='update_buyer_attachment'),
    path('add_buyer_attachment/<int:id>/', views.add_buyer_attachment, name='add_buyer_attachment'), 
    path('view_buyer/<int:id>/', views.view_buyer, name='view_buyer'),  
    path('delete_buyer/<int:id>/', views.delete_buyer, name='delete_buyer'), 

    # Buyer Inquiry Pages Admin Side
    path('buyer_inquiry_list/', views.buyer_inquiry_list, name='buyer_inquiry_list'),
    path('view_buyer_inquiry/<int:id>/', views.view_buyer_inquiry, name='view_buyer_inquiry'),
    path('edit_buyer_inquiry/<int:id>/', views.edit_buyer_inquiry, name='edit_buyer_inquiry'),
    path('update_buyer_inquiry/<int:inquiry_id>/', views.update_buyer_inquiry, name='update_buyer_inquiry'),
    #Buyer send inquiry to vendor
    path('view_send_buyer_inquiry/<int:inquiry_id>/', views.view_send_buyer_inquiry, name='view_send_buyer_inquiry'),
    path('send_buyer_inquiry_to_vendor/', views.send_buyer_inquiry_to_vendor, name='send_buyer_inquiry_to_vendor'), 
    #Delete Buyer Inquiry
    path('delete_buyer_inquiry/<int:id>/', views.delete_buyer_inquiry, name='delete_buyer_inquiry'),

    #Buyer Inquery form from admin side
    path('add_buyer_inquiry/', views.add_buyer_inquiry, name='add_buyer_inquiry'),  

    #Purchase Order For Buyer
    path('create_buyer_po/', views.create_buyer_po, name='create_buyer_po'), 
    path('get_buyer_email/', views.get_buyer_email, name='get_buyer_email'),
    path('buyer_po_list/', views.buyer_po_list, name='buyer_po_list'),  

    path('sendSimpleEmail/<emailto>/', views.sendSimpleEmail, name='sendSimpleEmail'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)