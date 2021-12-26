from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    STATUS=(
        ('1', 'open'),  
        ('2', 'Close'), 
    )      
    reference_no = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True,null=True, blank=True) 
    quotation = models.TextField(null=True, blank=True) 
    sub_total = models.CharField(max_length=200, null=True, blank=True)
    discount = models.CharField(max_length=200, null=True, blank=True)
    total_amount = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)  
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now_add=True) 
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS)
  
    def __str__(self): 
        return self.reference_no
