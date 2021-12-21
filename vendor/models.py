from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User 
from users.models import StaffUser
from django.db.models.fields import DateTimeField

# Create your models here.
class VendorInquiry(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    inquiry_reference_no = models.CharField(max_length=200, null=True, blank=True)
    quotation = models.TextField(null=True, blank=True)
    sub_total = models.CharField(max_length=200, null=True, blank=True)
    discount = models.CharField(max_length=200, null=True, blank=True)
    total_amount = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  
    creation_datetime = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.notes

    
class VendorAttachment(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    vendorinq = models.ForeignKey(VendorInquiry, on_delete=models.CASCADE)   
    attachment_file = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.status

class Categories(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    vendor = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.category_name

class Menufactures(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    vendor = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    menufacture_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.menufacture_name

class VendorModels(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    vendor = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.model_name

class Emails(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    vendor = models.ForeignKey(StaffUser, on_delete=models.CASCADE)
    email_list = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.email_list