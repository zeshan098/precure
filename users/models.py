from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StaffUser(models.Model):
      
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    role = models.CharField(max_length=10, null=True, blank=True) 
    status = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'StaffUser'
        ordering = ['user']

    def __unicode__(self):
        # return u"%s %s" % (self.user.first_name, self.user.last_name)
        return self.user.username