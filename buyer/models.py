from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from users.models import StaffUser
from django.db.models.fields import DateTimeField 

# Create your models here.
class BuyerInquiry(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    inquiry_type = models.CharField(max_length=200, null=True, blank=True)
    inquires = models.TextField(null=True, blank=True) 
    creation_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.category

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