from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Suplier(models.Model):
      name_suplier= models.CharField(max_length=255)
      address= models.CharField(max_length=255,blank=True,null=True)
      phone_number= models.CharField(max_length=15,blank=True,null=True)

class Customer(AbstractUser):
      address= models.CharField(max_length=255,blank=True,null=True)
      phone_number= models.CharField(max_length=15,blank=True,null=True)