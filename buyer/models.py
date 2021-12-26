from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from users.models import StaffUser
from django.db.models.fields import DateTimeField 

# Create your models here.
class BuyerInquiry(models.Model):
    STATUS=(
        ('1', 'Received'),
        ('2', 'Sourcing'), 
        ('3', 'Submitted'), 
        ('4', 'Won'), 
        ('5', 'Lost'), 
        ('6', 'Close'), 
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    reference_no = models.CharField(max_length=200, null=True, blank=True)
    inquiry_type = models.CharField(max_length=200, null=True, blank=True)
    inquires = models.TextField(null=True, blank=True) 
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now_add=True) 
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.user

class BuyerAttachment(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    buyerinq = models.ForeignKey(BuyerInquiry, on_delete=models.CASCADE)   
    attachment_file = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.status


class BuyerCategories(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    buyer = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.category_name

class BuyerMenufactures(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    buyer = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    menufacture_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.menufacture_name

class BuyerModels(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    buyer = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.model_name

class BuyerEmails(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    buyer = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    email_list = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.email_list

class BuyerInquiryToVendor(models.Model):
       
    inquiry_id = models.CharField(max_length=20, null=True, blank=True)  
    quotes_received = models.CharField(max_length=20, null=True, blank=True)  
    no_of_vendor_send = models.CharField(max_length=20, null=True, blank=True)  
  
    def __str__(self): 
        return self.inquiry_id

class BuyerPO(models.Model):
    STATUS=(
        ('1', 'Send'), 
        ('2', 'Close'), 
    )  
    reference_no = models.CharField(max_length=200, null=True, blank=True)  
    quotation = models.TextField(null=True, blank=True)
    sub_total = models.CharField(max_length=200, null=True, blank=True)
    discount = models.CharField(max_length=200, null=True, blank=True)
    total_amount = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)    
    attachment_file = models.FileField(null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now_add=True) 
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.reference_no