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
    buyer_vendor_name = models.CharField(max_length=250, null=True, blank=True)    
    company_name = models.CharField(max_length=250, null=True, blank=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    phone_no = models.CharField(max_length=100, null=True, blank=True) 
    alt_phone_no = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    location = models.CharField(max_length=250, null=True, blank=True)  
    role = models.CharField(max_length=10, null=True, blank=True) 
    status = models.CharField(max_length=1, null=True, blank=True, choices=STATUS)
    admin_notes = models.TextField(null=True, blank=True) 

    class Meta:
        verbose_name_plural = 'StaffUser'
        ordering = ['user']

    def __str__(self): 
        return self.user.username




