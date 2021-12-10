from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField

# Create your models here.
class StaffUser(models.Model):

    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )  
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    creation_datetime = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, null=True, blank=True) 
    status = models.CharField(max_length=1, null=True, blank=True, choices=STATUS)
    company_name = models.CharField(max_length=250, null=True, blank=True)
    phone_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True) 

    class Meta:
        verbose_name_plural = 'StaffUser'
        ordering = ['user']

    def __str__(self): 
        return self.user.username


class BuyerInquiry(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    category = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    menufacture = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    buyer_model = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    inquiry = models.TextField()
    location = models.CharField(max_length=200, null=True, blank=True)
    attachment_file = models.CharField(max_length=200, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)

    class Meta:
        verbose_name_plural = 'BuyerInquiry' 

    def __str__(self): 
        return self.category

class VendorInquiry(models.Model):
    STATUS=(
        ('1', 'Open'),
        ('2', 'Close'), 
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    quotation = models.TextField() 
    discount = models.CharField(max_length=200, null=True, blank=True)
    total_amount = models.CharField(max_length=200, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    attachment_file = models.CharField(max_length=200, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)

    class Meta:
        verbose_name_plural = 'VendorInquiry' 

    def __str__(self): 
        return self.notes